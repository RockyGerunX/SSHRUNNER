from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from PIL import Image
import pytesseract
from io import BytesIO
import time
import os

chrome_options = Options()
chrome_options.add_argument("--headless")
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")
chrome_options.add_argument("--disable-notifications")

driver = webdriver.Chrome(options=chrome_options)

driver.get('https://zefoy.com')

try:
    WebDriverWait(driver, 10).until(EC.alert_is_present())
    alert = driver.switch_to.alert
    alert.accept()
except:
    print("Tidak ada notifikasi yang muncul atau sudah ditangani.")

try:
    ad_popup = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, "//button[contains(text(), 'Close') or contains(text(), 'Oke')]"))
    )
    ad_popup.click()
except:
    print("Tidak ada pop-up iklan yang terdeteksi atau gagal ditutup.")

try:
    captcha_image = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, 'captcha_image_id'))
    )
    captcha_input = driver.find_element_by_name('captcha_input')

    captcha_image.screenshot('captcha.png')

    image = Image.open('captcha.png')
    captcha_text = pytesseract.image_to_string(image, config='--psm 8 --oem 3')

    print("Teks CAPTCHA yang terdeteksi:", captcha_text.strip())

    captcha_input.send_keys(captcha_text.strip())

    submit_button = driver.find_element_by_name('submit')
    submit_button.click()

except Exception as e:
    print("Error:", e)

time.sleep(5)

driver.quit()

if os.path.exists('captcha.png'):
    os.remove('captcha.png')
