import os
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException, NoAlertPresentException
import pytesseract
from PIL import Image
from io import BytesIO

pytesseract.pytesseract.tesseract_cmd = '/usr/bin/tesseract'

def log(message, status="[INFO]"):
    timestamp = time.strftime("%H:%M:%S", time.localtime())
    print(f"{timestamp} {status} {message}")

def handle_captcha(driver):
    max_attempts = 3
    for attempt in range(1, max_attempts + 1):
        log(f"Attempt {attempt}/{max_attempts} to solve CAPTCHA", "[WAITING]")
        try:
            log("Waiting for CAPTCHA image element", "[WAITING]")
            captcha_image = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, '/html/body/div[5]/div[2]/form/div/div/img'))
            )
            log("CAPTCHA image detected", "[SUCCESS]")

            log("Waiting for CAPTCHA input element", "[WAITING]")
            captcha_input = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, '/html/body/div[5]/div[2]/form/div/div/div/input'))
            )
            log("CAPTCHA input detected", "[SUCCESS]")

            log("Waiting for submit button", "[WAITING]")
            submit_button = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, '/html/body/div[5]/div[2]/form/div/div/div/div/button'))
            )
            log("Submit button detected", "[SUCCESS]")

            log("Capturing CAPTCHA image", "[WAITING]")
            captcha_png = captcha_image.screenshot_as_png
            image = Image.open(BytesIO(captcha_png))
            log("CAPTCHA image captured", "[SUCCESS]")

            log("Processing CAPTCHA text with OCR", "[WAITING]")
            captcha_text = pytesseract.image_to_string(image, config='--psm 8 --oem 3').strip().lower()
            log(f"Detected CAPTCHA text: {captcha_text}", "[SUCCESS]")

            log("Entering CAPTCHA text", "[WAITING]")
            captcha_input.clear()
            captcha_input.send_keys(captcha_text)
            submit_button.click()
            log("Submitted CAPTCHA", "[SUCCESS]")

            log("Verifying CAPTCHA result", "[WAITING]")
            try:
                WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.ID, 'errorcapthcaclose')))
                log("CAPTCHA verification failed", "[WARNING]")
                return False
            except (TimeoutException, NoSuchElementException):
                log("CAPTCHA passed successfully!", "[SUCCESS]")
                return True

        except Exception as e:
            log(f"Error handling CAPTCHA: {e}", "[WARNING]")
            if attempt == max_attempts:
                return False
            log("Retrying CAPTCHA in 2 seconds...", "[WAITING]")
            time.sleep(2)
            driver.refresh()
            log("Page refreshed", "[SUCCESS]")

    return False

def main():
    log("Starting Zefoy CAPTCHA automation")
    log("Current time: 07:46 AM WIB, Thursday, May 15, 2025")
    log("GitHub Runner Version: 2.323.0")

    log("Configuring Chrome for headless mode", "[WAITING]")
    chrome_options = Options()
    chrome_options.add_argument("--headless=new")
    chrome_options.add_argument("--disable-notifications")
    chrome_options.add_argument("--disable-popup-blocking")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    log("Chrome configuration completed", "[SUCCESS]")

    log("Initializing Chrome driver", "[WAITING]")
    driver = webdriver.Chrome(options=chrome_options)
    log("Chrome driver initialized", "[SUCCESS]")

    try:
        log("Navigating to https://zefoy.com", "[WAITING]")
        driver.get('https://zefoy.com')
        log("Successfully opened zefoy.com", "[SUCCESS]")

        log("Checking for notification alert", "[WAITING]")
        try:
            WebDriverWait(driver, 5).until(EC.alert_is_present())
            alert = driver.switch_to.alert
            alert.accept()
            log("Notification alert accepted", "[SUCCESS]")
        except NoAlertPresentException:
            log("No notification alert detected", "[INFO]")

        log("Checking for ad popup", "[WAITING]")
        try:
            ad_popup = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Oke') or contains(text(), 'Close')]"))
            )
            ad_popup.click()
            log("Ad popup closed", "[SUCCESS]")
        except (TimeoutException, NoSuchElementException):
            log("No ad popup detected or failed to close", "[INFO]")

        log("Starting CAPTCHA solving process", "[INFO]")
        if handle_captcha(driver):
            log("CAPTCHA process completed successfully", "[SUCCESS]")
        else:
            log("Failed to pass CAPTCHA after maximum attempts", "[WARNING]")

    except Exception as e:
        log(f"Critical error occurred: {e}", "[WARNING]")
    finally:
        log("Closing browser", "[WAITING]")
        driver.quit()
        log("Browser closed, automation finished", "[SUCCESS]")

if __name__ == "__main__":
    main()
