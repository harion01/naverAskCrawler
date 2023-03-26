from selenium import webdriver
from datetime import datetime
import time
from selenium.webdriver.common.by import By


from random import uniform


def main():
    chrome_options = webdriver.ChromeOptions()
    driver = webdriver.Chrome(options=chrome_options)

    date = datetime.now().strftime("%Y-%m-%d_%H_%M_%S")
    filename = f"result/mediGate/url_list_medigate_IssueList_{date}.txt"

    with open(filename, 'w', encoding='utf-8') as fname:
        page_url = []

        for pageIndex in range(100) :
            time.sleep(uniform(0.01, 1.0))
            ##medigate issue list
            url = f'https://www.medicaltimes.com/Main/News/List_Opinion.html?page={pageIndex}&MainCate=7&SubCate=70&TargetDate=&keyword='
            try:
                driver.get(url)
            except :
                break

            html = driver.page_source
            articleList = driver.find_elements(By.CLASS_NAME, "newsList_cont.clearfix")

            for n, article in enumerate(articleList):
                title = article.find_element(By.CLASS_NAME, "headLine").text
                list_txt_div  = article.find_element(By.CSS_SELECTOR, ".list_txt")
                span_text = list_txt_div.find_element(By.CSS_SELECTOR, "span").text
                full_text = list_txt_div.text.strip()
                articleText = full_text.replace(span_text, '').strip()
                fname.write(title + "\n" + articleText +"\n\n")


    fname.close()
    driver.close()


if __name__ == "__main__":
    main()