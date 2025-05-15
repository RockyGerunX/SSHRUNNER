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

# Konfigurasi Chrome Options untuk mode headless
chrome_options = Options()
chrome_options.add_argument("--headless")  # Jalankan dalam mode headless
chrome_options.add_argument("--disable-gpu")  # Nonaktifkan GPU (opsional untuk stabilitas)
chrome_options.add_argument("--no-sandbox")  # Diperlukan untuk beberapa lingkungan server
chrome_options.add_argument("--disable-dev-shm-usage")  # Mengatasi masalah memori di container
chrome_options.add_argument("--disable-notifications")  # Matikan notifikasi

# Inisialisasi WebDriver dengan Chrome
driver = webdriver.Chrome(options=chrome_options)

# Buka halaman zefoy.com
driver.get('https://zefoy.com')

# Tunggu dan terima permintaan notifikasi jika muncul
try:
    WebDriverWait(driver, 10).until(EC.alert_is_present())
    alert = driver.switch_to.alert
    alert.accept()  # Terima notifikasi
except:
    print("Tidak ada notifikasi yang muncul atau sudah ditangani.")

# Tunggu dan tutup pop-up iklan (sesuaikan selector jika ada ID/kelas spesifik)
try:
    ad_popup = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, "//button[contains(text(), 'Close') or contains(text(), 'Oke')]"))
    )
    ad_popup.click()  # Tutup pop-up iklan
except:
    print("Tidak ada pop-up iklan yang terdeteksi atau gagal ditutup.")

# Tunggu hingga elemen CAPTCHA muncul (sesuaikan selector dengan struktur situs)
try:
    captcha_image = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, 'captcha_image_id'))  # Ganti ID sesuai situs
    )
    captcha_input = driver.find_element_by_name('captcha_input')  # Ganti nama sesuai situs

    # Ambil screenshot gambar CAPTCHA
    captcha_image.screenshot('captcha.png')

    # Baca teks dari gambar menggunakan Pytesseract
    image = Image.open('captcha.png')
    captcha_text = pytesseract.image_to_string(image, config='--psm 8 --oem 3')

    print("Teks CAPTCHA yang terdeteksi:", captcha_text.strip())

    # Masukkan teks ke input CAPTCHA
    captcha_input.send_keys(captcha_text.strip())

    # Klik tombol submit (sesuaikan selector)
    submit_button = driver.find_element_by_name('submit')  # Ganti nama sesuai situs
    submit_button.click()

except Exception as e:
    print("Error:", e)

# Tunggu beberapa detik untuk melihat hasil
time.sleep(5)

# Tutup browser
driver.quit()

# Hapus file sementara
if os.path.exists('captcha.png'):
    os.remove('captcha.png')
