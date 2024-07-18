from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import time

URL = "https://www.amazon.com/s?k=deals"
# يمكن تعديل XPath بناءً على الموقع الفعلي للصفقة على صفحة أمازون
DEALS_XPATH = "//div[contains(@class, 's-main-slot')]//div[@data-component-type='s-search-result']"

def fetch_amazon_deals():
    chrome_options = Options()
    chrome_options.add_argument("--headless")  # تشغيل في وضع عدم العرض
    chrome_options.add_argument("--disable-gpu")  # تعطيل استخدام GPU
    chrome_options.add_argument("--no-sandbox")  # تعطيل وضع الساند بوكس
    chrome_options.add_argument("--disable-dev-shm-usage")  # تعطيل استخدام /dev/shm

    driver = webdriver.Chrome(options=chrome_options)
    driver.get(URL)

    time.sleep(5)  # انتظار تحميل الصفحة

    deals = driver.find_elements(By.XPATH, DEALS_XPATH)
    deal_list = []

    for deal in deals:
        try:
            title = deal.find_element(By.XPATH, ".//span[@class='a-size-medium']").text
            link = deal.find_element(By.XPATH, ".//a[@class='a-link-normal']").get_attribute("href")
            deal_list.append({"title": title, "link": link})
        except Exception as e:
            print(f"Error extracting deal: {e}")

    driver.quit()

    if deal_list:
        store_deals(deal_list)

def store_deals(deal_list):
    with open("deals.txt", "w", encoding="utf-8") as f:
        for deal in deal_list:
            f.write(f"Title: {deal['title']}\nLink: {deal['link']}\n\n")

def main():
    print("Starting the bot...")
    while True:
        print("Fetching Amazon deals...")
        fetch_amazon_deals()
        print("Fetched and stored Amazon deals.")
        print("Sleeping for 1 minute...")
        time.sleep(60)

if __name__ == "__main__":
    main()
