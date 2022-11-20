import os
import chromedriver_binary
import smtplib
from email.mime.text import MIMEText
from email.utils import formatdate
from selenium import webdriver
from time import sleep
from dotenv import load_dotenv


def send_email(date, text):
    sendAddress = os.environ.get("FROMADDRESS")
    password = os.environ.get("APP_PASSWORD")

    subject = f'{date}の空き状況'
    bodyText = text
    fromAddress = os.environ.get("FROMADDRESS")
    toAddress = os.environ.get("TOADDRESS")

    # connect to SMTP server
    smtpobj = smtplib.SMTP('smtp.gmail.com', 587)
    smtpobj.starttls()
    smtpobj.login(sendAddress, password)

    # create email
    msg = MIMEText(bodyText)
    msg['Subject'] = subject
    msg['From'] = fromAddress
    msg['To'] = toAddress
    msg['Date'] = formatdate()

    # send email
    smtpobj.send_message(msg)
    smtpobj.close()

def main():
    date = '2023年2月'
    url = f"https://passmarket.yahoo.co.jp/main/feature/Izuteddybear.html"
    
    # initialize driver
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
    options.add_experimental_option('excludeSwitches', ['enable-logging'])

    driver = webdriver.Chrome(options=options)
    driver.get(url)
    sleep(1)

    # push button
    #driver.find_element_by_xpath('//*[@id="SearchBox_LnkBtnSearch"]').click()
    #sleep(1)

    # check vacancies
    if "【2月】" in driver.find_element_by_xpath('//*[@id="evtlst"]').text:
        text = f"""ぬいぐるみワークショップの2月分が予約可能状態になりました。\n
                url: {url}"""
                
        send_email(date, text)
    else:
        text = f"""ぬいぐるみワークショップ2月分は予約不可状態です。\n
                url: {url}"""
    
        
        
    print(text)
    driver.quit()

if __name__ == "__main__":
    load_dotenv()
    main()