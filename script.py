from calendar import c
import requests
import smtplib
import time
from datetime import datetime

#Calculate Time Difference
def difference(h1, m1, h2, m2):
      
    # convert h1 : m1 into minutes
    t1 = h1 * 60 + m1
      
    # convert h2 : m2 into minutes 
    t2 = h2 * 60 + m2
      
    if (t1 == t2): 
        print("Both are same times")
        return 0
    else:
        # calculating the difference
        diff = t2-t1
          
    # calculating hours from the difference
    h = (int(diff / 60)) % 24
      
    # calculating minutes from the difference
    m = diff % 60
    return h*60*60 + m*60

#Accesing the API Key from the api_key_storage file
with open ("api_key_storage.txt", "r") as api_file:
    api_key = api_file.read()

#Starting point
starting_point = input("Enter the loctaion from where you will commence your journey: ")

#Final Destination
final_destination = input("Enter your final destination: ")

#Reporting Time
reporting_time = '...'

#url to send requests
url ='https://maps.googleapis.com/maps/api/distancematrix/json?'

#get a response from the API
api_response = requests.get(url + "origins=" + starting_point + "&destinations=" + final_destination + "&key=" + api_key)


#fetching time in usual display format and as seconds, we use the seconds for calculation      
seconds = api_response.json()["rows"][0]["elements"][0]["duration"]["value"]
print(api_response.json())

#fetch current time
current_time = time.localtime()
current_time = time.strftime("%H%M", current_time)

if(seconds > difference(int(current_time[0:2]), int(current_time[2:]), int(reporting_time[0:2]), int(reporting_time[2:]))):
    #EMail Credentials
    sender_email = "..."    
    recipient_email = "..."       
    subject = "High Traffic"   
    message = "Hello Boss,\nSorry, but I can't make it into work today on time.\nThe traffic seems to be very heavy.\nRegards,\n<Your Name>"

    #Formatting the EMail
    email = "Subject: {}\n\n{}".format(subject, message)

    #Retreive the password
    with open("passwords.txt", "r") as password_file:
        email_password = password_file.readline()
    
    #Create SMTP Session
    #Simple Mail Transfer Protocol (SMTP) is a protocol, which handles sending e-mail and routing e-mail between mail servers
    s = smtplib.SMTP("smtp.gmail.com", 587)

    #Start TLS Session to enable secure transmission of sensitive data
    s.starttls()

    #Login
    s.login(sender_email, email_password)

    #Sending the EMail 
    s.sendmail(sender_email, recipient_email, email)

    #Successfully Sent the Email
    print("Successfully sent the email.")
    #Logout
    s.quit()





