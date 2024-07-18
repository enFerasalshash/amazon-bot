from selenium import webdriver
from selenium.webdriver.chrome.options import Options

chrome_options = Options()
chrome_options.add_argument("--headless")
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")

print("Starting ChromeDriver...")
driver = webdriver.Chrome(options=chrome_options)
driver.get("https://www.google.com")
print("Page title is:", driver.title)
driver.quit()
