# -*- coding:utf-8 -*-
import sys
import codecs
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.pdfpage import PDFPage
from pdfminer.converter import XMLConverter, HTMLConverter, TextConverter
from pdfminer.layout import LAParams
from cStringIO import StringIO
import re
import jieba.analyse
import os

# 截获所统计的段落
def mymatch(matchword,txtfile):
    file=open(txtfile)
    content=file.read()
    content=content.replace('\n','')
    m=re.search(matchword,content)
    matched=m.group()
    return matched

# 字词统计
def wordcount(content):
    regex=re.compile(r"(?x) (?: [\w-]+ | [\x80-\xff]{3} )")
    count = 0
    word = [w for w in regex.split(content)]
    count += len(word)
    return count

#统计的字数
class Countword:
    part=[u'前期基础',u'计划项目实施思路',u'计划项目管理',u'计划项目条件保障',u'指导教师意见']
    def __init__(self):
        matchword1='前期基础.*二、计划项目实施思路'
        matchword2='二、计划项目实施思路（3000 字以内）.*三、计划项目管理'
        matchword3='三、计划项目管理.*四、计划项目条件保障'
        matchword4='四、计划项目条件保障.*五、指导教师意见'
        matchword5='五、指导教师意见.*指导老师签字'
        self.matchgroup=[]
        self.matchnumber=[]
        self.matchcheck={}
        self.matchgroup.append(matchword1)
        self.matchnumber.append(1000)
        self.matchgroup.append(matchword2)
        self.matchnumber.append(3000)
        self.matchgroup.append(matchword3)
        self.matchnumber.append(800)
        self.matchgroup.append(matchword4)
        self.matchnumber.append(800)
        self.matchgroup.append(matchword5)
        self.matchnumber.append(600)

    #查看字数是否超标，超了标注为true,否则false
    def countcheck(self,txtfile):
        checklist=[]
        len = self.matchgroup.__len__()
        for i in range(0,len,1):
            matchworded=mymatch(self.matchgroup[i],txtfile)
            count = wordcount(matchworded)
            if count > self.matchnumber[i]:
                # self.matchcheck[i]=True
                # print self.part[i],'超出字数'
                checklist.append(self.part[i]+u':超出字数')
            elif count < self.matchnumber[i]/2:
                checklist.append(self.part[i]+u':字数过少')
            else:
                self.matchcheck[i]=False
                print checklist
                checklist.append(self.part[i]+u':字数通过')
        print self.matchcheck
        return checklist


# 解读pdf内容
class PDFpraser:
    keytags=[]
    def __init__(self):
        self.pdffile=None
        self.txtfile=None

    def Pdfparser(self,pdf):
        outfile = pdf+'.txt'
        self.pdffile=pdf
        self.txtfile=outfile
        fp = file(pdf, 'rb')
        outfp = file(outfile,'w')
        rsrcmgr = PDFResourceManager()
        retstr = StringIO()
        codec = "utf-8"
        laparams = LAParams()
        device = TextConverter(rsrcmgr, outfp, codec=codec, laparams=laparams)
        # Create a PDF interpreter object.
        interpreter = PDFPageInterpreter(rsrcmgr, device)
        # Process each page contained in the document.
        for page in PDFPage.get_pages(fp):
            interpreter.process_page(page)
            data =  retstr.getvalue()
        device.close()
        outfp.close()

    def countwordcheck(self):
        c=Countword()
        return c.countcheck(self.txtfile)

    def extract(self):
        matchworded=mymatch('二、计划项目实施思路（3000 字以内）.*三、计划项目管理',self.txtfile)
        self.keytags=jieba.analyse.extract_tags(matchworded,10)
        for tag in self.keytags:
            print tag ,
            print '\n'

    def PDFload(self,file,filename):
        if not os.path.exists('static/upload/temp/'):
            os.mkdir('static/upload/temp/')
        with open('static/upload/temp/'+filename,'wb+') as destination:
            for chunk in file.chunks():
                destination.write(chunk)
        return 'static/upload/temp/'+filename

    def deleteFile(self):
        txtfile = self.txtfile
        if os.path.exists(txtfile):
            os.remove(txtfile)

    def readfile(self):
        filename = open(self.txtfile,'rb')
        data =filename.read().replace('\n','')
        data = data.replace('\t','')
        data = data.replace('\r','')
        data = data.replace('\s','')
        return data

    def getPDFdata(self,PDFname):
        self.Pdfparser(PDFname)
        data =self.readfile()
        self.deleteFile()
        return data




if __name__ == '__main__':
    pdf=PDFpraser()
    data =pdf.getPDFdata("/home/quincy1994/桌面/科技月项目申报书/热点公众事件社会情绪分析（实践类）申报书.pdf")
    print data