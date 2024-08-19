import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
import os

class MailSender:
    def __init__(self, smtp_svr, subject, sender, receiver, cc,bcc):
        self.content_list = []

        self.smtp_svr =
        self.emIl = MIMEMultipart("mixed")

   def _add_list_content(self, _content_type='', _content, file_list =[]):
       if(_content_type == "html"):
         self.contents_list.append(MIMEText(_content,_content_type)
       elif(_content_type == 'images')
            for file_name in file_list:
                with open(file_name ,'rb') as fp:
                    img = MIMEImage(fp.read)
                    img.add_header(
                    self.contents_list.append(img)
    def _merge_content(self):
        for content in self.contents_list:
            self.email.attach(content)
        content = []

   def _add_content

   def add_ht_content):
       self.emIl.attach( mimetext(content, 'html')

   def add_cid(self, cid_name , cid_image : bytes)
    cid_data = MIMEImage(cid_image)
    cid_data.add_header('Content-ID', f'<{cid_name}>')
    self.email.attach(cid_data)


 ## --> Class 객체로 만들 예정
def send_email(subject, body, to_email, from_email, smtp_server, smtp_port, login, password, attachment_path=None):
    # Create the email headers and message
    msg = MIMEMultipart()
    msg['From'] = from_email
    msg['To'] = to_email
    msg['Subject'] = subject

    # Attach the email body
    # msg.attach(MIMEText(body, 'plain'))
    msg.attach(MIMEText(body, 'html'))
    
    # Attach a file if provided
    if attachment_path:
        attachment = open(attachment_path, "rb")
        part = MIMEBase('application', 'octet-stream')
        part.set_payload((attachment).read())
        encoders.encode_base64(part)
        part.add_header('Content-Disposition', f"attachment; filename= {os.path.basename(attachment_path)}")
        msg.attach(part)

    # Connect to the server and send the email
    server = smtplib.SMTP(smtp_server, smtp_port)
    server.starttls()
    server.login(login, password)
    text = msg.as_string()
    server.sendmail(from_email, to_email, text)
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
    

