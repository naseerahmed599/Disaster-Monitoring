import smtplib
from email.message import EmailMessage

def email_alert(sub, text, to):
    msg = EmailMessage()
    msg.set_content(text)
    msg['subject'] = sub
    msg['to'] = to
    
    user = 'fyp.project.buitems@gmail.com'
    msg['from'] = user
    password = 'kuqexleksjdisspw'
    
    server = smtplib.SMTP('smtp.gmail.com',587)#587
    #setting gmail requires
    server.starttls()
    server.login(user, password)
    server.send_message(msg)
    
    
    server.quit()
    
#if __name__ == '__main__':
    #email_alert('Hey', 'Hello world','ahmednaseer5991@gmail.com')