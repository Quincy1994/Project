#coding:utf-8
__author__ = 'root'
from chenge.models import *
from chenge.PDFparser import *
from chenge.MailSend import MailSend
from chenge.cosmini import *
class LoginFactory:
    def createloginInsstorce(self,usertype):
        user=Users()
        if usertype=='1':
            user=Student()
        if usertype=='2':
            user=Teacher()
        if usertype=='3':
            user=Adminstrator()
        return user

class DllLogin:
    def UserLogin(self,usertype,id,password):
        loginfactory=LoginFactory()
        user=loginfactory.createloginInsstorce(usertype=usertype)
        return user.login(id,password)

class DllRegister:
    def UserRegister(self,usertype,id,password,name,college,grade,title,phone,mail):
        user =Users()
        if usertype == '1':
            user=Student()
            return user.register(id,password,name,college,grade,phone,mail)
        elif usertype == '2':
            user =Teacher()
            return user.register(id,password,name,college,title,phone,mail)
class DllprojectApply:
    def ProjectApply(self,projectDict):
        user =Student()
        return user.apply(projectDict)

class DLLprojectPDF:
    def projectPDFcheck(self,PDF,PDFname):
         pdf=PDFpraser()
         pdfname = pdf.PDFload(PDF,PDFname)
         pdf.Pdfparser(pdfname)
         checklist = pdf.countwordcheck()
         del pdf
         return checklist

class DLLAdmMailSend:
     def Mail(self,sender,receivers,college,title,content,filename,student,teacher,file):
         if receivers is not None:
             receiverlist=receivers
         else:
             receiverlist = None
         d = Dal()
         mail_list = d.getMail(receiverlist,college,student,teacher)
         Mailsender = d.getSender(sender)
         m = MailSend()
         try:
             if filename is not None:
                 print 'ttt',filename
                 file_name=m.mail_fileLoad(file,filename)
                 print 'kkkk',file_name
                 m.Sendwithfile(Mailsender,mail_list=mail_list,content=content,file_name=file_name,mail_title=title)
                 return True
             else:
                 m.send_mailText(Mailsender,mail_list,content,title)
                 return True
         except:
             return False

         # if mail_title == u'项目申报审核评分':

class checkproject:
   def MailFor_check(self,teachers,college,status):
       pc=ProjectCheck()
       pc.check(teachers=teachers,college=college,status=status)
       return True

   def isCheck(self,title,teachers,college):
        statuslist =[u'项目申报审核评分',u'项目中期审核评分',u'项目结项审核评分']
        if title in statuslist:
           if title == statuslist[0]:
               status = u'申报待审核'
           elif title == statuslist[1]:
               status = u'中期待审核'
           else:
               status = u'结项待审核'
           return self.MailFor_check(teachers,college,status)
        else:
            return False

   def TeachGetProject(self,pro_status,t_id):
        d=Dal()
        t_name =d.getTeachername(t_id)
        ProjectDict=d.getprojectToTeacher(pro_status,teacher=t_name)
        return ProjectDict

   def TeachGetProjectMark(self,projectlist,t_id):
       d=Dal()
       t_name = d.getTeachername(t_id)
       ProjectMarks = d.getMarksToTeacher(projectlist,t_name)
       return ProjectMarks

   def BLLStoreApply(self,p_name,t_name,points,advice):
       pro_status=u'申报待审核'
       d =Dal()
       d.StoreCheckPoint(p_name=p_name,t_name=t_name,points=points,advice=advice,pro_status=pro_status)
       return True

   def BLLStoreMid(self,p_name,t_name,points,advice):
       pro_status = u'中期待审核'
       d =Dal()
       d.StoreCheckPoint(p_name=p_name,t_name=t_name,points=points,advice=advice,pro_status=pro_status)
       return True

   def BLLStoreEnd(self,p_name,t_name,points,advice):
       pro_status = u'结项待审核'
       d =Dal()
       d.StoreCheckPoint(p_name=p_name,t_name=t_name,points=points,advice=advice,pro_status=pro_status)
       return True

   def SendAdvice(self,t_name,advice,p_name):
      d = Dal()
      mail_list=[]
      mail = d.projectToStuentMail(p_name)
      mail_list.append(str(mail))
      sender=['18819423747',u'创新创业小助手<18819423747@163.com>','xie5321927']
      title = u'你好,我是创新创业小助手'
      # title = 'ok'
      content = u'您好,您申报的学生创新创业项目,名为<<%s>>, 经评委的审核, 其中评委老师%s,对您的项目提出以下宝贵的意见:\n  %s'%(p_name,t_name,advice)
      # content =advice
      m = MailSend()
      m.send_mailText(sender, mail_list, content, title)

   def DllCheckover(self,ProjectMarks,t_name):
        d= Dal()
        for project in ProjectMarks:
            if ProjectMarks[project] > 0:
                d.checkover(project,t_name)

class Edtioninfo:
    def Teacherinfo(self,t_id):
        d =Dal()
        TeacherDict = d.getTeacherInfo(t_id)
        return TeacherDict
    def DllTeacherinfo(self,teacherinfo):
        d = Dal()
        d.changeTeacherInfo(teacherinfo)
    def Studentinfo(self,s_id):
        d =Dal()
        TeacherDict = d.getStudentInfo(s_id)
        return TeacherDict
    def DllStudentinfo(self,studentinfo):
        d = Dal()
        d.changeStudentInfo(studentinfo)


class AdminForCheck:
    def getprojects(self,college,p_status):
        d = Dal()
        projects = d.checkprojectAvgpoint(college,p_status)
        return projects

    def CheckSubmit(self,points,projectstatus,p_name):
        d = Dal()
        d.storePoints(p_name,points,projectstatus)
        d.changeStatus(p_name,projectstatus)
        d.CheckDelete(p_name)

    def delete(self,p_name):
        d = Dal()
        d.CheckDelete(p_name)
        d.Deleteproject(p_name)


class information:
    def StoreInfo(self,type,author,time,title,content,image,attachment,imagename,attachmentname):
        table = None
        if type == u'公告':
            table = 'notice'
        elif type == u'新闻':
            table = 'news'
        elif type == u'项目展示':
            table = 'projectshow'
        elif type == u'成果展':
            table = 'achievement'
        elif type == u'资源下载':
            table = 'download'
        print table
        if image is not None:
            imagepath = self.Imageload(table,image,imagename)
            print imagepath
        else:
            imagepath = None
        if attachment is not None :
            attachmentpath = self.Attachmentload(table,attachment,attachmentname)
        else:
            attachmentpath = None
        d = Dal()
        d.storeInformation(table,author,time,title,content,imagepath,attachmentpath)

    def Imageload(self,table,image,imagename):
        print table
        if not os.path.exists('static/%s/Image/'%(table)):
            os.mkdir('static/%s/Image/'%(table))
        print 'static/%s/Image/'%(table)+imagename
        with open('static/%s/Image/'%(table)+imagename,'wb+') as destination:
            for chunk in image.chunks():
                destination.write(chunk)
        return 'static/%s/Image/'%(table)+imagename

    def Attachmentload(self,table,attachment,attachmentname):
        if not os.path.exists('static/%s/attachment/'%(table)):
            os.mkdir('static/%s/attachment/'%(table))
        with open('static/%s/attachment/'%(table)+attachmentname,'wb+') as destination:
            for chunk in attachment.chunks():
                destination.write(chunk)
        return 'static/%s/attachment/'%(table)+attachmentname

    def Getinfo(self,table):
        d = Dal()
        noticelist = d.GetInfoList(table)
        return noticelist

import time
ISOTIMEFORMAT='%Y-%m-%d %X'
class DllLeaveMessage:
    def storeMessage(self,user,message):
        d = Dal()
        name = d.GetName(user)
        dates =time.strftime(ISOTIMEFORMAT,time.localtime(time.time()+ 8* 60* 60))
        d.StoreLeaveMessage(user,dates,name,message)
    def GetMessage(self):
        d =Dal()
        messagelist = d.GetLeaveMessage()
        return messagelist

class DllprojectManage:
    def GetprojectDict(self,s_id):
        d = Dal()
        ProjectDict = d.Getproject(s_id)
        return ProjectDict
    def DllGetProjectContent(self,p_name):
        d = Dal()
        ProjectContent = d.GetProjectContent(p_name)
        return ProjectContent
    def dllReloadfile(self,p_name,type,file ,filename):
        ProjectContent = self.DllGetProjectContent(p_name)
        print ProjectContent
        fileType=None
        filepath =None
        print type
        if type == 'apply':
            if ProjectContent[4] is not None:
                filepath = ProjectContent[4]
            fileType = 'filepath'
        elif type == 'mid':
            if ProjectContent[5] is not None:
                filepath = ProjectContent[5]
            fileType ='midfile'
        elif type == 'end':
            if ProjectContent[6] is not None:
                filepath = ProjectContent[6]
            fileType ='endfile'
        if filepath is not None :
            if os.path.exists(filepath)  :
                os.remove(filepath)
        filepath = self.LoadFile(file,filename,type)
        d = Dal()
        d.StoreFilePath(fileType,filepath,p_name)

    def LoadFile(self,file,filename,type):
        fileType = None
        if type == 'apply':
            fileType = u'申报待审核'
        elif type == 'mid':
            fileType = u'中期待审核'
        elif type == 'end':
            fileType = u'结项待审核'
        print 'load',fileType
        with open('static/upload/%s/'%(fileType)+filename,'wb+') as destination:
            for chunk in file.chunks():
                destination.write(chunk)
        return 'static/upload/%s/'%(fileType)+filename

class DllProjectAnalysis:
    def GetProject(self,college,pro_status):
        d = Dal()
        Projectlist = d.AnalyseGetProject(college,pro_status)
        return Projectlist

    def GetProjectInfo(self,p_name):
        d = Dal()
        ProjectInfo = d.AnalyseGetProjectInfo(p_name)
        return ProjectInfo

    def ProjectNameSimilar(self,p_name,college):
        d = Dal()
        projectlist = d.AnalyseGetProjectName(college)
        projectNamelist =[]
        for project in projectlist:
            projectNamelist.append(project[0])
        nameSimiarDict = {}
        ta =TextAnalyse()
        for projectName in projectNamelist:
            if projectName == p_name:
                continue
            similar = ta.similay(p_name,projectName)
            if similar > 0.5 :
                nameSimiarDict[projectName] = similar
        return nameSimiarDict

    def ApplySimilar(self,p_name,college):
        d = Dal()
        applyFilepath = d.AnalyseGetProjectApplyFile(p_name,college)
        if applyFilepath == None :
            return None
        pdf = PDFpraser()
        applyData = pdf.getPDFdata(applyFilepath)
        projectApplylist = d.AnalyseGetProjectApplyFilelist(college)
        applySimilarDict ={}
        ta =TextAnalyse()
        for project in projectApplylist :
            if project == p_name :
                continue
            if projectApplylist[project] == None :
                continue
            data = pdf.getPDFdata(projectApplylist[project])
            similar =ta.comsini(applyData,data)
            if similar > 0.5 :
                applySimilarDict[project] = similar
        return applySimilarDict

    def MidSimilar(self,p_name,college):
        d = Dal()
        MidFilepath = d.AnalyseGetProjectMidFile(p_name,college)
        if MidFilepath == None :
            return None
        pdf = PDFpraser()
        MidData = pdf.getPDFdata(MidFilepath)
        projectMidlist = d.AnalyseGetProjectMidFilelist(college)
        MidSimilarDict ={}
        ta =TextAnalyse()
        for project in projectMidlist :
            if project == p_name :
                continue
            if projectMidlist[project] == None :
                continue
            data = pdf.getPDFdata(projectMidlist[project])
            similar =ta.comsini(MidData,data)
            if similar > 0.5 :
                MidSimilarDict[project] = similar
        return MidSimilarDict

    def EndSimilar(self,p_name,college):
        d = Dal()
        endFilepath = d.AnalyseGetProjectEndFile(p_name,college)
        if endFilepath == None :
            return None
        pdf = PDFpraser()
        endData = pdf.getPDFdata(endFilepath)
        projectEndlist = d.AnalyseGetProjectEndFilelist(college)
        endSimilarDict ={}
        ta =TextAnalyse()
        for project in projectEndlist :
            if project == p_name :
                continue
            if projectEndlist[project] == None :
                continue
            data = pdf.getPDFdata(projectEndlist[project])
            similar =ta.comsini(endData,data)
            if similar > 0.5 :
                endSimilarDict[project] = similar
        return endSimilarDict

    def GetSearchProject(self,searchText):
        d =Dal()
        Projectlist = []
        projects = d.AnalyseGetSearchProject()
        for project in projects:
            if searchText in project[0]:
                Projectlist.append(project)
        return Projectlist

class MainPage:
    def GetContent(self):
        d =Dal()
        noticelist = d.GetNewNotice()
        newslist = d.GetNewNews()
        return noticelist,newslist