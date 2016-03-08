#coding:utf-8
import os
from DAL import *
os.environ.setdefault("DJANGO_SETTINGS_MODULE","untitled2.settings")


from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save


class Userprofile(models.Model):
    user = models.OneToOneField(User, primary_key=True)
    file = models.FileField(upload_to='./data/')

    def __unicode__(self):
        return u"%s" % self.user.username,self.file.name

    def getname(self):
        return self.user.username


def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Userprofile.objects.create(user=instance)

post_save.connect(create_user_profile, sender=User)

def handle_uploaded_file(file,filename,college,sid,filedir):
    if not os.path.exists('static/upload/'):
        os.mkdir('static/upload/')
    if not os.path.exists('static/upload/'+college+'/'):
        os.mkdir('static/upload/'+college+'/')
    if not os.path.exists(('static/upload/'+college+'/'+filedir)):
        os.mkdir('static/upload/'+college+'/'+filedir+'')
    with open(('static/upload/'+college+'/'+filedir+'')+filename,'wb+') as destination:
        for chunk in file.chunks():
            destination.write(chunk)
    filepath = 'static/upload/'+college+'/'+filedir+filename
    return filepath


class Users:
    id = None
    password = None
    def login(self,ID,password):
        return
    def register(self,ID,password,name,college,grade,phone,mail):
        return

class Student(Users):
    name = None
    college = None
    grade = None
    mail  =None
    def login(self,ID,password):
        self.id=ID
        self.password=password
        d=Dal()
        return  d.LoginAccess('student',self.id,self.password)
    def register(self,ID,password,name,college,grade,phone,mail):
        self.id =ID
        self.password = password
        self.name =name
        self.college =college
        self.grade =grade
        self.phone =phone
        self.mail =mail
        d = Dal()
        return d.RegisterAccess(tablename='student',ID=self.id , password=self.password,name=self.name,
                                college=self.college,grade=self.grade,phone=self.phone,mail=self.mail)
    def apply(self,projectDict):
        d = Dal()
        return d.projectApplyAccess(projectDict)

class Teacher(Users):
    name = None
    college = None
    title = None
    mail  =None
    def login(self,ID,password):
        self.id=ID
        self.password=password
        d=Dal()
        return  d.LoginAccess('teacher',self.id,self.password)
    def register(self,ID,password,name,college,title,phone,mail):
        self.id =ID
        self.password = password
        self.name =name
        self.college =college
        self.grade =title
        self.phone =phone
        self.mail =mail
        d = Dal()
        return d.RegisterAccess(tablename='student',ID=self.id , password=self.password,name=self.name,
                                college=self.college,grade=self.title,phone=self.phone,mail=self.mail)


class Adminstrator(Users):
    def login(self,ID,password):
        self.id=ID
        self.password=password
        d=Dal()
        return  d.LoginAccess('adminstrator',self.id,self.password)

class ProjectCheck:
    def check(self,teachers,college,status):
        d =Dal()
        ProjectDict=d.getProject(college,status)

        return d.Projectcheckadd(teachers,college,status,ProjectDict)

