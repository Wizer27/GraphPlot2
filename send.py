import smtplib
from email.mime.text import MIMEText
from email.utils import formataddr




server = "smtp.gmail.com" 
port = 587
email = 'some email'
passw = 'some pass'


Rec = 'some email'





msg = MIMEText("Hey ! Here is yor email verification code for my app.Thanks for using GraphPLot")
msg["Subject"] = "Verfication code (GraphPLot)"
msg["From"] = formataddr(("GraphPlot", email))
msg["To"] = Rec


try:
    with smtplib.SMTP(server, port) as server:
        server.starttls()  # Шифрование TLS
        server.login(email, passw)
        server.sendmail(email, Rec, msg.as_string())
    print("Mail sent!")
except Exception as e:
    print(f"Error: {e}")