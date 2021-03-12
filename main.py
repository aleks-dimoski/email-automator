import smtplib, ssl, os, csv, re
from email import encoders
from email.mime.base import MIMEBase
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
#import pandas as pd


#path = "filepath"
#raw =  pd.read_csv(filepath, delim=",")
"""
raw : pd.DataFrame
literally the GPU accelerated equivalent of an excel spreadsheet

    Type of Business, Name, Number, ....
1   Food                Michelle        201-000000
2
3
.
.
.


raw["Name"] = [all of the names]
raw.loc[1,1] = "Michelle <3 {address}"

## lets say youre worried about trailing spaces
apply the function (remove_trailing on all fo the names
and remove leading"
then pop the last character off of every name
now youre guaranteed
"""


"""
Type of Business,Name,Number,Called?,Emailed?,Email,Meeting / Vid Chat?,Contact Name?,"Amount, Date Range, Location/Type"
Food,Michelle <3 {,201-914-6069,✔,X,mwang57@stevens.edu,X,N/A,CBL
Food,ADDDDD {,201-790-0491,✔,✔,info@aleksandardimoski.com,X,N/A,Called; said manager absent & to email at attached address
Food,3 {,201-653-5319,✔,X,,X,N/A,"Called, waited for manager for 20 minutes, then they hung up on me"
"""
def send_to_emails(server):
    with open("contact_info.csv") as csvfile:
        reader = csv.reader(csvfile)
        info = {}
        for row in reader:
            if bool(re.search(r"(\w|\d)*@(\w|\d)*\.\w*", row[5])):
                info[row[1][:str.index(row[1], '{')-1]] = row[5]

        #info = {row[1][:str.index(row[1], '{')-1]:row[5] for row in reader if bool(re.search(r"(\w|\d)*@(\w|\d)*\.\w*", row[5]))}
        for key in info.keys():
            print(key, " ", info[key])
    for key in info:
        message = MIMEMultipart()
        message["Subject"] = "[The Stute] Advertising at " + key +" - Media Kit"
        message["From"] = "Aleks at The Stute"
        message["To"] = info[key]
        message.attach(media_kit)
        body = MIMEText(re.sub(r"_+", key, html)[1:], "html")
        message.attach(body)
        server.sendmail(sender_email, info[key], message.as_string())

smtp_server = "smtp.gmail.com"
port = 587
sender_email = "aleksdimoski890@gmail.com"
password = input("Enter your password: ")

filename = "Stute_Media_Kit_Online.pdf"
with open(filename, "rb") as attachment:
    media_kit = MIMEBase("application", "octet-stream")
    media_kit.set_payload(attachment.read())
encoders.encode_base64(media_kit)
media_kit.add_header(
    "Content-Disposition",
    f"attachment; filename= {filename}",
)

f = open("message.txt", 'r')
html = f.read()
f.close()

context = ssl.create_default_context()

try:
    server = smtplib.SMTP(smtp_server, port)
    server.starttls(context=context)
    server.login(sender_email, password)
    send_to_emails(server)
except Exception as e:
    print(e)
finally:
    server.quit()
