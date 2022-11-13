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
    date = '2022/12/24'
    url = f"https://reservation.anaihghotels.co.jp/booking/stay_pc/rsv/index.aspx?hi_id=41&lang=ja-JP&PMID=99502222&dt={date}"
    
    # initialize driver
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
    options.add_experimental_option('excludeSwitches', ['enable-logging'])

    driver = webdriver.Chrome(options=options)
    driver.get(url)
    sleep(1)

    # push button
    driver.find_element_by_xpath('//*[@id="SearchBox_LnkBtnSearch"]').click()
    sleep(1)

    # check vacancies
    if driver.find_elements_by_xpath('//*[@id="PNoDataErr"]'):
        text = f"""検索日: {date}
                お探しの条件では、利用できるプラン・客室がございません。条件を変更して再度お探しください。\n
                url: {url}"""
        
    else:
        num = driver.find_element_by_xpath('//*[@id="PnlPlanList"]/div[2]/p/span').text
        text = f"""検索日: {date}
                お探しの条件で{num}件のプランが見つかりました。\n
                url: {url}"""
    
    send_email(date, text)
    print(text)
    
    driver.quit()

if __name__ == "__main__":
    load_dotenv()
    main()