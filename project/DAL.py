#coding:utf-8
__author__ = 'root'
import MySQLdb
connhost='127.0.0.1'
user='root'
passwd='5510358'
db='project'
charset='utf8'

class Dal:
    def LoginAccess(self,tablename,id,pwd):
        conn = MySQLdb.connect(host=connhost,user=user,passwd=passwd,db=db,charset=charset)
        conn.select_db(db)
        cursor = conn.cursor()
        constring = None
        if tablename == 'student':
            constring = "select*from "+str(tablename) +" where s_id='"+str(id)+ "' and pwd='"+str(pwd)+"';"
        elif tablename == 'teacher':
            constring = "select*from "+str(tablename) +" where t_id='"+str(id)+ "' and pwd='"+str(pwd)+"';"
        elif tablename == 'adminstrator':
            constring = "select*from "+str(tablename) +" where a_name='"+str(id)+ "' and pwd='"+str(pwd)+"';"
        # result=cursor.execute("select*from %s where s_id=%s and pwd=%s;"%(tablename,id,pwd))
        result = cursor.execute(constring)
        cursor.close()
        conn.close()
        if result==0:
            return False
        else:
            return True

    def RegisterAccess(self,tablename,ID,password,name,college,grade,phone,mail):
        conn = MySQLdb.connect(host=connhost,user=user,passwd=passwd,db=db,charset=charset)
        conn.select_db(db)
        cursor = conn.cursor()
        constring =None
        if tablename =='student':
            constring = "insert into student(s_id,pwd,s_name,college,grade,mail,phone)values('"+str(ID)+"','"+str(password)+"','"+name+"','"+college+"','"+grade+"','"+str(mail)+"','"+str(phone)+"');"
        elif tablename == 'teacher':
            constring = "insert into teacher(t_id,pwd,t_name,college,title,mail,phone)values('"+str(ID)+"','"+str(password)+"','"+name+"','"+college+"','"+grade+"','"+str(mail)+"','"+str(phone)+"');"
        result = cursor.execute(constring)
        conn.commit()
        cursor.close()
        conn.close()
        print result
        if result==0:
            return False
        else:
            return True

    def projectApplyAccess(self,projectDict):
        conn = MySQLdb.connect(host=connhost,user=user,passwd=passwd,db=db,charset=charset)
        conn.select_db(db)
        cursor = conn.cursor()
        constring ="insert into projection(p_id,p_name,college,p_year,p_type,p_class,duration,p_charge,c_college,c_id,c_grade,p_sname1,s1_college,s1_id,s1_grade,p_sname2,s2_college,s2_id,s2_grade,p_sname3,s3_college,s3_id,s3_grade,p_sname4,s4_college,s4_id,s4_grade,p_teacher1,t1_college,t1_id,t1_grade,p_teacher2,t2_college,t2_id,t2_grade,p_key1,p_key2,p_key3,p_info,filepath,pro_status,midfile,endfile)"
        constring = constring+"values('%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','','')"%(projectDict['project_id'],projectDict['project_name'],projectDict['project_department'],projectDict['batch'],projectDict['project_type'],projectDict['project_variety'],projectDict['project_year'],projectDict['s1_name'],projectDict['s1_department'],projectDict['s1_id'],projectDict['s1_grade'],projectDict['s2_name'],projectDict['s2_department'],projectDict['s2_id'],projectDict['s2_grade'],projectDict['s3_name'],projectDict['s3_department'],projectDict['s3_id'],projectDict['s3_grade'],projectDict['s4_name'],projectDict['s4_department'],projectDict['s4_id'],projectDict['s4_grade'],projectDict['s5_name'],projectDict['s5_department'],projectDict['s5_id'],projectDict['s5_grade'],projectDict['t1_name'],projectDict['t1_department'],projectDict['t1_id'],projectDict['t1_title'],projectDict['t2_name'],projectDict['t2_department'],projectDict['t2_id'],projectDict['t2_title'],projectDict['project_key1'],projectDict['project_key2'],projectDict['project_key3'],projectDict['project_info'],projectDict['filepath'],projectDict['pro_status'])
        result = cursor.execute(constring)
        conn.commit()
        cursor.close()
        conn.close()
        if result==0:
            return False
        else:
            return True

    def getMail(self,receiverlist,college,student,teacher):
        mail_list = []
        if receiverlist is not None:
            # tablename=['student','teacher','adminstrator']
            conn = MySQLdb.connect(host=connhost,user=user,passwd=passwd,db=db,charset=charset)
            conn.select_db(db)
            cursor = conn.cursor()
            constring = None
            for receiver in receiverlist:
                constring = "select mail from student where s_name='%s';"%(receiver)
                print constring
                n =cursor.execute(constring)
                if n >= 1:
                    result = cursor.fetchall()
                    for r in result:
                        mail_list.append(r[0])

                constring = "select mail from teacher where t_name='%s';"%(receiver)
                n =cursor.execute(constring)
                if n >= 1:
                    result = cursor.fetchall()
                    for r in result:
                        mail_list.append(r[0])

                constring = "select mail from adminstrator where a_name='%s';"%(receiver)
                cursor.execute(constring)
                n =cursor.execute(constring)
                if n >= 1:
                    result = cursor.fetchall()
                    for r in result:
                        mail_list.append(r[0])
        if college is not None :
            if student is not None:
                constring = "select mail from student where college='%s';"%(college)
                cursor.execute(constring)
                n =cursor.execute(constring)
                if n >= 1:
                    result = cursor.fetchall()
                    for r in result:
                        mail_list.append(r[0])
            if teacher is not None:
                constring = "select mail from teacher where college='%s';"%(college)
                cursor.execute(constring)
                n =cursor.execute(constring)
                if n >= 1:
                    result = cursor.fetchall()
                    for r in result:
                        mail_list.append(r[0])
        cursor.close()
        conn.close()
        maillist =[]
        for mail in mail_list:
            maillist.append(str(mail))
        return maillist
    def getSender(self,sender):
        senderDict ={}
        conn = MySQLdb.connect(host=connhost,user=user,passwd=passwd,db=db,charset=charset)
        conn.select_db(db)
        cursor = conn.cursor()
        constring = "select mail,mailpwd from adminstrator where a_name='%s';"%(sender)
        cursor.execute(constring)
        result = cursor.fetchone()
        group= str(result[0]).split('@')
        senderMail = group[0] + "<"+str(result[0])+">.com"
        mailsender=[]
        mailsender.append(str(group[0]))
        mailsender.append(senderMail)
        mailsender.append(str(result[1]))
        return mailsender

    def getProject(self,college,status):
        conn = MySQLdb.connect(host=connhost,user=user,passwd=passwd,db=db,charset=charset)
        conn.select_db(db)
        cursor = conn.cursor()
        constring = ''
        if status == u'申报待审核':
            constring = "select p_name,filepath from projection where college='%s' and pro_status='%s';"%(college,status)
        elif status == u'中期待审核':
            constring = "select p_name,midfile from projection where college='%s' and pro_status='%s';"%(college,status)
        elif status == u'结项待审核':
            constring = "select p_name,endfile from projection where college='%s' and pro_status='%s';"%(college,status)
        cursor.execute(constring)
        result = cursor.fetchall()
        ProjectDict={}
        for r in result:
            projectname = r[0]
            projectpath = r[1]
            ProjectDict[projectname]=projectpath
        cursor.close()
        conn.close()
        return ProjectDict
    def Projectcheckadd(self,teachers,college,status,ProjectDict):
        conn = MySQLdb.connect(host=connhost,user=user,passwd=passwd,db=db,charset=charset)
        conn.select_db(db)
        cursor = conn.cursor()
        for teacher in teachers:
            for project in ProjectDict.keys():
                constring = "insert into checkproject(p_name,t_name,points,file_path,pro_status,advice,tag,college) values('%s','%s',0,'%s','%s','','F','%s')"%(project,teacher,ProjectDict[project],status,college)
                cursor.execute(constring)
        conn.commit()
        cursor.close()
        conn.close()
        return True

    def getprojectToTeacher(self,pro_status,teacher):
        conn = MySQLdb.connect(host=connhost,user=user,passwd=passwd,db=db,charset=charset)
        conn.select_db(db)
        cursor = conn.cursor()
        constring = "select p_name , file_path from checkproject where pro_status = '%s'and t_name='%s' and tag ='F';"%(pro_status,teacher)
        cursor.execute(constring)
        result = cursor.fetchall()
        ProjectDict={}
        for r in result:
            projectname = r[0]
            projectpath = r[1]
            ProjectDict[projectname]=projectpath
        cursor.close()
        conn.close()
        return ProjectDict

    def getTeachername(self,t_id):
        conn = MySQLdb.connect(host=connhost,user=user,passwd=passwd,db=db,charset=charset)
        conn.select_db(db)
        cursor = conn.cursor()
        constring = "select t_name from teacher where t_id='%s';"%(t_id)
        cursor.execute(constring)
        result = cursor.fetchone()
        teachername =result[0]
        return teachername

    def getstudentname(self,s_id):
        conn = MySQLdb.connect(host=connhost,user=user,passwd=passwd,db=db,charset=charset)
        conn.select_db(db)
        cursor = conn.cursor()
        constring = "select s_name from student where s_id='%s';"%(s_id)
        cursor.execute(constring)
        result = cursor.fetchone()
        studentname =result[0]
        return studentname


    def getMarksToTeacher(self,projectlist,t_name):
        conn = MySQLdb.connect(host=connhost,user=user,passwd=passwd,db=db,charset=charset)
        conn.select_db(db)
        cursor = conn.cursor()
        projectMarkDict={}
        for i in range(0,projectlist.__len__(),1):
            p_name = projectlist[i]
            constring = "select points from checkproject where t_name='%s' and p_name='%s';"%(t_name,p_name)
            cursor.execute(constring)
            result = cursor.fetchone()
            point =result[0]
            projectMarkDict[p_name] = point
        cursor.close()
        conn.close()
        return projectMarkDict

    def StoreCheckPoint(self,p_name,t_name,points,advice,pro_status):
        conn = MySQLdb.connect(host=connhost,user=user,passwd=passwd,db=db,charset=charset)
        conn.select_db(db)
        cursor = conn.cursor()
        constring = "update checkproject set points = %s,advice='%s' where p_name='%s' and t_name='%s' and pro_status='%s';"%(points,advice,p_name,t_name,pro_status)
        print constring
        cursor.execute(constring)
        conn.commit()
        cursor.close()
        conn.close()


    def projectToStuentMail(self,p_name):
        conn = MySQLdb.connect(host=connhost,user=user,passwd=passwd,db=db,charset=charset)
        conn.select_db(db)
        cursor = conn.cursor()
        constring = "select mail from student,projection where p_name='%s' and student.s_id = projection.c_id;"%(p_name)
        cursor.execute(constring)
        result = cursor.fetchone()
        mail =result[0]
        return mail

    def checkover(self,p_name,t_name):
        conn = MySQLdb.connect(host=connhost,user=user,passwd=passwd,db=db,charset=charset)
        conn.select_db(db)
        cursor = conn.cursor()
        constring = "update checkproject set tag = 'T' where p_name='%s' and t_name='%s'; "%(p_name,t_name)
        cursor.execute(constring)
        conn.commit()
        cursor.close()
        conn.close()

    def getTeacherInfo(self,t_id):
        conn = MySQLdb.connect(host=connhost,user=user,passwd=passwd,db=db,charset=charset)
        conn.select_db(db)
        cursor = conn.cursor()
        constring = "select t_id,pwd,t_name,college,title,mail,phone from teacher where t_id ='%s';"%(t_id)
        cursor.execute(constring)
        result = cursor.fetchone()
        teacherDict={}
        teacherDict['t_id']=result[0]
        teacherDict['pwd']=result[1]
        teacherDict['t_name']=result[2]
        teacherDict['college'] =result[3]
        teacherDict['title'] = result[4]
        teacherDict['mail'] = result[5]
        teacherDict['phone'] = result[6]
        return teacherDict

    def changeTeacherInfo(self,teacherDict):
        conn = MySQLdb.connect(host=connhost,user=user,passwd=passwd,db=db,charset=charset)
        conn.select_db(db)
        cursor = conn.cursor()
        t_id =''
        pwd=''
        t_name = ''
        college =''
        title = ''
        mail = ''
        phone = ''
        t_id =t_id+u'%s'%teacherDict['t_id']
        pwd = pwd +u'%s'%teacherDict['pwd']
        t_name =t_name +u'%s'%teacherDict['t_name']
        college =college +u'%s'%teacherDict['college']
        title =title +u'%s'%teacherDict['title']
        mail =mail +u'%s'%teacherDict['mail']
        phone =phone +u'%s'%teacherDict['phone']
        constring = "update teacher set pwd='%s',t_name='%s',college='%s',title='%s',mail='%s',phone ='%s' where t_id='%s';"%(pwd,t_name,college,title,mail,phone,t_id)
        print constring
        cursor.execute(constring)
        conn.commit()
        cursor.close()
        conn.close()

    def getStudentInfo(self,s_id):
        conn = MySQLdb.connect(host=connhost,user=user,passwd=passwd,db=db,charset=charset)
        conn.select_db(db)
        cursor = conn.cursor()
        constring = "select s_id,pwd,s_name,college,grade,mail,phone from student where s_id ='%s';"%(s_id)
        cursor.execute(constring)
        result = cursor.fetchone()
        studentDict={}
        studentDict['s_id']=result[0]
        studentDict['pwd']=result[1]
        studentDict['s_name']=result[2]
        studentDict['college'] =result[3]
        studentDict['grade'] = result[4]
        studentDict['mail'] = result[5]
        studentDict['phone'] = result[6]
        return studentDict

    def changeStudentInfo(self,studentDict):
        conn = MySQLdb.connect(host=connhost,user=user,passwd=passwd,db=db,charset=charset)
        conn.select_db(db)
        cursor = conn.cursor()
        s_id =''
        pwd=''
        s_name = ''
        college =''
        grade = ''
        mail = ''
        phone = ''
        s_id =s_id+u'%s'%studentDict['s_id']
        pwd = pwd +u'%s'%studentDict['pwd']
        s_name =s_name +u'%s'%studentDict['s_name']
        college =college +u'%s'%studentDict['college']
        grade =grade +u'%s'%studentDict['grade']
        mail =mail +u'%s'%studentDict['mail']
        phone =phone +u'%s'%studentDict['phone']
        constring = "update student set pwd='%s',s_name='%s',college='%s',grade='%s',mail='%s',phone ='%s' where s_id='%s';"%(pwd,s_name,college,grade,mail,phone,s_id)
        cursor.execute(constring)
        conn.commit()
        cursor.close()
        conn.close()

    def checkprojectAvgpoint(self,college,p_status):
        conn = MySQLdb.connect(host=connhost,user=user,passwd=passwd,db=db,charset=charset)
        conn.select_db(db)
        cursor = conn.cursor()
        projectMarks={}
        constring ="SELECT p_name,AVG(points) FROM checkproject where tag='T' and college='%s' and pro_status ='%s' GROUP BY p_name order by AVG(points) desc ;"%(college,p_status)
        cursor.execute(constring)
        result = cursor.fetchall()
        for r in result :
           projectMarks[r[0]]=r[1]
        return projectMarks

    def storePoints(self,p_name,points,p_status):
        conn = MySQLdb.connect(host=connhost,user=user,passwd=passwd,db=db,charset=charset)
        conn.select_db(db)
        cursor = conn.cursor()
        print 'nice'
        print p_name
        points = int(points)
        points = str(points)
        print points
        print p_status
        if p_status == u'申报通过':
            pro_status=u'申报待审核'
            constring = "update projection set applypoints=%s where p_name = '%s' and pro_status='%s';"%(points,p_name,pro_status)
            print constring
        elif p_status == u'中期通过':
            pro_status=u'中期待审核'
            constring = "update projection set midpoints=%s where p_name = '%s' and pro_status='%s';"%(points,p_name,pro_status)
        elif p_status == u'结项通过':
            pro_status=u'中期待审核'
            constring = "update projection set endpoints=%s where p_name = '%s' and pro_status='%s';"%(points,p_name,pro_status)
        else:
            constring = None
        cursor.execute(constring)
        conn.commit()
        cursor.close()
        conn.close()

    def changeStatus(self,p_name,p_status):
        conn = MySQLdb.connect(host=connhost,user=user,passwd=passwd,db=db,charset=charset)
        conn.select_db(db)
        cursor = conn.cursor()
        if p_status == u'申报通过':
            pro_status=u'申报待审核'
            constring = "update projection set pro_status='%s' where p_name = '%s'and pro_status='%s';"%(p_status,p_name,pro_status)
            print constring
        elif p_status == u'中期通过':
            pro_status=u'中期待审核'
            constring = "update projection set pro_status='%s' where p_name = '%s' and pro_status='%s';"%(p_status,p_name,pro_status)
        elif p_status == u'结项通过':
            pro_status=u'中期待审核'
            constring = "update projection set pro_status='%s' where p_name = '%s' and pro_status='%s';"%(p_status,p_name,pro_status)
        else:
            constring = None
        cursor.execute(constring)
        conn.commit()
        cursor.close()
        conn.close()

    def CheckDelete(self,p_name):
        conn = MySQLdb.connect(host=connhost,user=user,passwd=passwd,db=db,charset=charset)
        conn.select_db(db)
        cursor = conn.cursor()
        constring = "delete from checkproject where p_name ='%s';"%(p_name)
        cursor.execute(constring)
        conn.commit()
        cursor.close()
        conn.close()

    def Deleteproject(self,p_name):
        self.CheckDelete(p_name)
        conn = MySQLdb.connect(host=connhost,user=user,passwd=passwd,db=db,charset=charset)
        conn.select_db(db)
        cursor = conn.cursor()
        constring = "delete from projection where p_name ='%s';"%(p_name)
        cursor.execute(constring)
        conn.commit()
        cursor.close()
        conn.close()

    def storeInformation(self,table,author,time,title,content,imagepath,attachmentpath):
        conn = MySQLdb.connect(host=connhost,user=user,passwd=passwd,db=db,charset=charset)
        conn.select_db(db)
        cursor = conn.cursor()
        constring = "insert into %s(title,author,dates,content,imagepath,attachment) values('%s','%s','%s','%s','%s','%s');"%(table,title,author,time,content,imagepath,attachmentpath)
        print constring
        cursor.execute(constring)
        conn.commit()
        cursor.close()
        conn.close()

    def GetInfoList(self,table):
        conn = MySQLdb.connect(host=connhost,user=user,passwd=passwd,db=db,charset=charset)
        conn.select_db(db)
        cursor = conn.cursor()
        constring = "select title,author,dates,content,imagepath,attachment from %s order by dates desc;"%(table)
        cursor.execute(constring)
        result = cursor.fetchall()
        return result

    def GetLeaveMessage(self):
        conn = MySQLdb.connect(host=connhost,user=user,passwd=passwd,db=db,charset=charset)
        conn.select_db(db)
        cursor = conn.cursor()
        constring = "select author,dates,message from leavemessage order by dates desc;"
        cursor.execute(constring)
        result = cursor.fetchall()
        messagelist = []
        for r in result:
            messagelist.append(r)
        return messagelist

    def StoreLeaveMessage(self,mid,dates,author,message):
        conn = MySQLdb.connect(host=connhost,user=user,passwd=passwd,db=db,charset=charset)
        conn.select_db(db)
        cursor = conn.cursor()
        constring = "insert into leavemessage(id,dates,author,message)values('%s','%s','%s','%s');"%(mid,dates,author,message)
        cursor.execute(constring)
        conn.commit()
        cursor.close()
        conn.close()

    def GetName(self,mid):
        name =self.getstudentname(mid)
        print name
        if name is None:
            name =self.getTeachername(mid)
        if name is None:
            name = mid
        print name
        return name

    def Getproject(self,s_id):
        conn = MySQLdb.connect(host=connhost,user=user,passwd=passwd,db=db,charset=charset)
        conn.select_db(db)
        cursor = conn.cursor()
        constring = "select p_name,p_year from projection where c_id='%s';"%(s_id)
        cursor.execute(constring)
        projectlist = cursor.fetchall()
        projectDict={}
        for project in projectlist:
            projectDict[project[0]] = project[1]
        cursor.close()
        conn.close()
        return projectDict

    def GetProjectContent(self,p_name):
        conn = MySQLdb.connect(host=connhost,user=user,passwd=passwd,db=db,charset=charset)
        conn.select_db(db)
        cursor = conn.cursor()
        constring = "select p_charge,p_teacher1,p_teacher2,p_info,filepath,midfile,endfile from projection where p_name ='%s';"%(p_name)
        cursor.execute(constring)
        ProjectInfoDict = cursor.fetchone()
        return ProjectInfoDict

    def StoreFilePath(self,filetype,filepath,p_name):
        conn = MySQLdb.connect(host=connhost,user=user,passwd=passwd,db=db,charset=charset)
        conn.select_db(db)
        cursor = conn.cursor()
        constring = "update projection set %s ='%s' where p_name ='%s';"%(filetype,filepath,p_name)
        cursor.execute(constring)
        conn.commit()
        cursor.close()
        conn.close()

    def AnalyseGetProject(self,college,pro_status):
        conn = MySQLdb.connect(host=connhost,user=user,passwd=passwd,db=db,charset=charset)
        conn.select_db(db)
        cursor = conn.cursor()
        constring = "select p_name,p_year from projection where college = '%s' and pro_status = '%s';"%(college,pro_status)
        cursor.execute(constring)
        Projectlist = cursor.fetchall()
        return Projectlist

    def AnalyseGetProjectInfo(self,p_name):
        conn = MySQLdb.connect(host=connhost,user=user,passwd=passwd,db=db,charset=charset)
        conn.select_db(db)
        cursor = conn.cursor()
        constring = "select p_name,college,p_key1,p_key2,p_key3,p_info,filepath,midfile,endfile from projection where p_name ='%s';"%(p_name)
        cursor.execute(constring)
        ProjectInfo = cursor.fetchone()
        return ProjectInfo

    def AnalyseGetApplyfilelist(self,college):
        conn = MySQLdb.connect(host=connhost,user=user,passwd=passwd,db=db,charset=charset)
        conn.select_db(db)
        cursor = conn.cursor()
        constring = "select filepath from projection where college = '%s';"%(college)
        cursor.execute(constring)
        Applyfilelist = cursor.fetchall()
        return Applyfilelist

    def AnalyseGetProjectName(self,college):
        conn = MySQLdb.connect(host=connhost,user=user,passwd=passwd,db=db,charset=charset)
        conn.select_db(db)
        cursor = conn.cursor()
        constring = "select p_name from projection where college = '%s';"%(college)
        cursor.execute(constring)
        projectNamelist = cursor.fetchall()
        return projectNamelist

    def AnalyseGetProjectApplyFilelist(self,college):
        conn = MySQLdb.connect(host=connhost,user=user,passwd=passwd,db=db,charset=charset)
        conn.select_db(db)
        cursor = conn.cursor()
        constring = "select p_name,filepath from projection where college = '%s';"%(college)
        cursor.execute(constring)
        result = cursor.fetchall()
        projectApplylist ={}
        for r in result:
            projectApplylist[r[0]] =r[1]
        return projectApplylist

    def AnalyseGetProjectApplyFile(self,p_name,college):
        conn = MySQLdb.connect(host=connhost,user=user,passwd=passwd,db=db,charset=charset)
        conn.select_db(db)
        cursor = conn.cursor()
        constring = "select filepath from projection where college = '%s' and p_name = '%s';"%(college,p_name)
        cursor.execute(constring)
        result = cursor.fetchone()
        filepath = result[0]
        return filepath

    def AnalyseGetProjectMidFile(self,p_name,college):
        conn = MySQLdb.connect(host=connhost,user=user,passwd=passwd,db=db,charset=charset)
        conn.select_db(db)
        cursor = conn.cursor()
        constring = "select midfile from projection where college = '%s' and p_name = '%s';"%(college,p_name)
        cursor.execute(constring)
        result = cursor.fetchone()
        midfile = result[0]
        return midfile

    def AnalyseGetProjectMidFilelist(self,college):
        conn = MySQLdb.connect(host=connhost,user=user,passwd=passwd,db=db,charset=charset)
        conn.select_db(db)
        cursor = conn.cursor()
        constring = "select p_name,midfile from projection where college = '%s';"%(college)
        cursor.execute(constring)
        result = cursor.fetchall()
        projectMidlist ={}
        for r in result:
            projectMidlist[r[0]] =r[1]
        return projectMidlist

    def AnalyseGetProjectEndFile(self,p_name,college):
        conn = MySQLdb.connect(host=connhost,user=user,passwd=passwd,db=db,charset=charset)
        conn.select_db(db)
        cursor = conn.cursor()
        constring = "select endfile from projection where college = '%s' and p_name = '%s';"%(college,p_name)
        cursor.execute(constring)
        result = cursor.fetchone()
        endfile = result[0]
        return endfile

    def AnalyseGetProjectEndFilelist(self,college):
        conn = MySQLdb.connect(host=connhost,user=user,passwd=passwd,db=db,charset=charset)
        conn.select_db(db)
        cursor = conn.cursor()
        constring = "select p_name,endfile from projection where college = '%s';"%(college)
        cursor.execute(constring)
        result = cursor.fetchall()
        projectEndlist ={}
        for r in result:
            projectEndlist[r[0]] =r[1]
        return projectEndlist

    def AnalyseGetSearchProject(self):
        conn = MySQLdb.connect(host=connhost,user=user,passwd=passwd,db=db,charset=charset)
        conn.select_db(db)
        cursor = conn.cursor()
        constring = "select p_name,p_year from projection;"
        cursor.execute(constring)
        Projectlist = cursor.fetchall()
        return Projectlist

    def GetNewNotice(self):
        conn = MySQLdb.connect(host=connhost,user=user,passwd=passwd,db=db,charset=charset)
        conn.select_db(db)
        cursor = conn.cursor()
        constring = "select title,dates from notice order by dates desc;"
        cursor.execute(constring)
        noticelist = cursor.fetchall()
        return noticelist

    def GetNewNews(self):
        conn = MySQLdb.connect(host=connhost,user=user,passwd=passwd,db=db,charset=charset)
        conn.select_db(db)
        cursor = conn.cursor()
        constring = "select title,dates from news order by dates desc;"
        cursor.execute(constring)
        newslist = cursor.fetchall()
        return newslist