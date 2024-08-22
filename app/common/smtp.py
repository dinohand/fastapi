import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
import os


## 수정중
class MailSender():
    def __init__(self, login :str , password : str, smtp_server :str, smtp_port:int):
        self.server = smtplib.SMTP(smtp_server, smtp_port)
        # server.starttls()
        self.server.login(login, password)
        self.msg = MIMEMultipart('mixed')
        self.content =''
        
    def set_title(self, subject):
        self.msg['Subject'] = subject
    
    def set_email(self, from_email, to_email):
        self.msg['From'] = from_email
        self.msg['To'] = to_email
    
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
    

