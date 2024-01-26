import time
from selenium import webdriver as wb

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

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



def get_image_title(url):
    # 웹 드라이버 초기화

    driver = wb.Chrome()

    driver.implicitly_wait(5)  # or bigger second

    # 열고자 하는 채널 -> 동영상 목록으로 된 url 페이지를 엶
    driver.get(url)

    image_list = list()  # 썸네일을 받을 수 있는 주소 저장용 리스트
    title_list = list()  # 썸네일 제목을 저장하는 리스트

    idx = 1
    while True:
        try:
            img_xpath = '/html/body/ytd-app/div/ytd-page-manager/ytd-browse/ytd-two-column-browse-results-renderer/div[1]/ytd-section-list-renderer/div[2]/ytd-item-section-renderer/div[3]/ytd-grid-renderer/div[1]/ytd-grid-video-renderer[' + str(
                idx) + ']/div[1]/ytd-thumbnail/a/yt-img-shadow/img'
            title_xpath = '/html/body/ytd-app/div/ytd-page-manager/ytd-browse/ytd-two-column-browse-results-renderer/div[1]/ytd-section-list-renderer/div[2]/ytd-item-section-renderer/div[3]/ytd-grid-renderer/div[1]/ytd-grid-video-renderer[' + str(
                idx) + ']/div[1]/div[1]/div[1]/h3/a'

            # 이미지가 곧바로 로드 되지 않을 때, 20초간 강제로 기다림
            img = WebDriverWait(driver, 20).until(EC.presence_of_all_elements_located((By.XPATH, img_xpath)))
            if img is None:
                print(idx, 'img is not loaded.')

            # 한 페이지에 약 8개 불러오는 데, 동영상 목록을 추가 불러오기 위해 스크롤 내림
            if idx % 8 == 0:
                driver.execute_script('window.scrollBy(0, 1080);')
                time.sleep(2)
                driver.execute_script('window.scrollBy(0, 1080);')
                time.sleep(2)
                driver.execute_script('window.scrollBy(0, 1080);')
                time.sleep(2)

            # 썸네일 주소를 리스트에 저장
            image = driver.find_element_by_xpath(img_xpath)
            img_url = image.get_attribute('src')
            image_list.append(img_url)

            # 타이틀을 리스트에 저장
            title = driver.find_element_by_xpath(title_xpath)
            print(idx, title.text, img_url)
            title_list.append(title.text)

            idx += 1
        except Exception as e:
            print()
            print(e)
            break
    assert len(image_list) == len(title_list)
    driver.close()
    return image_list, title_list


# 자이언트 펭TV


keywords = ['music','음악','game','게임','sports','스포츠','cook','요리','pets','애완동물','nature','자연']
key_count = 0

image1= []
title1= []

for keyword in keywords:

    yt_url = f'https://www.youtube.com/results?search_query={keyword}'
    driver = wb.Chrome()
    try:
        image1, title1= get_image_title(yt_url)

    except:
        print('drivet.get', keyword)

    time.sleep(2)
    print(image1, title1)
