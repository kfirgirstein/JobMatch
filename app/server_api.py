import os, copy, random
from cvxopt import matrix, solvers
from app.models import *
import json


# using existing libraby name cvxopt to compute the minimum distance between 2 vectors in a given sub_space
# details on the input and demands of the function solvers.qp() are documented inside it's implementation file
# minimize 0.5x'Qx + px
# given Gx <= h, Ax = b
# recieving number of questions, minimal passing grade, list of passed candidates, list of failed candidates, and the old weight vector
def quadratic_programing_calculation(n, k, t, passed_vectors, failed_vectors, current_vector):
    new_vector = []

    #defining Q
    Q = 2*matrix(create_Q_list(n), (n,n))

    # defining h
    vector_h = (n+k) * [0.0]
    for i in range (0,len(passed_vectors)):
        vector_h[i] = -1*t
    for i in range (0,k):
        vector_h[i] = t
    h = matrix(vector_h, (n+k,1))

    # defining p
    vector_p = []
    for i in range (0,n):
        vector_p.append(current_vector[i])
    for i in range (0,n):
        vector_p[i] = -2.0 * vector_p[i]
    p = matrix(vector_p ,(n,1))

    # defining G
    list_G = []
    for i in range(0,len(passed_vectors)):
        single_vector = []
        for j in range (0,n):
            single_vector.append(-1.0 * passed_vectors[i][j])
        list_G.append(single_vector)
    for i in range(0,len(failed_vectors)):
        single_vector = []
        for j in range (0,n):
            single_vector.append(failed_vectors[i][j])
        list_G.append(single_vector)
    temp_list = create_Q_list(n)
    for i in range (0,n):
        single_vector = temp_list[i]
        for j in range (0,n):
            single_vector[j] = single_vector[j] * -1.0
        list_G.append(single_vector)
    G = transpose_matrix(list_G, n, k+n)
    G = matrix(G, (n+k,n))

    temp_list = n * [1.0]
    solvers.options['show_progress'] = False
    sol=solvers.qp(Q, p, G, h, matrix(temp_list, (1,n)), matrix(100.0))
    for i in range (0,n):
        new_vector.append(sol['x'][i])
    return new_vector

# create singular matrix of size nxn
def create_Q_list(n):
    Q_list = []
    list = n*[0.0]
    for i in range (0,n):
        temp_list = copy.copy(list)
        temp_list[i] = 1.0
        Q_list.append(temp_list)
    return Q_list

# transpose matrix of size nxk
def transpose_matrix(matrix_list, n, k):
    G = []
    for i in range (0,n):
        for j in range (0,k):
            G.append(matrix_list[j][i])
    return G

def update_company_questionwidth(_company,_list):
    data  = json.loads(_list)
    cluset=Clusters(company=_company)
    cluset.save()
    if cluset is None:
        raise RuntimeError('cannot initials clusters')
    each_weight=100/len(data)
    for q in data:
        quest=Question.objects.filter(pk=q).first()
        current_weight=Questions_weights(cluster=cluset,question=quest,weight=each_weight)
        if current_weight is None:
            raise MemoryError('cannot initials Questions weights')
        current_weight.save()

def change_weights_vector(name):
    company=Company.objects.filter(name=name).first()
    t = company.threshold
    n = company.num_of_questions
    clus=Clusters.objects.filter(company=company).first()
    current_vector = []
    questions_weights = Questions_weights.objects.filter(cluster=clus)
    for question_weight in questions_weights:
        current_vector.append(question_weight.weight)

    passed_vectors = []
    passed_submissions = Submissions.objects.filter(company=company, status = 3)
    for passed_submission in passed_submissions:
        temp_str = passed_submission.answeres
        passed_vectors.append(json.loads(temp_str))

    failed_vectors = []
    failed_submissions = Submissions.objects.filter(company=company, status = 4)
    for failed_submission in failed_submissions:
        temp_str = failed_submission.answeres
        failed_vectors.append(json.loads(temp_str))

    new_vector = quadratic_programing_calculation(n,len(failed_vectors)+len(passed_vectors),t, passed_vectors, failed_vectors, current_vector)
    print(new_vector)
    Questions_weights.objects.filter(cluster = clus)
    i = 0
    for question_weight in questions_weights:
        question_weight.weight = new_vector[i]
        question_weight.save()
        i += 1

def getCompanyWithQuestion():
    company_to_search=[]
    clus=Clusters.objects.all()
    for c in clus:
        qw = Questions_weights.objects.filter(cluster=c)
        if qw.exists():
            company_to_search.append(c.company.id)
    return Company.objects.filter(pk__in=company_to_search)

# checking sucess rate for high number of executions
def sucess_rate_test(base_vector,imitate_vector,company,iteration,candidate):
    t = company.threshold
    current_vector = list(base_vector)
    failed_vectors = []
    passed_vectors = []
    n = len(current_vector)

    with open(os.path.dirname(os.path.dirname(os.path.abspath(__file__))) + "\\static\\app\\"+company.name+".txt", "w") as test_file:
        for ii in range(0,iteration):
            for i in range(0,50):
                temp_vector = []
                grade_int = 0
                grade_old = 0
                for j in range (0,n):
                    temp_vector.append(float(random.randint(0, 1)))
                    grade_old += temp_vector[j] * current_vector[j]
                    grade_int += temp_vector[j] * imitate_vector[j]
                if grade_old > t and grade_int > t:
                    if list(temp_vector) in passed_vectors:
                        continue
                    else:
                        passed_vectors.append(list(temp_vector))
                elif grade_old > t and grade_int <= t:
                    if list(temp_vector) in failed_vectors:
                        continue
                    else:
                        failed_vectors.append(list(temp_vector))
            k = len(passed_vectors) + len(failed_vectors)
            current_vector=quadratic_programing_calculation(n, k, t, passed_vectors, failed_vectors, current_vector)
            test_file.write("Changing the weight vector for the " + str(ii + 1) + " time:\n" + str(current_vector) + "\n\n")
        try:
            pass_cur = 0
            pass_base = 0
            q_pass_cur = 0
            q_pass_base = 0
            fail_cur = 0
            fail_base = 0
            q_fail_cur = 0
            q_fail_base = 0
            for i in range(0,candidate):
                temp_vector = []
                grade_cur = 0
                grade_base = 0
                grade_int = 0
                for j in range (0, n):
                    temp_vector.append(float(random.randint(0, 1)))
                    grade_cur += temp_vector[j] * current_vector[j]
                    grade_base += temp_vector[j] * base_vector[j]
                    grade_int += temp_vector[j] * imitate_vector[j]
                if grade_cur > t and grade_int > t:
                    pass_cur += 1
                    q_pass_cur += 1
                elif grade_cur > t and grade_int <= t:
                    fail_cur += 1
                    q_pass_cur += 1
                elif grade_cur <= t:
                    q_fail_cur += 1
                if grade_base > t and grade_int > t:
                    pass_base += 1
                    q_pass_base += 1
                elif grade_base > t and grade_int <= t:
                    fail_base += 1
                    q_pass_base += 1
                elif grade_base <= t:
                    q_fail_base += 1

            test_file.write("\nnumber of candidates - "+str(candidate)+".\n\n")
            test_file.write("Without using the algorithm:\n")
            test_file.write("Numer of people passing the questionaire - " + str(q_pass_base) + "\n")
            test_file.write("Numer of people passing the interview - " + str(pass_base) + "\n")
            test_file.write("Percentage of people passing the interview after passing the questionaire: " + str((float)(pass_base/((float)(pass_base + fail_base)))*100) + "%\n")
            test_file.write("\nUsing the algorithm:" + "\n")
            test_file.write("Numer of people passing the questionaire - " + str(q_pass_cur) + "\n")
            test_file.write("Numer of people passing the interview - " + str(pass_cur) + "\n")
            test_file.write("Percentage of people passing the interview after passing the questionaire: " + str(((float)(pass_cur)/((float)(pass_cur + fail_cur)))*100) + "%\n")

            summary={"Summary":[{"Title":"candidates","value":candidate},
                                {"Title":"iteration","value":iteration},
                              {"Title":"passing questionaire before algorithm","value":q_pass_base}, 
                              {"Title":"passing interview before algorithm","value":pass_base},
                              {"Title":"% passing the interview before algorithm",
                              "value":(float)(pass_base/((float)(pass_base + fail_base)))*100},
                              {"Title":"passing the questionaire after algorithm","value":q_pass_cur},
                              {"Title":"passing the interview after algorithm","value":pass_cur},
                             {"Title":"% passing the interview after algorithm",
                               "value":((float)(pass_cur)/((float)(pass_cur + fail_cur)))*100}
                               ],
                     "Weight":json.dumps(current_vector)}
        except Exception as e:
            summary={"error":"faild to run demo"+e.message}
              
    return json.dumps(summary)
def sucess_rate_demo(base_vector,imitate_vector,company,iteration=1,candidate=1000):
       return sucess_rate_test(base_vector,imitate_vector,company,iteration,candidate)

