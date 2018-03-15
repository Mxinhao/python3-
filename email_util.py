# 使用SMTP发送邮件，pop3接收邮件
#--coding:utf-8
import smtplib
import poplib
from email.parser import Parser
from email.header import decode_header
from email.utils import parseaddr
import time
from email.mime.application import MIMEApplication
from email.mime.text import MIMEText
from email.header import Header
from email.mime.multipart import MIMEMultipart
import sys
# 自定义异常类，出现异常打印出异常消息，并退出程序
class MyException(Exception):
    def __init__(self,message):
        Exception.__init__(self)
        # self.message=message
        print(message)
        sys.exit()
#         主类
class email_util():
    def __init__(self,server,user,password,port=25):
        self.server=server
        self.user=user
        self.passwprd=password
        self.port=port
        self.text_content = {}#通过pop3获取的邮件内容，字典类型，包涵邮件内容和附件
        self.files = []#通过pop3获取附件数组，最终放在self.text_content字典中返回
    #     发送邮件的SMTP连接
    def get_connection(self):
        try:
            smtpOBJ = smtplib.SMTP()
            try:
                smtpOBJ.connect(self.server, self.port)  # 25 为 SMTP 端口号
            except Exception as e:
                raise MyException("server connection fail")
            try:
                smtpOBJ.login(self.user, self.passwprd)
            except Exception as e:
                raise MyException("user or password is wrong")
            return smtpOBJ
        except smtplib.SMTPException as e:
            print(e)
    #         发送邮件的方法
    def send_email(self,message):
        smtpObj=self.get_connection()
        print("连接成功........")
        try:
            smtpObj.sendmail(message["From"], message["To"], message.as_string())
            print("send email success")
        except Exception as e:
            raise MyException("send email fail")
        if smtpObj is not None:
            smtpObj.quit()
    #     从服务器获取邮件
    def get_pop_connection(self):
        # 连接到POP3服务器:
        try:
            server = poplib.POP3(self.server,timeout=300)
            try:
                # 身份认证
                server.user(self.user)
                server.pass_(self.passwprd)
            except Exception as e:
                raise MyException("user or password wrong")
            return server
        except Exception as e:
            raise MyException("pop3 failed connection")
    #     获取收件箱邮件总个数
    def mails_count(self):
        server = self.get_pop_connection()
        resp, mails, octets = server.list()
        return len(mails)
    #     获取并解码邮件，以邮件索引来获取邮件并返回
    def get_email(self,index):
        self.files=[]
        server=self.get_pop_connection()
        resp, lines, octets = server.retr(index)
        msg_content = b'\r\n'.join(lines).decode("utf-8",errors="ignore" )
        msg = Parser().parsestr(msg_content)
        return msg
    # 根据邮件头的编码方式进行解码
    def decode_str(self,s):
        value, charset = decode_header(s)[0]
        if charset:
            value = value.decode(charset)
        return value
    # 获取邮件正文内容编码方式charset
    def guess_charset(self,msg):
        charset = msg.get_charset()
        if charset is None:
            content_type = msg.get('Content-Type', '').lower()
            pos = content_type.find('charset=')
            if pos >= 0:
                charset = content_type[pos + 8:].strip()
        return charset
    # 获取发件人
    def get_sender(self,email):
        value = email.get("From", '')
        hdr, addr = parseaddr(value)
        From = addr
        return From
    # 获取收件人
    # email.util  parseaddr只能获取到一个收件人
    def get_receive(self,email):
        value = email.get("To", '')
        addrs = []
        for cc in value.split(","):
            name, addr = parseaddr(cc)
            name=self.decode_str(name)
            addrs.append({"name": name, "address": addr})
        return addrs
    # 获取CC收件人
    def get_receive_cc(self, email):
        value = email.get("Cc", '')
        addrs=[]
        for cc in value.split(","):
            name, addr = parseaddr(cc)
            name = self.decode_str(name)
            addrs.append({"name":name,"address":addr})
        return addrs
    # 获取邮件主题
    def get_subject(self,email):
        value = email.get("Subject", '')
        value = self.decode_str(value)
        Subject = value
        return Subject
    # 获取邮件的发送时间，并将日期处理成一般形式
    def get_email_date(self,email):
        value = email.get("Date", '')
        return value
#     处理附件内容，放进self.text_content字典
    def handle_attchment(self,msg):
        file = {}
        for part in msg.walk():
            content_type = msg.get_content_type()
            fileName = part.get_filename()
            if fileName:
                filename = self.decode_str(fileName)
                file["file_type"] = content_type
                file["name"] = filename
                data = part.get_payload(decode=True)
                file['data'] = data
                self.files.append(file)
                self.text_content["files"] = self.files
        
#     获取邮件的内容,返回字典
    def get_mail_content(self,msg):
        if (msg.is_multipart()):
            parts = msg.get_payload()
            for n, part in enumerate(parts):
                self.get_mail_content(part)
        else:
            content_type = msg.get_content_type()
            # 输出邮件的内容，if 里面是邮件正文，else是附件
            if content_type=='text/plain' or content_type == 'text/html':
                email_content={}
                content = msg.get_payload(decode=True)
                charset = self.guess_charset(msg)
                # 由于content_type=='text/plain' 附件是txt时也是这种类型,邮件纯文本也是
                # 所以，charset存在说明是邮件正文，不存在是txt文件
                if charset:
                    email_content['charset'] = charset
                    content = content.decode(charset)
                    email_content["content"]=content
                    self.text_content["email_content"] = email_content
                else:
                    self.handle_attchment(msg)#txt类型附件
            else:
                self.handle_attchment(msg)#其他类型附件
        return self.text_content
