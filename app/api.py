

from rest_framework.generics import ListAPIView,RetrieveAPIView
from django.http import HttpResponseRedirect
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status
from django.http import JsonResponse
from json import dumps
from django.core import serializers
from rest_framework.views import APIView
from rest_framework.renderers import JSONRenderer
from app.models import *
from app.serializers import *
from app.server_api import *





class QuestionListView(ListAPIView):
    queryset=Question.objects.all()
    serializer_class=QuestionSerializer

class QuestionWeightListView(ListAPIView):
    serializer_class = QuestionsWeightsSerializer

    def get_queryset(self):
        nameToFind = self.kwargs['name']
        try:
            comp=Company.objects.filter(name=nameToFind).first()
            clus=Clusters.objects.filter(company=comp).first()
            if clus is not None:
                queryset = Questions_weights.objects.filter(cluster=clus)
                if not queryset:
                  queryset=Company.objects.filter(name=nameToFind)
        except Exception as e:
            queryset=Company.objects.filter(name=nameToFind)
        return queryset

class SubmissionCompanyListView(ListAPIView):
    serializer_class = SubmissionsSerializer
    def get_queryset(self):
        nameToFind = self.request.user.username;
        try:
            comp=Company.objects.filter(name=nameToFind).first()
            if comp is not None:
                queryset = Submissions.objects.filter(company=comp)
                if not queryset:
                  queryset=comp
        except Exception as e:
            queryset=Company.objects.filter(name=nameToFind)
        return queryset

class SubmissionUserListView(ListAPIView):
    serializer_class = SubmissionsSerializer
    def get_queryset(self):
        try:
            userf=self.request.user
            if userf is not None:
                queryset = Submissions.objects.filter(user=userf)
                if not queryset:
                  queryset==User.objects.filter(name=nameToFind)
        except Exception as e:
            queryset==User.objects.filter(name=nameToFind)
        return queryset

class UpdateCompanyWeight(APIView):
    renderer_classes = (JSONRenderer, )

    def post(self, request):
        try:
            result_json = {}
            sent_user=User.objects.filter(pk=request.data["user"])
            comp=Company.objects.filter(name=request.user.username).first()
            if sent_user is not None:
                sub=Submissions.objects.filter(user=sent_user).filter(company=comp).first()
                if sub is None or sub.status_id==1:
                     result_json['error'] = 'user not have interview..'
                else:
                    if request.data["option"]==3:
                        sub.status_id=3
                        sub.save()
                    elif request.data["option"]==4:
                        sub.status_id=4
                        sub.save()
                        change_weights_vector(request.user.username)
                    else:
                         result_json['error'] = 'invalid user option'
            else:
                result_json['error'] = 'invalid user'
        except Exception as e:
              return Response(data=e, status=status.HTTP_405_METHOD_NOT_ALLOWED)

        return Response(data="ok" ,status=status.HTTP_200_OK)


class AddQuestion(ListAPIView):
    renderer_classes = (JSONRenderer, )
    def post(self, request, format=None):
       try:
           if not 'id' in request.data:
                 question = Question(description=request.data['description'],
                                     option_a=request.data['option_a'],
                                     option_b=request.data['option_b'],
                                     correct_answer=request.data['correct_answer']
                                     )
                 if 'option_c' in request.data:
                     question.option_c=request.data['option_c']
                 if 'option_d' in request.data:
                     question.option_d=request.data['option_d']
                 question.save()
                 return Response(data=list(Question.objects.all().values()), status=status.HTTP_200_OK)

       except Exception as e:
            return Response(data=e, status=status.HTTP_405_METHOD_NOT_ALLOWED)
        
      
class VectorCompany(APIView):
    renderer_classes = (JSONRenderer, )

    def get(self, request, format=None):
        t = 55
        current_vector = [10.0, 10.0, 10.0, 10.0, 10.0, 10.0, 10.0, 10.0, 10.0, 10.0]
        passed_vectors = [[1, 1, 1, 1, 1, 0, 0, 0, 0, 0], [1, 1, 1, 1, 0, 1, 0, 0, 0, 0], [1, 1, 1, 1, 0, 0, 1, 0, 0, 0], [1, 1, 1, 1, 0, 0, 0, 1, 0, 0], [1, 1, 1, 1, 0, 0, 0, 0, 1, 0], [1, 1, 1, 1, 0, 0, 0, 0, 0, 1]]
        failed_vector = [0, 0, 0, 0, 0, 1, 1, 1, 1, 1]
        n = len(current_vector)
        k = len(passed_vectors) + 1
        content= quadratic_programing_calculation(n, k, t, passed_vectors, failed_vector, current_vector)
        return Response(content)


class GetDemoForCompany(APIView):
    renderer_classes = (JSONRenderer, )
    
    def post(self, request, format=None):
        try:
            if not 'imitate' in request.data:
                 return Response(data='no data', status=status.HTTP_405_METHOD_NOT_ALLOWED)
            if not 'iteration' in request.data:
                iteration=1
            else:
                iteration=request.data['iteration']
            if not 'candidates' in request.data:
                candidates=1000
            else:
                candidates=request.data['candidates']
            _company=Company.objects.filter(name=request.user.username).first()
            clus=Clusters.objects.filter(company=_company).first()
            current_weight = Questions_weights.objects.filter(cluster=clus).values_list('weight', flat=True)
            content= sucess_rate_demo(list(current_weight),request.data['imitate'],_company,iteration,candidates)
            return Response(content)

        except Exception as e:
           return Response(data=e, status=status.HTTP_405_METHOD_NOT_ALLOWED)




