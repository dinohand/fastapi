import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
import os

class MailSender:
    def __init__(self, login :str = '' , password : str = '' , smtp_server :str ='' , smtp_port:int = 100):
        self.__server = smtplib.SMTP(smtp_server, smtp_port)
        self.__server.login(login, password)
        self.__msg = MIMEMultipart('mixed')
        self.__content =''
        self.__subject = ''
        self.__sender = ''
    
        
    # 메일 서버
    @property
    def server(self):
        return self.__server

    @server.setter
    def server(self, smtp_server : str):
        self.__server = smtp_server

    # 메일 제목
    @property
    def subject(self):
        return self.__subject

    @subject.setter
    def subject(self, subject : str = ''):
        self.__subject = subject
        self.msg['Subject'] = self.__subject

    # 발신자
    @property
    def sender(self):
        return self.__sender

    @sender.setter
    def sender(self, sender : str = ''):
        self.__sender = sender
        self.msg['From'] = self.__sender
    
    # 수신자
    @property
    def reciever(self):
        return self.__reciever
    
    @reciever.setter
    def reciever(self, reciever : str = ''):
        self.__reciever = reciever
        self.msg['To'] = self.__reciever
        
    def attach(self):
        if attachment_path:
            attachment = open(attachment_path, "rb")
            part = MIMEBase('application', 'octet-stream')
            part.set_payload((attachment).read())
            encoders.encode_base64(part)
            part.add_header('Content-Disposition', f"attachment; filename= {os.path.basename(attachment_path)}")
            msg.attach(part)
 
    def set_content(sefl, content):
        self.content = content
        
        
    def send(send):
        with server.SMTP(smtp_server, port) as server:
            server.sendmail(self.from_email, self.to_email, self.content )
        server.quit()    
            

# # Example usage
# if __name__ == "__main__":
#     subject = "Daily Report"
#     body = "Please find attached the daily report."
#     to_email = "recipient@example.com"
#     from_email = "your_email@example.com"
#     smtp_server = "smtp.example.com"
#     smtp_port = 587
#     login = "your_email@example.com"
#     password = "your_password"
#     # attachment_path = "/path/to/report.csv"

#     # send_email(subject, body, to_email, from_email, smtp_server, smtp_port, login, password, attachment_path)
#     send_email(subject, body, to_email, from_email, smtp_server, smtp_port, login, password)
    

