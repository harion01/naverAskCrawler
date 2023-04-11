from datetime import datetime
from selenium import webdriver
import time
import re
import requests
from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By
import json

#검색 쿼리 문자열을 반환합니다.
def get_search_query():
    return "당귀 효능"


#현재 날짜를 형식화된 문자열로 반환합니다.
def get_current_date():
    return datetime.now().strftime("%Y-%m-%d_%H_%M_%S")

#Chrome WebDriver를 시작하고 드라이버 인스턴스를 반환합니다.
def start_chrome_driver():
    path = "chromedriver.exe"
    driver = webdriver.Chrome(path)
    return driver

#WebDriver를 다음 홈페이지로 이동합니다.
def navigate_to_daum(driver):
    driver.get('http://www.daum.net')
    time.sleep(2)

#WebDriver를 사용하여 주어진 쿼리 텍스트를 검색합니다.
def search_query(driver, query_txt):
    element = driver.find_element(By.ID, "q")
    element.send_keys(query_txt)
    element.submit()
    time.sleep(1)

#검색 결과 페이지에서 "블로그" 섹션을 클릭합니다.
def click_blog(driver):
    driver.find_element(By.LINK_TEXT, "블로그").click()

#검색 결과에서 기사 URL을 추출하고 목록으로 반환합니다.
def extract_urls(driver):
    article_raw = driver.find_elements(By.CLASS_NAME, "tit_main")
    daum_news_url_list = [article.get_attribute('href') for article in article_raw]
    time.sleep(1)

    elements = driver.find_elements(By.CLASS_NAME, "tit_main");
    for element in elements:
        text = element.text
        url = element.get_attribute("href")
        # print("Title: ", text)
        # print("URL: ", url)

    return daum_news_url_list

#검색 결과의 블로그 기사 URL을 텍스트 파일에 저장합니다.
def save_urls_to_file(driver, date, max_pages):
    filename = f"result/daum/daum_blogLinkList_{date}.txt"

    for _ in range(max_pages):
        elements = driver.find_elements(By.CLASS_NAME, "tit_main")

        with open(filename, 'a', encoding='utf-8') as file:
            for element in elements:
                title = element.text
                url = element.get_attribute("href")
                file.write("title["+title+"] url["+url+"]\n")

        time.sleep(1)

        try:
            next_button = driver.find_element(By.CSS_SELECTOR, "a.ico_comm1.btn_page.btn_next")
            next_button.click()
            time.sleep(2)
        except Exception as e:
            print("No more pages or error occurred:", e)
            break

    return filename


#텍스트 파일에서 URL을 읽고 제목과 URL을 포함하는 블로그 사전 목록을 반환합니다.
def get_blog_list(file_path):
    blog_list = []
    pattern = r"title\[(.*?)\] url\[(.*?)\]"

    with open(file_path, 'r', encoding='utf-8') as file:
        for line in file:
            match = re.search(pattern, line)
            if match:
                title, url = match.groups()
                blog_list.append({'title': title, 'url': url})

    return blog_list

#여러 클래스 이름을 시도하여 주어진 URL에서 콘텐츠를 검색하는 일반적인 접근 방식을 사용합니다.
def get_content_generic( one_url):
    try:
        response = requests.get(one_url)
    except :
        return None

    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
    else:
        print("Request failed with status code:", response.status_code)
        return None

    content = get_content_by_class(soup, one_url, "entry-content")
    if(content == None) :
        content = get_content_by_class(soup, one_url, "area_view_content")
    if(content == None) :
        content = get_content_by_class(soup, one_url, "article")
    if(content == None) :
        content = get_content_by_class(soup, one_url, "area-view")
    if(content == None) :
        content = get_content_by_class(soup, one_url, "content-width")
    if(content == None) :
        content = get_content_by_class(soup, one_url, "area_view")
    if(content == None) :
        content = get_content_by_class(soup, one_url, "post-body")
    if(content == None) :
        content = get_content_by_class(soup, one_url, "se-main-container")

    if(content == None) :
        print("Failed to parse URL " + one_url);


    return content


#BeautifulSoup 객체에서 지정된 클래스 이름을 검색하여 주어진 URL에서 콘텐츠를 검색합니다.
def get_content_by_class(soup, one_url, class_name):
    try:
        body_element = soup.find(class_=class_name)
        content = body_element.text
        print("success to parse url: " + one_url)
        return content
    except:
        # print(f"Failed to parse URL ({class_name}): " + one_url)
        return None


#JSON 형식의 콘텐츠 데이터를 파일에 저장합니다.
def save_data_to_file(data_list, date):
    content_file_name = f"result/daum/daum_contentList_{date}.txt"

    with open(content_file_name, 'w', encoding='utf-8') as content_file:
        json.dump(data_list, content_file, ensure_ascii=False, indent=2)

#JSON 저장을 위해 정리 및 형식화된 블로그 데이터를 포함하는 데이터 목록을 생성합니다.
def create_data_list(blog_list):
    data_list = []

    for blog in blog_list:
        content = get_content_generic( blog['url'])
        if content:
            # Remove special characters from title and content
            cleaned_title = re.sub(r'[^a-zA-Z0-9가-힣\s]', '', blog['title'])
            cleaned_content = re.sub(r'[^a-zA-Z0-9가-힣\s]', '', content)

            # Remove extra white spaces and newlines
            single_spaced_title = re.sub(r'\s+', ' ', cleaned_title.strip())
            single_spaced_content = re.sub(r'\s+', ' ', cleaned_content.strip())

            data = {
                "prompt": single_spaced_title,
                "completion": single_spaced_content
            }
            data_list.append(data)

    return data_list



#스크립트를 실행하는 다른 모든 함수를 결합하고 실행하는 주요 함수입니다.
def main():
    query_txt = get_search_query()
    date = get_current_date()

    driver = start_chrome_driver()
    navigate_to_daum(driver)
    search_query(driver, query_txt)
    click_blog(driver)

    url_file_name = save_urls_to_file(driver, date, max_pages=1000)  # Adjust max_pages as needed

    blog_list = get_blog_list(url_file_name)
    data_list = create_data_list(blog_list )
    save_data_to_file(data_list, date)
    driver.close()


if __name__ == "__main__":
    main()
