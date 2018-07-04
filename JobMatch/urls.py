"""
Definition of urls for JobMatch.
"""
from django.views.generic.base import RedirectView


from datetime import datetime
from django.conf.urls.static import static
from django.conf import settings
from django.conf.urls import url,include
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import TemplateView
from django.contrib import admin
import django.contrib.auth.views
from django.contrib.auth.decorators import login_required
from app.decorators import interviewer_required
from app.api import *
import app.forms
import app.views

favicon_view = RedirectView.as_view(url='/static/logo-fav.png', permanent=True)

# Uncomment the next lines to enable the admin:
# from django.conf.urls import include
# from django.contrib import admin
# admin.autodiscover()
urlpatterns = [
    url(r'^$', app.views.home, name='home'),
    url(r'^favicon\.ico$', favicon_view),
    url(r'^auth_api/',include('auth_api.urls')),
    url(r'^contact$', app.views.contact, name='contact'),
    url(r'^signup/$',TemplateView.as_view(template_name='app/Register.html'), name='register'),
    url(r'^signup/company/$',app.views.SignupSuper, name='signupSuper'),
    url(r'^signup/user/$',app.views.Signup, name='signup'),
    url(r'^progress/user/$',login_required(TemplateView.as_view(template_name='app/user_progress.html')),name='user_progress'),
    url(r'^progress/company/$',interviewer_required(TemplateView.as_view(template_name='app/company_progress.html')),name='copmany_progress'),
    url(r'^email/$',login_required(TemplateView.as_view(template_name='app/email-inbox.html')),name='email'),
    url(r'^email/read/$',login_required(TemplateView.as_view(template_name='app/email-read.html')),name='email-read'),
    url(r'^email/send/$',login_required(TemplateView.as_view(template_name='app/email-compose.html')),name='email-send'),
    url(r'^profile/$',login_required(TemplateView.as_view(template_name='app/profile.html')),name='profile'),
    url(r'^home/$',login_required(app.views.dashboard),name='dashboard'),
    url(r'^company/(?P<name>[A-Za-z]+)/$',app.views.CompanyFormView, name='company_form'),
    url(r'^search/company/(?P<name>[A-Za-z]+)/$',app.views.CompanySearch, name='search_company'),
    url(r'^mini/company/(?P<name>[A-Za-z]+)/$',app.views.CompanySearchMini, name='company_mini'),
    url(r'^download/(?P<name>[A-Za-z]+)/', app.views.downloadFile),
    url(r'^about', app.views.about, name='about'),
    url(r'^login/$',
        django.contrib.auth.views.login,
        {
            'template_name': 'app/login.html',
            'authentication_form': app.forms.BootstrapAuthenticationForm,
            'extra_context':
            {
                'title': 'Log in',
                'year': datetime.now().year,
            }
        },
        name='login'),
    url(r'^logout$',
        django.contrib.auth.views.logout,
        {
            'next_page': '/',
        },
        name='logout'),

    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^api/question_weight/(?P<name>.+)/$', QuestionWeightListView.as_view()),
    url(r'^api/submission/company/$', SubmissionCompanyListView.as_view()),
    url(r'^api/submission/user/$', SubmissionUserListView.as_view()),
    url(r'^api/add/question/$',csrf_exempt( AddQuestion.as_view())),
    url(r'^api/question/$', QuestionListView.as_view()),
    url(r'^api/vector/', VectorCompany.as_view()),
    url(r'^api/demo/', GetDemoForCompany.as_view()),
    url(r'^api/update/company/$', UpdateCompanyWeight.as_view()),


]+ static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)


