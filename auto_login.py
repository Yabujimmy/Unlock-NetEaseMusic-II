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
    browser.add_cookie({"name": "MUSIC_U", "value": "00A22E26FEA38DCAA8F2F2DD0B6AAF02F882F59318AD44A0D48DF25AFAE15760028BD89B2E0061CCFA267FD0A4B20661284D7A9797E65245DEDED14AD807F7A841692E9BF0CCC7BA43CEE9FE22AD88AFA1E36B3E75A63718E4485B4FE1DE7892EFE04562BD02AA07C9838E158F6A1FBA143A364306713563936A63AB1B9C53667AA15BC84AED04D1E046F82431A6E5EB151BCAA6111E1F697BF168FC94D34B16DE9F28393C401D015A3CEAF3D55DEA12D1CEED2CEA1D9704242DDE60E036CCB7E38D092DCB38AB4A86E55E38CBB6802F9E68AB5F67B5270079904B380ED37C620163A97F549CE9555BD4D066E8CF4474BA6597DE0E919377CF5092E9DC32CE8D858CDBD479739132CACC8C125CB83CE21A98A0E03856013A47B1B8BC3C4F53A1D61A38FA0F6B437E2EC76A5226FAFF736B25850CD67255B4FA289A25C7D14B1649AC998572C3CCB4246AA3F05E0CE1D27BAA88C93A737FCCD4AF408D9FAC7F7D48"})
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
