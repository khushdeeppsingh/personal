Python Email Sender
This code provides a function send_python_email to send emails with multiple data tables and attachments. The email is sent using an SMTP server or your personal Gmail account. The email body is formatted using pretty_html_table package and a random theme is selected for the email.

Requirements
This code requires the following packages to be installed:

os
datetime
pytz
smtplib
email
pandas
pretty_html_table
random
How to use
To use this code, follow the steps below:

Import the required libraries and the send_python_email function from emailer.py.
Set the email subject line and display email, and the recipient email addresses.
Prepare the data tables and attachments to be included in the email. The data tables must be in the form of a list of tuples where each tuple consists of a heading, a pandas dataframe, and a comment (optional).
Call the send_python_email function with the required parameters.
