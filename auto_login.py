# coding: utf-8

import os
import time
import logging
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from retrying import retry

# Configure logging
logging.basicConfig(level=logging.INFO, format='[%(levelname)s] %(asctime)s %(message)s')

@retry(wait_random_min=5000, wait_random_max=10000, stop_max_attempt_number=3)
def enter_iframe(browser):
    logging.info("Enter login iframe")
    time.sleep(5)  # 给 iframe 额外时间加载
    try:
        iframe = WebDriverWait(browser, 10).until(
            EC.presence_of_element_located((By.XPATH, "//*[starts-with(@id,'x-URS-iframe')]")
        ))
        browser.switch_to.frame(iframe)
        logging.info("Switched to login iframe")
    except Exception as e:
        logging.error(f"Failed to enter iframe: {e}")
        browser.save_screenshot("debug_iframe.png")  # 记录截图
        raise
    return browser

@retry(wait_random_min=1000, wait_random_max=3000, stop_max_attempt_number=5)
def extension_login():
    chrome_options = webdriver.ChromeOptions()

    logging.info("Load Chrome extension NetEaseMusicWorldPlus")
    chrome_options.add_extension('NetEaseMusicWorldPlus.crx')

    logging.info("Initializing Chrome WebDriver")
    try:
        service = Service(ChromeDriverManager().install())  # Auto-download correct chromedriver
        browser = webdriver.Chrome(service=service, options=chrome_options)
    except Exception as e:
        logging.error(f"Failed to initialize ChromeDriver: {e}")
        return

    # Set global implicit wait
    browser.implicitly_wait(20)

    browser.get('https://music.163.com')

    # Inject Cookie to skip login
    logging.info("Injecting Cookie to skip login")
    browser.add_cookie({"name": "MUSIC_U", "value": "003B7E840150ED9D3ACC076C84DE3513B5BEE6A24B3772DACBB71D9EBA064916073C7E3D0D044D41E7D1C693D7D1776FDC38F8C650C28ACFD586D04C96363DBBD84B202E05DDDA471104BBF88580132753BA2E8EBB31E7DE4B705F2F8A2D947633A02F145847CE22A4C7E9A94A6BC6AE7FE33FE845F1D1EB739432B882D6B5550F636FD419C7BFD99AAF1BC433BC35523F7CB29A942F185AC094F9BFC9A747E784349D6B16FA71D615CDE81605D7F18ED69B06EC01A9833C4CFC355D8D4EB295ED7B872A9A557BE060EBC65A4F3847500B56E469639F93D0936972A0D3D1AB6BCC2A52EBA1C220D5EB48F67258E0EA158EF286066BC5C780E439D5318EDD3BA566D54166C0CF6BBD79CEA1E070F8AFCB357E4255546D009590F5AEEF50393E7DECA3FB8AD2A35B0417B236F5C16CF77E37E2BB4A6FFD3447F3656EC23FBF080601759E4992E334D5B367CCCC92013460497A3F1EACC713401149779B92A9E84B94"})
    browser.refresh()
    time.sleep(5)  # Wait for the page to refresh
    logging.info("Cookie login successful")

    # Confirm login is successful
    logging.info("Unlock finished")

    time.sleep(10)
    browser.quit()


if __name__ == '__main__':
    try:
        extension_login()
    except Exception as e:
        logging.error(f"Failed to execute login script: {e}")
