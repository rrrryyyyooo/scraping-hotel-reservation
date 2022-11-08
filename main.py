import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from time import sleep

def main():
    url = "https://reservation.anaihghotels.co.jp/booking/stay_pc/rsv/index.aspx?hi_id=41&lang=ja-JP&PMID=99502222&dt=2022/12/04"
    
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
        print('ng')
    else:
        print('ok')
    
    driver.quit()

if __name__ == "__main__":
    main()