import requests
import time
import random
import string
import hashlib
import pandas as pd
import json
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


def create_api_request(api_callerid, api_key, area):
    global time, output
    callerId = api_callerid
    key = api_key
    time = str(time.time())
    unique = str(''.join(random.choice(string.ascii_lowercase + string.digits) for _ in range(16)))
    hashstr = hashlib.sha1((callerId + time + key + unique).encode('utf-8')).hexdigest()
    query_type = 'listings'
    query_city = area
    offset = '0'
    limit = str(10)  # Maximum number of response objects. Limit = 500
    object_type = "lägenhet"
    MinRooms = "1"
    MaxPrice = "3500000"
    r = requests.get("https://api.booli.se/" +
                     query_type + "?q=" + query_city +
                     "&callerId=" + callerId +
                     "&time=" + time +
                     "&unique=" + unique +
                     "&hash=" + str(hashstr) +
                     "&limit=" + limit +
                     "&offset=" + offset +
                     "&objectType=" + object_type +
                     "&minRooms=" + MinRooms +
                     "&maxListPrice=" + MaxPrice)
    print("Status code from API request = " + str(r.status_code) + "\n")
    if r.status_code != 200:
        print(r.text)
        print('fail')
        exit()

    return json.loads(r.text)


def create_df(output):
    urls = []
    for value in range(len(output['listings'])):
        urls.append(output['listings'][value]['url'])
    object_id = []
    for value in range(len(output['listings'])):
        object_id.append(output['listings'][value]['booliId'])
    room_info = []
    for value in range(len(output['listings'])):
        room_info.append(output['listings'][value]['rooms'])
    muni_info = []
    for value in range(len(output['listings'])):
        muni_info.append(output['listings'][value]['location']['region']['municipalityName'])
    price_info = []
    for value in range(len(output['listings'])):
        price_format = '{:,}'.format(output['listings'][value]['listPrice'])
        price_info.append(price_format)
    address_info = []
    for value in range(len(output['listings'])):
        address_info.append(output['listings'][value]['location']['address']['streetAddress'])
    published_info = []
    for value in range(len(output['listings'])):
        date_format = pd.to_datetime(output['listings'][value]['published'], format="%Y-%m-%d %H:%M:%S")
        published_info.append(date_format.date())
    df = pd.DataFrame({
        'Published': published_info,
        '2. Area': muni_info,
        '1. Address': address_info,
        '4. Rooms': room_info,
        '3. Price': price_info,
        '5. urls': urls
    })
    df2 = df.set_index(['Published'])
    df_html = df2.to_html()
    #print(df2)
    return df_html


def create_html(df_html):
    html = """\
       <html>
            <body>

                Hi,
                <p>
                    Here is your custom email notification regarding new listings. 
                    <b></b>
                    %s
                    <b></b>
                    Please contact rikard.fahlstrom@gmail.com if you have suggestions for improvements.
                </p> 
             </body>
       </html>
   """ % (df_html)
    return html


def send_email(send_to, send_from_email, send_from_password, html):
    fromaddr = 'Custom email notification'
    toaddr = send_to
    subject = 'Most recent listings'
    msg = MIMEMultipart()
    msg['From'] = fromaddr
    msg['To'] = toaddr
    msg['Subject'] = subject
    msg.attach(MIMEText(html, 'html'))
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login('rikard.email.notification@gmail.com', send_from_password)
    text = msg.as_string()
    server.sendmail(send_from_email, toaddr, text)
    server.quit()
    print('Done')


def main():
    output = create_api_request('Rikard Fahlström', api_key, 'fålhagen')
    df = create_df(output)
    html = create_html(df)
    send_email('rikard.fahlstrom@gmail.com', 'rikard.email.notification@gmail.com', 'send_from_password, html)


if __name__ == '__main__':
    main()
