from selenium import webdriver
from bs4 import BeautifulSoup
from datetime import datetime
import time
from selenium.webdriver.common.by import By


from random import uniform


def main():
    chrome_options = webdriver.ChromeOptions()
    driver = webdriver.Chrome(options=chrome_options)

    date = datetime.now().strftime("%Y-%m-%d_%H_%M_%S")
    filename = f"result/mediGate/url_list_medigate_IssueList_{date}.txt"

    with open(filename, 'w') as fname:
        page_url = []

        for pageIndex in range(3) :
            time.sleep(uniform(0.01, 1.0))
            ##medigate issue list
            url = f'https://www.medicaltimes.com/Main/News/List_Opinion.html?page={pageIndex}&MainCate=7&SubCate=70&TargetDate=&keyword='
            driver.get(url)

            articleList = driver.find_elements(By.CLASS_NAME, "newsList_cont.clearfix")

            for n, article in enumerate(articleList):
                title = article.find_element(By.CLASS_NAME, "headLine").text
                text = article.find_element(By.CLASS_NAME, "list_txt").text
                fname.write(title + "\n" + text +"\n\n")

                soup = BeautifulSoup(text, 'html.parser')
                list_txt_div = soup.find('div', class_='list_txt')
                item1_text = list_txt_div.find('span').text
                full_text = list_txt_div.text.strip()


    fname.close()
    driver.close()


if __name__ == "__main__":
    main()