#coding:utf-8
from django.contrib.auth import authenticate ,login as user_login,logout
from django.contrib.auth.models import User
import json
from django.shortcuts import render, render_to_response
from django import forms
from django.http import HttpResponseRedirect,HttpResponse
from django.template.context import RenderContext, RequestContext
from chenge.models import Userprofile,Users
from django.contrib.auth.decorators import login_required
from django.core.servers.basehttp import FileWrapper
import os
import sys
from DLL import DllLogin ,DllRegister,DllprojectApply,DLLprojectPDF,DLLAdmMailSend
from models import handle_uploaded_file
from DLL import checkproject,Edtioninfo,AdminForCheck,information,DllLeaveMessage,DllprojectManage,DllProjectAnalysis,MainPage
from DAL import *
class UserForm(forms.Form):
    username=forms.CharField(label='username:',error_messages={'required':'Please input your username'},max_length=100)
    password=forms.CharField(label='password:',error_messages={'required':'Please input your password'},widget=forms.PasswordInput())

class FileForm(forms.Form):
    username =forms.CharField()
    projectfile = forms.FileField()

def login(request):
    m = MainPage()
    noticelist,newslist =m.GetContent()
    if noticelist.__len__() > 4 :
        noticelist =noticelist[1:4]
    if newslist.__len__() > 4:
        newslist = newslist[1:4]
    if request.method=="POST":
        uf=UserForm(request.POST)
        try:
            if request.POST['register']:
                return HttpResponseRedirect('/register')
        except:
            if uf.is_valid():
                username=uf.cleaned_data['username']
                password=uf.cleaned_data['password']
                userType=request.POST['variety']
                dlllogin=DllLogin()
                tag=dlllogin.UserLogin(userType,username,password)
                user=authenticate(username=username,password=password)
                print user
                if tag :
                    if user is None:
                        user = User.objects.create_user(username=username,password=password)
                        user.save()
                    user=authenticate(username=username,password=password)
                    if user is not None:
                        if user.is_active:
                            user_login(request, user)
                            print request.user,'ok'
                    if userType == '1':
                        return HttpResponseRedirect('/student/%s'%username)
                    elif userType == '2':
                        return HttpResponseRedirect('/teacher/%s'%username)
                    elif userType == '3':
                        return HttpResponseRedirect('/adminstrator/%s'%username)
                else:
                    return render_to_response('login.html',{'uf':uf ,'noticelist':noticelist,'newslist':newslist})
            else:
                return render_to_response('login.html',{'uf':uf,'noticelist':noticelist,'newslist':newslist})
    else:
        return render_to_response('login.html',{'noticelist':noticelist,'newslist':newslist})


def index1(request):
    if request.method == 'POST':
            return render_to_response('index1.html',RenderContext(request))
    return render_to_response('index1.html',RenderContext(request))

def register(request):
    if request.method == 'POST':
        try:
            if request.POST['returnLogin']:
                return HttpResponseRedirect('/login')
        except:
            name =request.POST['name']
            usertype = request.POST['userType']
            id = request.POST['id']
            password = request.POST['password']
            college = request.POST['department']
            try :
                grade = request.POST['grade']
            except:
                grade =None
            try:
                title = request.POST['title']
            except:
                title =None
            mail = request.POST['mail']
            phone = request.POST['phone']
            print (usertype,id,password,name,college,grade,title,phone,mail)
            d = DllRegister()
            if d.UserRegister(usertype,id,password,name,college,grade,title,phone,mail):
               return HttpResponseRedirect('/')
            return render_to_response('register.html',RenderContext(request))
    return render_to_response('register.html',RenderContext(request))


def student(request):
    m = MainPage()
    noticelist,newslist =m.GetContent()
    if noticelist.__len__() > 4 :
        noticelist =noticelist[1:4]
    if newslist.__len__() > 4:
        newslist = newslist[1:4]
    user = request.user
    # d =Dal()
    # sname=d.getstudentname(user)
    if not request.user.is_authenticated():
        return render_to_response('redirect.html',RenderContext(request))
    if request.method == 'POST':
        try:
            if request.POST['logout']:
                logout(request)
                return HttpResponseRedirect('/')
        except:
            return render_to_response('student.html',{'user':user,'noticelist':noticelist,'newslist':newslist})
    return render_to_response('student.html',{'user':user,'noticelist':noticelist,'newslist':newslist})

def teacher(request):
    m = MainPage()
    noticelist,newslist =m.GetContent()
    if noticelist.__len__() > 4 :
        noticelist =noticelist[1:4]
    if newslist.__len__() > 4:
        newslist = newslist[1:4]
    user = request.user
    # d =Dal()
    # tname=d.getstudentname(user)
    if not request.user.is_authenticated():
        return render_to_response('redirect.html',RenderContext(request))
    if request.method == 'POST':
        if request.POST['logout']:
            logout(request)
            return HttpResponseRedirect('/')
        return render_to_response('teacher.html',{'user':user,'noticelist':noticelist,'newslist':newslist})
    return render_to_response('teacher.html',{'user':user,'noticelist':noticelist,'newslist':newslist})

def adminstrator(request):
    m = MainPage()
    noticelist,newslist =m.GetContent()
    if noticelist.__len__() > 4 :
        noticelist =noticelist[1:4]
    if newslist.__len__() > 4:
        newslist = newslist[1:4]
    user = request.user
    if not request.user.is_authenticated():
        return render_to_response('redirect.html',RenderContext(request))
    if request.method == 'POST':
        if request.POST['logout']:
            logout(request)
            return HttpResponseRedirect('/')
        return render_to_response('adminstrator.html',{'user':user,'noticelist':noticelist,'newslist':newslist})
    return render_to_response('adminstrator.html',{'user':user,'noticelist':noticelist,'newslist':newslist})

def ProjectApply(request):
    user = request.user
    if not request.user.is_authenticated():
        return render_to_response('redirect.html',RenderContext(request))
    if request.method == 'POST':
        try:
            if request.POST['logout']:
                logout(request)
                return HttpResponseRedirect('/')
        except:
            projectDict={}
            projectDict['project_name'] = request.POST['project_name']
            projectDict['project_department'] = request.POST['project_department']#思科信息学院
            projectDict['batch'] = request.POST['batch'] #2012,2013,2014,2015
            projectDict['project_variety'] = request.POST['variety']  #创新实验项目 ,创新训练项目
            projectDict['project_type'] = request.POST['type'] #文科
            projectDict['project_year'] = request.POST['year'] #1 year ,2year
            projectDict['project_id'] = request.POST['project_id']
            projectDict['project_file'] = request.FILES['fileField']

            projectDict['s1_name'] = request.POST['s1_name']
            projectDict['s1_department'] =request.POST['s1_department']
            projectDict['s1_id'] = request.POST['s1_id']
            projectDict['s1_grade'] = request.POST['s1_grade']
            filedir = u'申报待审核/'
            projectDict['filepath']=handle_uploaded_file(projectDict['project_file'],request.FILES['fileField'].name,projectDict['project_department'],projectDict['s1_id'],filedir)

            projectDict['t1_name'] = request.POST['t1_name']
            projectDict['t1_department'] = request.POST['t1_department']
            projectDict['t1_title'] = request.POST['t1_title']
            projectDict['t1_id'] = request.POST['t1_id']

            projectDict['t2_name'] = request.POST['t2_name']
            projectDict['t2_department'] = request.POST['t2_department']
            projectDict['t2_title'] = request.POST['t2_title']
            projectDict['t2_id'] = request.POST['t2_id']

            projectDict['s2_name'] = request.POST['s2_name']
            projectDict['s2_department'] =request.POST['s2_department']
            projectDict['s2_id'] = request.POST['s2_id']
            projectDict['s2_grade'] = request.POST['s2_grade']

            projectDict['s3_name'] = request.POST['s3_name']
            projectDict['s3_department'] =request.POST['s3_department']
            projectDict['s3_id'] = request.POST['s3_id']
            projectDict['s3_grade'] = request.POST['s3_grade']

            projectDict['s4_name'] = request.POST['s4_name']
            projectDict['s4_department'] =request.POST['s4_department']
            projectDict['s4_id'] = request.POST['s4_id']
            projectDict['s4_grade'] = request.POST['s4_grade']

            projectDict['s5_name'] = request.POST['s5_name']
            projectDict['s5_department'] =request.POST['s5_department']
            projectDict['s5_id'] = request.POST['s5_id']
            projectDict['s5_grade'] = request.POST['s5_grade']
            #
            projectDict['project_key1'] = request.POST['project_key1']
            projectDict['project_key2'] = request.POST['project_key2']
            projectDict['project_key3'] = request.POST['project_key3']
            projectDict['project_info'] = request.POST['project_info']
            projectDict['pro_status']=u'申报待审核'

            dll = DllprojectApply()
            if dll.ProjectApply(projectDict):
                message = 'apply success!!'
                return render_to_response('confure.html',{'message':message})
            return render_to_response('ProjectApply.html',{'user':user})
    return render_to_response('ProjectApply.html',{'user':user})

def redirect(request):
    return render_to_response('redirect.html',RenderContext(request))
def confure(request):
    user =request.user
    return HttpResponseRedirect('/student/%s'%user)
def Mailmessage(request):
    return render_to_response('Mailmessge.html',RenderContext(request))
def check(request):
    if request.method == 'POST':
         if request.POST['checkPDF'] == 'checkPDF':
            print 'checkPDF'
            projectfile = request.FILES['fileField']
            d =DLLprojectPDF()
            checklist =d.projectPDFcheck(projectfile,request.FILES['fileField'].name)
            print checklist
            return render_to_response('check.html',{'checklist':checklist})
    return render_to_response('check.html',RenderContext(request))

def MailSend(request):
    user =request.user
    if request.method == 'POST':
        try:
            if request.POST['logout']:
                    logout(request)
                    return HttpResponseRedirect('/')
        except:
            receiver = request.POST['receiver']
            college = request.POST['sending_department']
            title = request.POST['title']
            content = request.POST['sending_message']
            filename = request.POST['textfield']
            receivers=''
            receivers = receivers+ u'%s'%(receiver)
            receiverlist = receivers.split('*')
            transaction = ''
            transaction = transaction + u'%s'%(title)
            cp = checkproject()
            cp.isCheck(transaction,receiverlist,college)
            try :
                student = request.POST['check_student']
            except:
                student = None
            try :
                teacher = request.POST['check_teacher']
            except:
                teacher = None
            try :
                if filename is not None:
                    file = request.FILES['sending_file']
                    f_name = request.FILES['sending_file'].name
            except:
                file = None
                f_name = None
            ada =DLLAdmMailSend()
            tag = ada.Mail(user,receiverlist,college,title,content,f_name,student,teacher,file)
            if tag == True:
                message = u'发送成功'
                return render_to_response('Mailmessge.html',{'message':message})
            else:
                message = u'发送失败'
            return render_to_response('Mailmessge.html',{'message':message})
    return render_to_response('MailSend.html',{'user':user})

def TeacherApplyMark(request):
    user =request.user
    d =Dal()
    t_name = d.getTeachername(user)
    try:
        if request.POST['logout']:
            logout(request)
            return HttpResponseRedirect('/')
    except:
        c =checkproject()
        pro_status = u'申报待审核'
        project_Dict = c.TeachGetProject(pro_status,user)
        project_names=project_Dict.keys()
        project_list=[]
        for p in project_names :
            project_list.append(p)
        ProjectMarks = c.TeachGetProjectMark(project_list,user)
        for i in range(0,project_list.__len__(),1):
            try :
                if int(request.POST['project']) == (i+1) :
                    filename = project_Dict[project_list[i]]
                    return render_to_response('TeacherMarking_ApplyReader.html',{'filename':filename})
            except:
                continue
        for i in range(0,project_list.__len__(),1):
            try:
               if int(request.POST['MarkSubmit']) == (i+1):
                    point = request.POST[project_list[i]]
                    advice=''
                    advice= advice+u'%s'%(request.POST['TextArea'])
                    p_name = project_list[i]
                    c = checkproject()
                    c.BLLStoreApply(p_name,t_name,point,advice)
                    ProjectMarks[p_name] = point
                    if advice == '':
                        return render_to_response('TeacherApplyMark.html',{'user':user,'ProjectMarks':ProjectMarks})
                    else:
                        c.SendAdvice(t_name,advice,p_name)
                        return render_to_response('TeacherApplyMark.html',{'user':user,'ProjectMarks':ProjectMarks})
            except:
                continue
        # try :
        #     if request.POST['finished']:
        try :
            if request.POST['finished'] == '1':
                c.DllCheckover(ProjectMarks,t_name)
                return render_to_response('TeacherApplyMark.html',{'user':user,'ProjectMarks':ProjectMarks})
        except:
            return render_to_response('TeacherApplyMark.html',{'user':user,'ProjectMarks':ProjectMarks})
    return render_to_response('TeacherApplyMark.html',{'user':user})

def TeacherMidMark(request):
    user =request.user
    d =Dal()
    t_name = d.getTeachername(user)
    try:
        if request.POST['logout']:
            logout(request)
            return HttpResponseRedirect('/')
    except:
        c =checkproject()
        pro_status = u'中期待审核'
        project_Dict = c.TeachGetProject(pro_status,user)
        project_names=project_Dict.keys()
        project_list=[]
        for p in project_names :
            project_list.append(p)
        ProjectMarks = c.TeachGetProjectMark(project_list,user)
        for i in range(0,project_list.__len__(),1):
            try :
                if int(request.POST['project']) == (i+1) :
                    filename = project_Dict[project_list[i]]
                    return render_to_response('TeacherMarking_MidReader.html',{'filename':filename})
            except:
                continue

        for i in range(0,project_list.__len__(),1):
            try:
               if int(request.POST['MarkSubmit']) == (i+1):
                    point = request.POST[project_list[i]]
                    advice=''
                    advice= advice+u'%s'%(request.POST['TextArea'])
                    p_name = project_list[i]
                    c = checkproject()
                    c.BLLStoreMid(p_name,t_name,point,advice)
                    ProjectMarks[p_name] = point
                    if advice == '':
                        return render_to_response('TeacherMidMark.html',{'user':user,'ProjectMarks':ProjectMarks})
                    else:
                        c.SendAdvice(t_name,advice,p_name)
                        return render_to_response('TeacherMidMark.html',{'user':user,'ProjectMarks':ProjectMarks})
            except:
                continue
        try :
            if request.POST['finished'] == '1':
                c.DllCheckover(ProjectMarks,t_name)
                return render_to_response('TeacherMidMark.html',{'user':user,'ProjectMarks':ProjectMarks})
        except:
            return render_to_response('TeacherMidMark.html',{'user':user,'ProjectMarks':ProjectMarks})

    return render_to_response('TeacherMidMark.html',{'user':user})

def TeacherEndMark(request):
    user =request.user
    d =Dal()
    t_name = d.getTeachername(user)
    try:
        if request.POST['logout']:
            logout(request)
            return HttpResponseRedirect('/')
    except:
        c =checkproject()
        pro_status = u'结项待审核'
        project_Dict = c.TeachGetProject(pro_status,user)
        project_names=project_Dict.keys()
        project_list=[]
        for p in project_names :
            project_list.append(p)
        ProjectMarks = c.TeachGetProjectMark(project_list,user)
        for i in range(0,project_list.__len__(),1):
            try :
                if int(request.POST['project']) == (i+1) :
                    filename = project_Dict[project_list[i]]
                    return render_to_response('TeacherMarking_EndReader.html',{'filename':filename})
            except:
                continue
        for i in range(0,project_list.__len__(),1):
            try:
               if int(request.POST['MarkSubmit']) == (i+1):
                    point = request.POST[project_list[i]]
                    advice=''
                    advice= advice+u'%s'%(request.POST['TextArea'])
                    p_name = project_list[i]
                    c = checkproject()
                    c.BLLStoreEnd(p_name,t_name,point,advice)
                    ProjectMarks[p_name] = point
                    if advice == '':
                       return render_to_response('TeacherEndMark.html',{'user':user,'ProjectMarks':ProjectMarks})
                    else:
                        c.SendAdvice(t_name,advice,p_name)
                        return render_to_response('TeacherEndMark.html',{'user':user,'ProjectMarks':ProjectMarks})
            except:
                continue
        try :
            if request.POST['finished'] == '1':
                c.DllCheckover(ProjectMarks,t_name)
                return render_to_response('TeacherEndMark.html',{'user':user,'ProjectMarks':ProjectMarks})
        except:
            return render_to_response('TeacherEndMark.html',{'user':user,'ProjectMarks':ProjectMarks})
    return render_to_response('TeacherEndMark.html',{'user':user})


def TeacherMarking_ApplyReader(request):
    try:
        if request.POST['back']:
            return render_to_response('TeacherApplyMark.html')
    except:
        return render_to_response('TeacherMarking_ApplyReader.html')

def TeacherMarking_MidReader(request):
    try:
        if request.POST['back']:
            return render_to_response('TeacherMidMark.html')
    except:
        return render_to_response('TeacherMarking_MidReader.html')

def TeacherMarking_EndReader(request):
    try:
        if request.POST['back']:
            return render_to_response('TeacherEndMark.html')
    except:
        return render_to_response('TeacherMarking_EndReader.html')

def Edition__Teacher(request):
    user = request.user
    try:
        if request.POST['logout']:
            logout(request)
            return HttpResponseRedirect('/')
    except:
        None
    teacherDict={}
    try:
        if request.POST['submit'] == '1':
            teacherDict['t_name'] = request.POST['t_name']
            teacherDict['t_id'] = u'%s'%(user)
            teacherDict['pwd'] = request.POST['pwd']
            teacherDict['college'] = request.POST['college']
            teacherDict['title'] = request.POST['title']
            teacherDict['mail'] = request.POST['mail']
            teacherDict['phone'] = request.POST['phone']
            e =Edtioninfo()
            e.DllTeacherinfo(teacherDict)
    except:
        None
    e = Edtioninfo()
    teacherDict=e.Teacherinfo(user)
    pwd = teacherDict['pwd']
    t_name=teacherDict['t_name']
    college = teacherDict['college']
    title =teacherDict['title']
    mail =teacherDict['mail']
    phone = teacherDict['phone']
    return render_to_response('Edition__Teacher.html',{'user':user,'t_name':t_name,'pwd':pwd,'college':college,'title':title,'mail':mail,'phone':phone})


def Edition__Student(request):
    user = request.user
    try:
        if request.POST['logout']:
            logout(request)
            return HttpResponseRedirect('/')
    except:
        None
    studentDict={}
    try:
        if request.POST['submit'] == '1':
            studentDict['s_name'] = request.POST['s_name']
            studentDict['s_id'] = u'%s'%(user)
            studentDict['pwd'] = request.POST['pwd']
            studentDict['college'] = request.POST['college']
            studentDict['grade'] = request.POST['grade']
            studentDict['mail'] = request.POST['mail']
            studentDict['phone'] = request.POST['phone']
            print studentDict
            e =Edtioninfo()
            e.DllStudentinfo(studentDict)
    except:
        None
    e = Edtioninfo()
    studentDict=e.Studentinfo(user)
    pwd = studentDict['pwd']
    s_name=studentDict['s_name']
    college =studentDict['college']
    grade =studentDict['grade']
    mail =studentDict['mail']
    phone = studentDict['phone']
    return render_to_response('Edition__Student.html',{'user':user,'s_name':s_name,'pwd':pwd,'college':college,'grade':grade,'mail':mail,'phone':phone})

class Project:
    projectMarks = None
    def __init__(self,projectMarks):
        self.__class__.projectMarks = projectMarks

def CheckSituation(request):
    user = request.user
    try:
        if request.POST['logout']:
            logout(request)
            return HttpResponseRedirect('/')
    except:
        None
    try:
        if request.POST['check']:
            college = request.POST['college']
            p_status = request.POST['p_status']
            a = AdminForCheck()
            ProjectMarks = a.getprojects(college,p_status)
            Project(ProjectMarks)
            return render_to_response('CheckSituation.html',{'user':user,'ProjectMarks':ProjectMarks,'p_status':p_status,'college':college})
    except:
        None
    try:
        if request.POST['changed'] == '1':
            projectlist = Project.projectMarks.keys()
            for i in range(0,projectlist.__len__(),1):
                projectstatus = request.POST[str(i+1)]
                p_name = projectlist[i]
                points = Project.projectMarks[p_name]
                status = ''
                status = status + u'%s'%(projectstatus)
                if status == u'终止项目':
                    a =AdminForCheck()
                    a.delete(p_name)
                    continue
                a = AdminForCheck()
                a.CheckSubmit(points,projectstatus,p_name)
            return render_to_response('CheckSituation.html',{'user':user})
        return render_to_response('CheckSituation.html',{'user':user,'ProjectMarks':ProjectMarks,'p_status':p_status,'college':college})
    except:
        None
    return render_to_response('CheckSituation.html',{'user':user})


def Edition(request):
    user = request.user
    try:
        if request.POST['logout']:
            logout(request)
            return HttpResponseRedirect('/')
    except:
        None
    try:
        if request.POST['changed'] == '1':
            print 'op'
            type = request.POST['type']
            author = request.POST['author']
            time = request.POST['time']
            title = request.POST['title']
            content = request.POST['content']
            print content
            try:
                image = request.FILES['image']
                imagename = request.FILES['image'].name
            except:
                image = None
                imagename = None
            try:
                attachment = request.FILES['attachment']
                attachmentname = request.FILES['attachment'].name
            except:
                attachment =None
                attachmentname =None
            print imagename , attachmentname
            print type
            i = information()
            i.StoreInfo(type,author,time,title,content,image,attachment,imagename,attachmentname)
            return render_to_response('Edition.html',{'user':user})
    except:
        None
    return render_to_response('Edition.html',{'user':user})

def Download(request):
    table = 'download'
    i = information()
    downloadlist = i.Getinfo(table)
    downloadDict ={}
    for download in downloadlist:
        downloadDict[download[0]] = download[2]
    try:
        for download in downloadDict:
            if request.POST['download'] == download:
                for down in downloadlist:
                    if download == down[0]:
                        title = down[0]
                        author = down[1]
                        dates = down[2]
                        content = down[3]
                        imagepath = '../'+down[4]
                        attachment = '../'+down[5]
                        attachmentname = down[5].replace('static/download/attachment/','')
                        type = u'资源下载'
                        return  render_to_response('Content.html',{'type':type,'title':title,'author':author,'dates':dates,'content':content,'imagepath':imagepath,'attachment':attachment,'attachmentname':attachmentname})
                return render_to_response('Download.html',{'downloadDict':downloadDict})
    except:
        None
    try:
        if request.POST['search']:
            searchText = request.POST['searchText']
            downloadDict = {}
            for download in downloadlist:
                string = ''
                for n in download:
                    string = string + n
                if searchText in string:
                    downloadDict[download[0]] = download[2]
            return render_to_response('Download.html',{'downloadDict':downloadDict})
    except:
        None
    return render_to_response('Download.html',{'downloadDict':downloadDict})

def News(request):
    table = 'news'
    i = information()
    newslist = i.Getinfo(table)
    newsDict ={}
    for news in newslist:
        newsDict[news[0]] = news[2]
    try :
        for news in newsDict:
            if request.POST['news'] == news:
                for newss in newslist:
                    if news == newss[0]:
                        title = newss[0]
                        author = newss[1]
                        dates = newss[2]
                        content = newss[3]
                        if newss[4] is not None:
                            imagepath = '../'+newss[4]
                        else:
                            imagepath = None
                        if newss[5] is not None:
                            attachment = '../'+newss[5]
                            attachmentname = newss[5].replace('static/notice/attachment/','')
                        else:
                            attachment = None
                            attachmentname = None
                        type = u'新闻'
                        return render_to_response('Content.html',{'type':type,'title':title,'author':author,'dates':dates,'content':content,'imagepath':imagepath,'attachment':attachment,'attachmentname':attachmentname})
                return render_to_response('News.html',{'newsDict':newsDict})
    except:
        None
    try:
        if request.POST['search']:
            searchText = request.POST['searchText']
            newsDict = {}
            for news in newslist:
                string = ''
                for n in news:
                    string = string + n
                if searchText in string:
                    newsDict[news[0]] = news[2]
            return render_to_response('News.html',{'newsDict':newsDict})
    except:
        None
    return render_to_response('News.html',{'newsDict':newsDict})

def Notice(request):
    table = 'notice'
    i = information()
    noticelist = i.Getinfo(table)
    noticeDict ={}
    for notice in noticelist:
        noticeDict[notice[0]] = notice[2]
    try :
        for notice in noticeDict:
            if request.POST['notice'] == notice:
                for notices in noticelist:
                    if notice == notices[0]:
                        title = notices[0]
                        author = notices[1]
                        dates = notices[2]
                        content = notices[3]
                        imagepath = '../'+notices[4]
                        attachment = '../'+notices[5]
                        attachmentname = notices[5].replace('static/notice/attachment/','')
                        type = u'公告'
                        return render_to_response('Content.html',{'type':type,'title':title,'author':author,'dates':dates,'content':content,'imagepath':imagepath,'attachment':attachment,'attachmentname':attachmentname})
                return render_to_response('Notice.html',{'noticeDict':noticeDict})
    except:
        None
    try:
        if request.POST['search']:
            searchText = request.POST['searchText']
            noticeDict = {}
            for notice in noticelist:
                string = ''
                for n in notice:
                    string = string + n
                if searchText in string:
                    noticeDict[notice[0]] = notice[2]
            return render_to_response('Notice.html',{'noticeDict':noticeDict})
    except:
        None
    return render_to_response('Notice.html',{'noticeDict':noticeDict})

def Achievement(request):
    table = 'achievement'
    i = information()
    achievementlist = i.Getinfo(table)
    achievementDict ={}
    for achievement in achievementlist:
        achievementDict[achievement[0]] = achievement[2]
    try :
        for achievement in achievementDict:
            if request.POST['achievement'] == achievement:
                for achieve in achievementlist:
                    if achievement == achieve[0]:
                        title = achieve[0]
                        author = achieve[1]
                        dates = achieve[2]
                        content = achieve[3]
                        imagepath = '../'+achieve[4]
                        attachment = '../'+achieve[5]
                        attachmentname = achieve[5].replace('static/achievement/attachment/','')
                        type = u'成果展'
                        return render_to_response('Content.html',{'type':type,'title':title,'author':author,'dates':dates,'content':content,'imagepath':imagepath,'attachment':attachment,'attachmentname':attachmentname})
                return render_to_response('Achievement.html',{'achievementDict':achievementDict})
    except:
        None
    try:
        if request.POST['search']:
            searchText = request.POST['searchText']
            achievementDict = {}
            for achievement in achievementlist:
                string = ''
                for n in achievement:
                    string = string + n
                if searchText in string:
                    achievementDict[achievement[0]] = achievement[2]
            return render_to_response('Achievement.html',{'achievementDict':achievementDict})
    except:
        None
    return render_to_response('Achievement.html',{'achievementDict':achievementDict})

def Projectshow(request):
    table = 'projectshow'
    i = information()
    projectshowlist = i.Getinfo(table)
    projectshowDict ={}
    for projectshow in projectshowlist:
        projectshowDict[projectshow[0]] = projectshow[2]
    try :
        for projectshow in projectshowDict:
            if request.POST['projectshow'] == projectshow:
                for project in projectshowlist:
                    if projectshow == project[0]:
                        title = project[0]
                        author = project[1]
                        dates = project[2]
                        content = project[3]
                        imagepath = '../'+project[4]
                        attachment = '../'+ project[5]
                        attachmentname = project[5].replace('static/projectshow/attachment/','')
                        type = u'项目展示'
                        return render_to_response('Content.html',{'type':type,'title':title,'author':author,'dates':dates,'content':content,'imagepath':imagepath,'attachment':attachment,'attachmentname':attachmentname})
                return render_to_response('Projectshow.html',{'projectshowDict':projectshowDict})
    except:
        None
    try:
        if request.POST['search']:
            searchText = request.POST['searchText']
            projectshowDict = {}
            for project in projectshowlist:
                string = ''
                for n in project:
                    string = string + n
                if searchText in string:
                    projectshowDict[project[0]] = project[2]
            return render_to_response('Notice.html',{'projectshowDict':projectshowDict})
    except:
        None
    return render_to_response('Projectshow.html',{'projectshowDict':projectshowDict})

def Content(request):
    return render_to_response('Content.html')

def Leavemessage(request):
    user = request.user
    l = DllLeaveMessage()
    messagelist = l.GetMessage()
    try:
        if request.POST['leavemessage']:
            message = request.POST['searchText']
            l.storeMessage(user,message)
            messagelist = l.GetMessage()
            return render_to_response('LeaveMessage.html',{'messagelist':messagelist})
    except:
        None
    return render_to_response('LeaveMessage.html',{'messagelist':messagelist})

def ProjectManagement(request):
    user = request.user
    if not request.user.is_authenticated():
        return render_to_response('redirect.html',RenderContext(request))
    p = DllprojectManage()
    projectDict = p.GetprojectDict(user)
    try :
        for project in projectDict:
            if request.POST['projectname'] == project:
                ProjectContent = p.DllGetProjectContent(project)
                return render_to_response('projectRead.html',{'ProjectContent':ProjectContent,'project':project})
    except :
        None
    return render_to_response('ProjectManagement.html',{'projectDict':projectDict})

def projectRead(request):
    print 'well'
    user = request.user
    if not request.user.is_authenticated():
        return render_to_response('redirect.html',RenderContext(request))
    try:
        if request.POST['apply']:
            type ='apply'
            p_name =request.POST['apply']
            applyfile = request.FILES['fileField']
            applyfilename = request.FILES['fileField'].name
            projectManage = DllprojectManage()
            projectManage.dllReloadfile(p_name,type,applyfile,applyfilename)
            p = DllprojectManage()
            ProjectContent = p.DllGetProjectContent(p_name)
            return render_to_response('projectRead.html',{'ProjectContent':ProjectContent,'project':p_name})
    except:
        None
    try:
        if request.POST['apply']:
            type ='apply'
            p_name =request.POST['apply']
            applyfile = request.FILES['fileField']
            applyfilename = request.FILES['fileField'].name
            projectManage = DllprojectManage()
            projectManage.dllReloadfile(p_name,type,applyfile,applyfilename)
            p = DllprojectManage()
            ProjectContent = p.DllGetProjectContent(p_name)
            return render_to_response('projectRead.html',{'ProjectContent':ProjectContent,'project':p_name})
    except:
        None
    try:
        if request.POST['mid']:
            type ='mid'
            p_name =request.POST['mid']
            midfile = request.FILES['fileField']
            midfilename = request.FILES['fileField'].name
            projectManage = DllprojectManage()
            projectManage.dllReloadfile(p_name,type,midfile,midfilename)
            p = DllprojectManage()
            ProjectContent = p.DllGetProjectContent(p_name)
            return render_to_response('projectRead.html',{'ProjectContent':ProjectContent,'project':p_name})
    except:
        None
    try:
        if request.POST['end']:
            type ='end'
            p_name =request.POST['end']
            endfile = request.FILES['fileField']
            endfilename = request.FILES['fileField'].name
            projectManage = DllprojectManage()
            projectManage.dllReloadfile(p_name,type,endfile,endfilename)
            p = DllprojectManage()
            ProjectContent = p.DllGetProjectContent(p_name)
            return render_to_response('projectRead.html',{'ProjectContent':ProjectContent,'project':p_name})
    except:
        None
    return render_to_response('projectRead.html')


class ProjectAnalysis:
    ProjectAnalyselist = None
    def __init__(self,ProjectAnalyselist):
        self.__class__.ProjectAnalyselist = ProjectAnalyselist
def ProjectAnalyse(request):
    print ProjectAnalysis.ProjectAnalyselist
    user = request.user
    if not request.user.is_authenticated():
        return render_to_response('redirect.html',RenderContext(request))
    try :
        if request.POST['look']:
            college = request.POST['college']
            pro_status = request.POST['p_status']
            projectAnalysis  = DllProjectAnalysis()
            projectlist =projectAnalysis.GetProject(college,pro_status)
            ProjectAnalysis(projectlist)
            return render_to_response('ProjectAnalyse.html',{'projectlist':projectlist})
    except:
        None
    try :
        if request.POST['search']:
            searchText = request.POST['searchfield']
            pa = DllProjectAnalysis()
            projectlist =pa.GetSearchProject(searchText)
            ProjectAnalysis(projectlist)
            return render_to_response('ProjectAnalyse.html',{'projectlist':projectlist})
    except:
        None

    try :
        if request.POST['project']:
            projectlist = ProjectAnalysis.ProjectAnalyselist
            for project in projectlist:
                if request.POST['project'] == project[0]:
                    print project[0]
                    PA = DllProjectAnalysis()
                    projectInfo = PA.GetProjectInfo(project[0])
                    p_name = projectInfo[0]
                    college = projectInfo[1]
                    try :
                        nameSimilar = PA.ProjectNameSimilar(p_name,college)
                    except :
                        nameSimilar ={}
                    try:
                        applySimilar = PA.ApplySimilar(p_name,college)
                        print 'applySimilar',applySimilar
                    except:
                        applySimilar ={}
                    try:
                        midSimilar = PA.MidSimilar(p_name,college)
                        print 'midSimilar',midSimilar
                    except:
                        midSimilar ={}
                    try:
                        endSimilar = PA.EndSimilar(p_name,college)
                        print 'endSimilar',endSimilar
                    except:
                        endSimilar ={}
                    return render_to_response('OneAnalyse.html',{'projectInfo':projectInfo,'nameSimiar':nameSimilar,'applySimilar':applySimilar,'midSimilar':midSimilar,'endSimilar':endSimilar})
    except:
        None
    return render_to_response('ProjectAnalyse.html')

def OneAnalyse(request):
    if not request.user.is_authenticated():
        return render_to_response('redirect.html',RenderContext(request))
    return render_to_response('OneAnalyse.html')