import csv
import time
from selenium import webdriver
from selenium_stealth import stealth
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


options = webdriver.ChromeOptions()
driver = webdriver.Chrome(options=options)

stealth(driver,
        languages=["en-US", "en"],
        vendor="Google Inc.",
        platform="Win32",
        webgl_vendor="Intel Inc.",
        renderer="Intel Iris OpenGL Engine",
        fix_hairline=True)

try:
    # 1. Зайти на https://www.nseindia.com
    driver.get('https://www.nseindia.com/')

    # 2. Навестись (hover) на MARKET DATA
    WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.ID, 'link_2'))).click()

    # 3. Кликнуть на Pre-Open Market
    WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, "//a[text()='Pre-Open Market']"))).click()

    # 4. Спарсить данные Final Price по всем позициям на странице и вывести их в csv файл. Имя;цена
    time.sleep(5)
    WebDriverWait(driver, 20).until(EC.visibility_of_element_located((By.TAG_NAME, 'tbody')))
    table_body = driver.find_element(By.TAG_NAME, 'tbody')
    table_rows = table_body.find_elements(By.TAG_NAME, 'tr')

    with open('result.csv', mode="w", newline="") as file:
        writer = csv.writer(file)
        for row in table_rows[:-1]:
            name_data = row.find_elements(By.XPATH, './/td[2]')
            price_data = row.find_elements(By.XPATH, './/td[7]')

            row_data = [name.text for name in name_data] + [price.text for price in price_data]
            writer.writerow(row_data)

    print('Парсинг завершен')

    # Имитация небольшого пользовательского сценария использования сайта:
    # 1. Зайти на главную страницу
    WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.ID, 'link_0'))).click()
    time.sleep(5)

    # 2. Пролистать вниз до графика
    graf = WebDriverWait(driver, 20).until(EC.visibility_of_element_located((By.XPATH, '//*[@id="NIFTY50"]/div/div/div[1]/div[2]/div/div[2]')))
    driver.execute_script("arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});", graf)
    time.sleep(5)

    # 3. Выбрать график "NIFTY BANK"
    driver.execute_script("window.scrollTo({top: 0, behavior: 'smooth'});")
    time.sleep(5)
    WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="NIFTY BANK"]'))).click()

    # 4. Нажать “View all” под "TOP 5 STOCKS - NIFTY BANK"
    driver.execute_script("arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});", graf)
    time.sleep(5)

    table = WebDriverWait(driver, 20).until(EC.visibility_of_element_located((By.XPATH, '//*[@id="tab4Ganier"]')))
    driver.execute_script("arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});", table)
    time.sleep(5)

    view_all = WebDriverWait(driver, 30).until(EC.visibility_of_element_located((By.XPATH, '//*[@id="tab4_gainers_loosers"]/div[3]/a'))).click()
    time.sleep(10)

    # 5. Выбрать в селекторе “NIFTY ALPHA 50”
    WebDriverWait(driver, 20).until(EC.visibility_of_element_located((By.XPATH, '//*[@id="equitieStockSelect"]')))

    option = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, '//*[@id="equitieStockSelect"]/optgroup[4]/option[7]')))
    driver.execute_script("arguments[0].scrollIntoView();", option)
    option.click()

    time.sleep(10)

    # 6. Пролистать таблицу до конца
    for i in range(1, 5):
        element_to_scroll_to = driver.find_element(By.XPATH, f'//*[@id="equityStockTable"]/tbody/tr[{10*i}]')
        # Выполняем плавную прокрутку к элементу
        driver.execute_script("arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});", element_to_scroll_to)
        time.sleep(1)
    time.sleep(15)
finally:
    driver.quit()
