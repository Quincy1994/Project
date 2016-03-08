__author__ = 'root'
from django.conf.urls import patterns, url
from chenge.views import login,index1,student,teacher,adminstrator,ProjectApply,redirect,register,confure,MailSend
from chenge.views import check,Mailmessage,TeacherApplyMark,TeacherMidMark,TeacherEndMark
from chenge.views import TeacherMarking_ApplyReader,TeacherMarking_MidReader,TeacherMarking_EndReader
from chenge.views import Edition__Teacher,Edition__Student,CheckSituation,Edition
from chenge.views import Download,News,Notice,Achievement,Projectshow,Content,Leavemessage
from chenge.views import ProjectManagement,projectRead
from chenge.views import ProjectAnalyse,OneAnalyse
urlpatterns = patterns('',
    url(r'^$', login,name='login'),
    url(r'^login$', login,name='login'),
    url(r'^index1$',index1,name='index1'),
    url(r'^student',student,name='student'),
    url(r'^teacher',teacher,name='teacher'),
    url(r'^adminstrator',adminstrator,name='adminstrator'),
    url(r'^ProjectApply$',ProjectApply,name='ProjectApply'),
    url(r'^redirect$',redirect,name='redirect'),
    url(r'^register',register,name='register'),
    url(r'^confure$',confure,name='confure'),
    url(r'^check',check,name ='check'),
    url(r'^MailSend',MailSend,name ='MailSend'),
    url(r'^Mailmessage',Mailmessage,name ='Mailmessage'),
    url(r'^TeacherApplyMark',TeacherApplyMark,name ='TeacherApplyMark'),
    url(r'^TeacherMidMark',TeacherMidMark,name ='TeacherMidMark'),
    url(r'^TeacherEndMark',TeacherEndMark,name ='TeacherEndMark'),
    url(r'^TeacherMarking_ApplyReader',TeacherMarking_ApplyReader,name='TeacherMarking_ApplyReader'),
    url(r'^TeacherMarking_MidReader',TeacherMarking_MidReader,name='TeacherMarking_MidReader'),
    url(r'^TeacherMarking_EndReader',TeacherMarking_EndReader,name='TeacherMarking_EndReader'),
    url(r'^Edition__Teacher',Edition__Teacher,name='Edition__Teacher'),
    url(r'^Edition__Student',Edition__Student,name='Edition__Student'),
    url(r'^CheckSituation',CheckSituation,name='CheckSituation'),
    url(r'^Edition',Edition,name='Edition'),
    url(r'^Download',Download,name='Download'),
    url(r'^News',News,name='News'),
    url(r'^Notice',Notice,name='Notice'),
    url(r'^Achievement',Achievement,name='Achievement'),
    url(r'^Projectshow',Projectshow,name='Projectshow'),
    url(r'Content',Content,name='Content'),
    url(r'Leavemessage',Leavemessage,name='Leavemessage'),
    url(r'ProjectManagement',ProjectManagement,name='ProjectManagement'),
    url(r'projectRead',projectRead,name='projectRead'),
    url(r'ProjectAnalyse',ProjectAnalyse,name='ProjectAnalyse'),
    url(r'OneAnalyse',OneAnalyse,name='OneAnalyse'),
    )
