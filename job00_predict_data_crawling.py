from selenium import webdriver as wb
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup as bs
from selenium.webdriver.chrome.options import Options

import re
import random
import time
import pandas as pd
import datetime


def scroll():
    try:
        # 페이지 내 스크롤 높이 받아오기
        last_page_height = driver.execute_script("return document.documentElement.scrollHeight")
        while True:
            # 임의의 페이지 로딩 시간 설정
            # PC환경에 따라 로딩시간 최적화를 통해 scraping 시간 단축 가능
            pause_time = random.uniform(1, 2)
            # 페이지 최하단까지 스크롤
            driver.execute_script("window.scrollTo(0, document.documentElement.scrollHeight);")
            # 페이지 로딩 대기
            time.sleep(pause_time)
            # 무한 스크롤 동작을 위해 살짝 위로 스크롤(i.e., 페이지를 위로 올렸다가 내리는 제스쳐)
            driver.execute_script("window.scrollTo(0, document.documentElement.scrollHeight-50)")
            time.sleep(pause_time)
            # 페이지 내 스크롤 높이 새롭게 받아오기
            new_page_height = driver.execute_script("return document.documentElement.scrollHeight")
            # 스크롤을 완료한 경우(더이상 페이지 높이 변화가 없는 경우)
            if new_page_height == last_page_height:
                print("스크롤 완료")
                break

            # 스크롤 완료하지 않은 경우, 최하단까지 스크롤
            else:
                last_page_height = new_page_height

    except Exception as e:
        print("에러 발생: ", e)


# f-string
options = Options()
key_count = 0

options.add_argument('--start-maximized')


yt_url = 'https://www.youtube.com/'

x_path = '//*[@id="chips"]/yt-chip-cloud-chip-renderer[*]'
driver = wb.Chrome(options)

try:
    driver.get(yt_url)
except:
    print('drivet.get', keyword)

driver.find_element(By.XPATH, '//*[@id="chips"]/yt-chip-cloud-chip-renderer[{}]'.format(7)).click()
time.sleep(2)


scroll()


html = bs(driver.page_source, 'html.parser')
#print(html)

driver.close()

titleList=[]

for content in html.select('a#video-title-link'):
    title = content.get('title')
    title = re.compile('[^가-힣a-zA-Z]').sub(' ', title)


    titleList.append(title)

df_titles = pd.DataFrame()
df_section_title = pd.DataFrame(titleList, columns=['titles'])
df_section_title['category'] = 'game'
df_titles = pd.concat([df_titles, df_section_title], axis='rows', ignore_index=True)
df_titles.to_csv('./predict_data/data_{}_{}.csv'.format('game', datetime.datetime.now().strftime('%Y%m%d')), index=False)




