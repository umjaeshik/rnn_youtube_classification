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

keywords = ['music','음악','game','게임','sports','스포츠','cook','요리','pets','애완동물','nature','자연']
key_count = 0
options = Options()
options.add_argument('--start-maximized')

for keyword in keywords:

    yt_url = f'https://www.youtube.com/results?search_query={keyword}'
    driver = wb.Chrome(options=options)
    try:
        driver.get(yt_url)
    except:
        print('drivet.get', keyword)
        continue
    time.sleep(2)

    scroll()
    html = bs(driver.page_source, 'html.parser')
    #print(html)

    driver.close()
    if key_count % 2 == 0:
        titleList=[]

    for content in html.select('a#video-title'):
        title = content.get('title')
        title = re.compile('[^가-힣a-zA-Z]').sub(' ', title)

        titleList.append(title)

    key_label_num =2*int(key_count/2)

    if key_count % 2 == 1:

        df_titles = pd.DataFrame()
        df_section_title = pd.DataFrame(titleList, columns=['titles'])
        df_section_title['category'] = keywords[key_label_num]
        df_titles = pd.concat([df_titles, df_section_title], axis='rows', ignore_index=True)
        df_titles.to_csv('./data/data_{}_{}.csv'.format(keywords[key_count-1], datetime.datetime.now().strftime('%Y%m%d')), index=False)
        titleList=[]
    key_count += 1


