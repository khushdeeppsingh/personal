# importing libraries
import os
from datetime import date, timedelta, datetime
from app import logger #to check logs
import numpy as np
import smtplib
import pytz #for time
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
import pandas as pd
from pretty_html_table import build_table
import random

# randomized theme for email
html_theme = random.choice(['green_light', 'yellow_light', 'orange_light', 'grey_light', 'blue_light' ])
today = date.strftime(datetime.now(pytz.timezone('Asia/Dubai')), '%Y-%m-%d %H' + ' Hr')

# use this if keys available 
SMTP_SERVER = os.environ.get('SMTP_SERVER')
SMTP_USER = os.environ.get('SMTP_USER')
SENDGRID_API_KEY = os.environ.get('SENDGRID_API_KEY')
subject = ''

def send_mail(from_email, to_email, parsed_content):
    logger.info('4. Mailer ran')
    conn = smtplib.SMTP(SMTP_SERVER)
    conn.set_debuglevel(False)
    conn.login(SMTP_USER, SENDGRID_API_KEY)
    logger.info('trying to send email')
    conn.sendmail(
        from_email, to_email, parsed_content.as_string()
    )
    logger.info('mailer sent')
    logger.info('mailer quitting')
    conn.quit()

# or if testing on local use you personal gmail account.

# SMTP_USER = "your email"
# SENDGRID_API_KEY = "email_password"
# def send_mail(from_email, to_email, parsed_content):
#     try:
#         context = ssl.create_default_context()
#         with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
#             server.login(SMTP_USER, SENDGRID_API_KEY)
#             server.sendmail(
#                 from_email, to_email, parsed_content.as_string()
#         )
#     except Exception as e:
#         print(f"Failed to send email: {e}")
#         raise

def get_html(data_tables):
    html = f'<html><head></head><body><h1>{subject}</h1>'

    for title, dataframe, comment in data_tables:
        html += f'<h2>{title}</h2>' if title else '<br>'
        html += f'<p>{comment}</p>' if comment else ''
        html += f"{build_table(dataframe, html_theme)}"
    html += '</body></html>'

    return html


def get_parsed_content(subject, data_tables=[], attachments_list=[], attachment_name=[], from_email='', to_email=''):
    parsed_content = MIMEMultipart('alternative')
    parsed_content['Subject'] = subject
    parsed_content["From"] = from_email
    parsed_content["To"] = ", ".join(to_email)

    # Include body
    email_body = MIMEText(get_html(data_tables), 'html')
    parsed_content.attach(email_body)

    # Include Attachments
    if len(attachment_name)==0:
        for index, attachment in enumerate(attachments_list):
            attachment = MIMEApplication(attachment.to_csv(index = False))
            attachment["Content-Disposition"] = f'attachment; filename= "attachment_{index}.csv"'
            parsed_content.attach(attachment)
        logger.info('3. subject, attachment done')
        return parsed_content
    else:
        for index, attachment in enumerate(attachments_list):
            attachment = MIMEApplication(attachment.to_csv(index = False))
            attachment["Content-Disposition"] = f'attachment; filename= "{index}.{attachment_name[index]}.csv"'
            parsed_content.attach(attachment)
        logger.info('3. subject, attachment done')
        return parsed_content        


def send_python_email(subject, from_email, to_email, data_tables, attachments_list, attachment_name):
    parsed_content = get_parsed_content(subject, data_tables, attachments_list, attachment_name, from_email, to_email)
    send_mail(from_email, to_email, parsed_content)

    
#####################################################Functions-Above#######################################################################


# How to use?
#let's say I have a dataframes  df1, df2

# subject = 'your subject' + today 
# from_email  = 'any_display_email'
# to_email = ['can have list of emails', '']
# data_tables = [
#   (heading, table_under_heading, text_bw_headingAndTable)
#     ('Yesterday Summary:', df1,None),
#     ('Yesterday Summary2:', df1.head(10),None),
#     ('Month Top:', df2.head(10),None )
# ]
# attachments = [df, df.head(), df2] #can be empty if not will be in form of csvs
# attachment_name = ['final_file', 'yesterday_raw', 'MTD_raw']
# send_python_email(subject, from_email, to_email, data_tables, attachments,attachment_name)


