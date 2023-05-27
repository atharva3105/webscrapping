from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.print_page_options import PrintOptions
from PIL import Image
from pytesseract import pytesseract
import os
import time
from PIL import Image
import io
import cv2
import json







chrome_options = Options()
# chrome_options.add_extension(extension_path)
chrome_options.add_experimental_option("prefs", {
    # 'printing.print_preview_sticky_settings.appState': json.dumps(settings),
    "plugins.always_open_pdf_externally": False,
    "download.default_directory": "Z:\web scraping\Election LIst  scraping\pdf"
})

# chrome_options.add_argument('--kiosk-printing')

# chrome_options.add_argument("--headless")  # Run Chrome in headless mode
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("--print-to-pdf")

url = "https://ceoelection.maharashtra.gov.in/searchlist/"
xpath_dist = '//*[@id="ctl00_Content_DistrictList"]'
xpath_assm_con = '//*[@id="ctl00_Content_AssemblyList"]'
xpath_part = '//*[@id="ctl00_Content_PartList"]'


def get_driver(URL):
    webdriver_path = "E:\chromedriver_win32\\chromedriver.exe"
    driver = webdriver.Chrome(executable_path=webdriver_path ,options=chrome_options)
    driver.execute_script('window.open = function(url, name, features) { window.location.href = url; }')
    driver.get(URL)
    return driver


def get_dropdown_list(xpath, driver):
    dropdown_element = driver.find_element(By.XPATH, xpath)
    dropdown = Select(dropdown_element)
    all_options = dropdown.options
    x = 1
    output = []
    for option in all_options:
        if x == 1:
            x += 1
        else:
            output.append(option.text)
    return output


def select_option(xpath, option, driver):
    dropdown_element = driver.find_element(By.XPATH, xpath)
    dropdown = Select(dropdown_element)
    dropdown.select_by_visible_text(option)
    
def get_captcha(d):
    image_element = d.find_element(By.XPATH,'//*[@id="aspnetForm"]/div[3]/article/table/tbody/tr[6]/td[2]/img')
    image_screenshot = image_element.screenshot_as_png
    screenshot = Image.open(io.BytesIO(image_screenshot))
    screenshot.save("img.png")
    
def delete_captcha():
    file_path = 'Z:\web scraping\Election LIst  scraping\img.png'
    os.remove(file_path)
    
def get_captcha_text(d):
    get_captcha(d)
    path_to_tesseract = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
    pytesseract.tesseract_cmd = path_to_tesseract
    img  = cv2.imread("img.png")
    gry = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    (h, w) = gry.shape[:2]
    gry = cv2.resize(gry, (w*4, h*4))
    clss = cv2.morphologyEx(gry, cv2.MORPH_CLOSE, None)
    thr = cv2.threshold(clss, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]
    text = pytesseract.image_to_string(thr)

    return text

def fill_captcha(d,text):
    text_box = d.find_element(By.XPATH, '//*[@id="ctl00_Content_txtcaptcha"]')
    text_box.clear()
    text_box.send_keys(text)
    
def download_pdf(d):
    download_link = d.find_element(By.XPATH ,'//*[@id="ctl00_Content_OpenButton"]')
    download_link.click()
    
def fill_cap_err(d,text):
    fill_captcha(d,text=text)
    try:
        d.switch_to.window(d.window_handles[1])
        alert = d.switch_to.alert
        alert.accept()
        text = get_captcha_text(d)
        time.sleep(1)
        d.switch_to.window(d.window_handles[0])
        d.close()
        time.sleep(1)
        d.switch_to.window(d.window_handles[0])
        time.sleep(1)
        fill_cap_err(d,text)
    except:
         print('NO alert')

    
    

path = '//*[@id="ctl00_Content_DistrictList"]'
d = get_driver(url)



select_option(xpath_dist,'Akola',d)
select_option(xpath_assm_con,'32 - Murtizapur (SC)',d)
select_option(xpath_part,'1 - Viravada',d)
txt = get_captcha_text(d)
print(txt)
time.sleep(1)
fill_cap_err(d=d,text=txt)
time.sleep(10)
# d.switch_to.window(d.window_handles[1])
d.switch_to.window(d.window_handles[-1])












# download_pdf(d)


# output ={}
# for dist in data:
#     select_option(xpath_dist,dist,d)
#     assm_const = get_dropdown_list(xpath_assm_con,d)
#     o2 = {}
#     for assm in assm_const:
#         select_option(xpath_assm_con , assm ,d)
#         parts = get_dropdown_list(xpath_part,d)
#         o2[assm]=parts
#     output[dist] =o2

# with open("sample.json", "w") as outfile:
#     json.dump(output, outfile)


# print(output)


# driver.quit()


# print(get_captcha_text(d))







