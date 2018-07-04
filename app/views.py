"""
Definition of views.
"""
import sys,os,json
from django.shortcuts import render,redirect
from rest_framework import status
from django.contrib import messages 
from django.http import HttpRequest,HttpResponse,HttpResponseRedirect
from django.template import RequestContext
from datetime import datetime
from django.contrib.auth import authenticate
from app.forms import RegistrtionForm,SuperRegistrtionForm,CompanyForm
from app.models import *
from django.contrib.auth.decorators import login_required
from app.decorators import interviewer_required
from app.server_api import update_company_questionwidth,getCompanyWithQuestion
from django.utils.encoding import smart_str





def dashboard(request):
    result =  getCompanyWithQuestion()
    return render(
        request,
        'app/dashboard.html',
        {
            'companies':result,
        }
    )
def home(request):
    """Renders the home page."""
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/index.html',
        {
            'title':'Home Page',
            'year':datetime.now().year,
        }
    )
def contact(request):
    """Renders the contact page."""
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/contact.html',
        {
            'title':'Contact',
            'message':'Your contact page.',
            'year':datetime.now().year,
        }
    )
def about(request):
    """Renders the about page."""
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/about.html',
        {
            'title':'About',
            'message':'Your application description page.',
            'year':datetime.now().year,
        }
    )

@interviewer_required(login_url='/home/')
@login_required
def CompanyFormView(request,name):
    if request.method=="GET":
        comp=Company.objects.filter(name=name)
        if not comp:
          form=CompanyForm()
          return render(request,'app/company_create.html',{'form':form})

        return render(request,'app/company_profile.html',{'companies':comp.first()})
    
    elif request.method=="POST":
        form=CompanyForm(request.POST)
        try:
            if form.is_valid():
                update_company_questionwidth(form.save(request.user),request.POST['questions'])
                return redirect('/company/'+request.user.username)
        except Exception as e:
             form =CompanyForm(e)
    return render(request, 'app/company_create.html', {'form':form})

@login_required
def CompanySearchMini(request,name):
    comp=Company.objects.filter(name=name)
    if not comp:
        return HttpResponse(status=status.HTTP_404_NOT_FOUND)
    return render(request,'app/company_mini.htm',)
  
@login_required
def CompanySearch(request,name):
  if request.method=="GET":
      comp=Company.objects.filter(name=name)
      if not comp:
          return HttpResponse(status=status.HTTP_404_NOT_FOUND)
      if comp.first().name==request.user.username:
          return redirect('/progress/company/')
      sub=Submissions.objects.filter(user=request.user).filter(company=comp)
      if not sub: 
          return render(request,'app/company_form.html',)
      return redirect('/progress/user/')

  elif request.method=="POST":
       comp=Company.objects.filter(name=name).first()
       clus=Clusters.objects.filter(company=comp).first()
       if not comp:
           return HttpResponse(status=status.HTTP_404_NOT_FOUND)
       queryset = Questions_weights.objects.filter(cluster=clus)
       answers=[]
       grade=0.0
       for qw in queryset:
           if int(request.POST[str(qw.id)])==qw.question.correct_answer:
               answers.append(1)
               grade=grade+qw.weight
           else:
               answers.append(0)
       if(grade>=comp.threshold):
           submit_status=Status.objects.get(pk=2)
       else:
           submit_status=Status.objects.get(pk=1)
       submit=Submissions(user=request.user,company=comp,status=submit_status,answeres=json.dumps(answers))
       if submit is not None:
           submit.save()
           return redirect('/home/')
       return HttpResponse(status=status.HTTP_409_CONFLICT)



def Signup(request):
    if request.method=="GET":
        form=RegistrtionForm()
        return render(request,'app/RegisterUser.html',{'form':form})
    elif request.method=="POST":
        form=RegistrtionForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/login/')
    return render(request, 'app/RegisterUser.html', {'form':form})

def SignupSuper(request):
    if request.method=="GET":
        form=SuperRegistrtionForm()
        return render(request,'app/RegisterInterviewer.html',{'form':form})
    elif request.method=="POST":
        form=SuperRegistrtionForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/login/')
    return render(request, 'app/RegisterInterviewer.html', {'form':form})

def create_vector(request):
    t = 55
    current_vector = [10.0, 10.0, 10.0, 10.0, 10.0, 10.0, 10.0, 10.0, 10.0, 10.0]
    passed_vectors = [[1, 1, 1, 1, 1, 0, 0, 0, 0, 0], [1, 1, 1, 1, 0, 1, 0, 0, 0, 0], [1, 1, 1, 1, 0, 0, 1, 0, 0, 0], [1, 1, 1, 1, 0, 0, 0, 1, 0, 0], [1, 1, 1, 1, 0, 0, 0, 0, 1, 0], [1, 1, 1, 1, 0, 0, 0, 0, 0, 1]]
    failed_vector = [0, 0, 0, 0, 0, 1, 1, 1, 1, 1]
    n = len(current_vector)
    k = len(passed_vectors) + 1
    return quadratic_prgraming_calculation(n, k, t, passed_vectors, failed_vector, current_vector)

def downloadFile(request,name):
    test_file = open(os.path.dirname(os.path.dirname(os.path.abspath(__file__))) + "\\static\\app\\"+name+".txt", 'rb')
    response = HttpResponse(content=test_file)
    response['Content-Type'] = 'application/force-download'
    response['Content-Disposition'] = 'attachment; filename="%s.txt"'% smart_str(name)
    return response