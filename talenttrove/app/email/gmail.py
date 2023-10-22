import imaplib
import email
from datetime import datetime, timedelta
from email.header import decode_header

class Gmail:
    def __init__(self, username, password):
        self.username = username
        self.password = password
    
    def authenticate(self):
        # authenticate with gmail
        # https://www.systoolsgroup.com/imap/
        gmail_host= 'imap.gmail.com'
        #set connection
        mail = imaplib.IMAP4_SSL(gmail_host)
        #login
        mail.login(self.username, self.password)
        self.mail = mail
    
    def search_mail(self,category='INBOX',search_criteria='ALL'):
        self.mail.select(category)
        _, email_ids = self.mail.search(None,search_criteria)
        email_ids = email_ids[0].split()
        return email_ids
    
    def get_email_by_date(self,from_date,category='INBOX',primary=True,to_date=(datetime.now() + timedelta(days=1)).strftime("%d-%b-%Y")):
        primary = ' X-GM-RAW "Category:Primary"' if primary else ""
        search_criteria = f'(SINCE "{from_date}" BEFORE "{to_date}"){primary}'
        email_ids = self.search_mail(category=category,search_criteria = search_criteria)
        return email_ids
    
    @staticmethod
    def get_body(msg):
        if msg.is_multipart():
            for part in msg.walk():
                content_type = part.get_content_type()
                content_disposition = str(part.get("Content-Disposition"))
                if "attachment" not in content_disposition:
                    print('x')
                    body = part.get_payload(decode=True)
                    if body is None:
                        continue
                    body = body.decode()
        else:
            body = msg.get_payload(decode=True).decode()
        return body

    def parse_emails(self,ids:list):
        data=[]
        for email_id in ids:
            _, email_data = self.mail.fetch(email_id, '(RFC822)')
            raw_email = email_data[0][1]

            # Parse the email
            msg = email.message_from_bytes(raw_email)
            # Extract email information (e.g., subject and sender)
            subject, _ = decode_header(msg["Subject"])[0]
            sender, _ = decode_header(msg["From"])[0]
            data.append(
                {
                    'subject':subject,
                    'sender':sender,
                    'date':msg['Date'],
                    'body':self.get_body(msg),
                }
            )

        return data

    def close(self):
        self.mail.close()
        self.mail.logout()