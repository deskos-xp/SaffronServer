import smtplib

from email.mime.multipart import MIMEMultipart 
from email.mime.text import MIMEText 
from email.mime.base import MIMEBase 
from email import encoders 

class sender:
    send_type=None
    attachment=None
    carriers_mms={}
    carriers_txt = {
        'boost':'@sms.myboostmobile.com',
        'cricket':'@mms.cricketwireless.net',
        'google-project-fi':'@msg.fi.google.com',
        'republican-wireless':'@text.republicwireless.com',
        'sprint':'@messaging.sprintpcs.com',
        'straight-talk':'@vtext.com',
        't-mobile':'@tmomail.net',
        'ting':'@message.ting.com',
        'us-cellular':'@email.uscc.net',
        'verizon':'@vtext.com',
        'virgin-mobile':'@vmobl.com',
        '':''
    }
    def send(self,message,to:str,email:str,password:str,carrier:str):
            # Replace the number with your own, or consider using an argument\dict for multiple people.
            to_number = '{}{}{}{}'.format(*to,self.carriers_txt[carrier])
            auth = (email, password)
             
            # Establish a secure session with gmail's outgoing SMTP server using your gmail account
            server = smtplib.SMTP( "smtp.gmail.com", 587 )
            server.starttls()
            server.ehlo()
            server.login(auth[0], auth[1])
            if self.send_type == "email":
                with open(self.attachment,"rb") as attachment:
                    print("sending")
                    msg=MIMEMultipart()
                    print(email)
                    msg['From']=email
                    msg['To']=to
                    msg['Subject']=message
                    msg.attach(MIMEText("see attachment","plain"))

                    p=MIMEBase('application','octet-stream')
                    p.set_payload((attachment).read())
                    encoders.encode_base64(p)
                    p.add_header('Content-Disposition', "attachment; filename= {}".format(self.attachment))
                    msg.attach(p)
                    message=msg.as_string()
            # Send text message through SMS gateway of destination number
            to_number=to
            server.sendmail( auth[0], to_number, message)
            server.quit()
    def __init__(self):
        pass

    def __init__(self,send_type,attachment):
        self.send_type=send_type
        self.attachment=attachment

if __name__ == "__main__":
    sender().send("from pc",(804,854,4057),'k.j.hirner.wisdom@gmail.com','T1mes_ch@nge')
