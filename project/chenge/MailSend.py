__author__ = 'root'
# -*- coding: utf-8 -*-



import smtplib
import email.MIMEMultipart
import email.MIMEText
import email.MIMEBase
import os.path
from email.mime.text import MIMEText

class MailSend:
    def Sendwithfile(self,mailsender,mail_list,content,file_name,mail_title):
        # From = "18819423747<18819423747@163.com>"
        From = mailsender[1]
        title=mail_title
        print mail_title
        # To = "zhangliming134@foxmail.com;1024760384@qq.com"
        # file_name = "/home/gdufs-iiip/下载/pywordform-0.01.zip"
        To=";".join(mail_list)
        server = smtplib.SMTP()
        server.connect("smtp.163.com")
        # server.login('18819423747','xie5321927')
        server.login(mailsender[0],mailsender[2])
        # 构造MIMEMultipart对象做为根容器
        main_msg = email.MIMEMultipart.MIMEMultipart()

        # 构造MIMEText对象做为邮件显示内容并附加到根容器
        text_msg = MIMEText(content,_subtype='plain',_charset='gb2312')
        main_msg.attach(text_msg)

        # 构造MIMEBase对象做为文件附件内容并附加到根容器
        contype = 'application/octet-stream'
        maintype, subtype = contype.split('/', 1)
        if file_name is not None:
            ## 读入文件内容并格式化
            data = open(file_name, 'rb')
            file_msg = email.MIMEBase.MIMEBase(maintype, subtype)
            file_msg.set_payload(data.read( ))
            data.close( )
            email.Encoders.encode_base64(file_msg)

            ## 设置附件头
            basename = os.path.basename(file_name)
            file_msg.add_header('Content-Disposition',
            'attachment', filename = basename)
            main_msg.attach(file_msg)

            # 设置根容器属性
            main_msg['From'] = From
            main_msg['To'] = To
            main_msg['Subject'] = title
            main_msg['Date'] = email.Utils.formatdate( )

            # 得到格式化后的完整文本
            fullText = main_msg.as_string( )
        else:
            fullText =None
        # 用smtp发送邮件
        try:
            server.sendmail(From, To, fullText)
        finally:
            server.quit()
    def mail_fileLoad(self,file,filename):
        if not os.path.exists('static/mail/'):
            os.mkdir('static/mail/')
        with open('static/mail/'+filename,'wb+') as destination:
            for chunk in file.chunks():
                destination.write(chunk)
        return 'static/mail/'+filename

    def send_mailText(self,sender,to_list,content,title):
        print 'nice'
        print title ,content
        mail_host="smtp.163.com"
        mail_user=sender[0]
        mail_pass =sender[2]
        # me="hello"+"<"+mail_user+"@"+mail_postfix+">"
        me = sender[1]
        msg = MIMEText(content,_subtype='plain',_charset='gb2312')
        msg['Subject'] = title
        msg['From'] = me
        msg['To'] = ";".join(to_list)
        try:
            server = smtplib.SMTP()
            server.connect(mail_host)
            server.login(mail_user,mail_pass)
            server.sendmail(me, to_list, msg.as_string())
            server.close()
            return True
        except Exception, e:
            print str(e)
            return False


if __name__ == '__main__':
    target_mailist=[u"1024760384@qq.com"]
    mail_title="sa"
    content="挺好的"
    filename='/home/quincy1994/project/templates/ProjectApply.html'
    filename =None
    sender=['18819423747','18819423747<18819423747@163.com>','xie5321927']
    m=MailSend()
    # m.Send(sender,target_mailist,content,filename,mail_title)
    m.send_mailText(sender,target_mailist,content,mail_title)





