import smtplib, ssl
from email.mime.text import MIMEText
from email.header import Header
from configs import MAIL_PORT, MAIL_SERVER, MAIL_USEERNAME, MAIL_PASSWORD


verify_text = '''
<p>【schedulenote】您的验证码为（该验证码5分钟内有效）：</p>
<b><p>{code}</p></b>
<p>如非本人操作，请忽略本邮件</p>
'''





# 向receiver发送验证邮件，其中包含6位验证码
# 用于邮件验证、邮件登录、通过邮件修改密码（忘记原密码）
# return 0成功，return -1失败
def send_email(receiver, verify_code):
    try:
        message = MIMEText(verify_text.format(code = verify_code), 'html', 'utf-8')
        message['From'] = MAIL_USEERNAME
        message['To'] =  receiver
        message['Subject'] = Header("中文标题","utf-8")
        context = ssl.create_default_context()
        # print(message.as_string()) 
        with smtplib.SMTP_SSL(MAIL_SERVER, MAIL_PORT, context = context) as server:
            server.login(MAIL_USEERNAME,MAIL_PASSWORD)  
            server.sendmail(MAIL_USEERNAME, receiver, message.as_string())
        return 0
    except Exception as e:
        print("mail error : ", e)
        return -1

if send_email("546774786@qq.com", 123456) == -1:
    print("fail")
else:
    print("succees")