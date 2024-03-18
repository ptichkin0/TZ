from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium_stealth import stealth
from selenium import webdriver
from bs4 import BeautifulSoup
import zipfile
import random
import time


# Параметры для входа
email = ""
password = ''
username = ''

# Параметры прокси
PROXY_HOST = ''
PROXY_PORT = 0
PROXY_USER = ''
PROXY_PASS = ''

manifest_json = """
{
    "version": "1.0.0",
    "manifest_version": 2,
    "name": "Chrome Proxy",
    "permissions": [
        "proxy",
        "tabs",
        "unlimitedStorage",
        "storage",
        "<all_urls>",
        "webRequest",
        "webRequestBlocking"
    ],
    "background": {
        "scripts": ["background.js"]
    },
    "minimum_chrome_version":"22.0.0"
}
"""

background_js = """
var config = {
        mode: "fixed_servers",
        rules: {
        singleProxy: {
            scheme: "http",
            host: "%s",
            port: parseInt(%s)
        },
        bypassList: ["localhost"]
        }
    };

chrome.proxy.settings.set({value: config, scope: "regular"}, function() {});

function callbackFn(details) {
    return {
        authCredentials: {
            username: "%s",
            password: "%s"
        }
    };
}

chrome.webRequest.onAuthRequired.addListener(
            callbackFn,
            {urls: ["<all_urls>"]},
            ['blocking']
);
""" % (PROXY_HOST, PROXY_PORT, PROXY_USER, PROXY_PASS)

word = '@elonmusk'

def get_chromedriver(use_proxy=False, user_agent=None):
    chrome_options = webdriver.ChromeOptions()

    if use_proxy:
        plugin_file = 'proxy_auth_plugin.zip'

        with zipfile.ZipFile(plugin_file, 'w') as zp:
            zp.writestr('manifest.json', manifest_json)
            zp.writestr('background.js', background_js)

        chrome_options.add_extension(plugin_file)

    if user_agent:
        chrome_options.add_argument(f'--user-agent={user_agent}')

    chrome_options.add_argument("--start-maximized")
    driver = webdriver.Chrome(options=chrome_options)
    # Настройка selenium-stealth
    stealth(driver,
            languages=["en-US", "en"],
            vendor="Google Inc.",
            platform="Win32",
            webgl_vendor="Intel Inc.",
            renderer="Intel Iris OpenGL Engine",
            fix_hairline=True)

    return driver


def scraping(pagesource):
    # Парсим собранный HTML-код

    bs = BeautifulSoup(pagesource, 'html.parser')
    # создаем пустой список твитов
    tweet_list = []

    for tweets in bs.find_all('div',
                              class_='css-1rynq56 r-8akbws r-krxsd3 r-dnmrzs r-1udh08x r-bcqeeo r-qvutc0 r-37j5jr r-a023e6 r-rjixqe r-16dba41 r-bnwqim'):
        tweet_content = tweets.get_text(separator=' ', strip=True)
        tweet_list.append(tweet_content)

    # Убираем повторы
    unique_tweets = list(dict.fromkeys(tweet_list))
    result_tweet = unique_tweets[:10]

    # Выводим результаты с нумерацией
    for index, tweet in enumerate(result_tweet, start=1):
        print(f"{index}. {tweet}")


def main():
    driver = get_chromedriver(use_proxy=True, user_agent='Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36')
    driver.get('https://twitter.com/i/flow/login')
    time.sleep(10)
    # Ввод email
    element = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH,
                                                                              '//input[@class="r-30o5oe r-1dz5y72 r-13qz1uu r-1niwhzg r-17gur6a r-1yadl64 r-deolkf r-homxoj r-poiln3 r-7cikom r-1ny4l3l r-t60dpp r-fdjqy7"]')))
    # Имитация ввода
    for letter in email:
        element.send_keys(letter)
        time.sleep(0.1)
    time.sleep(5)

    WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH,
                                                                '//*[@id="layers"]/div/div/div/div/div/div/div[2]/div[2]/div/div/div[2]/div[2]/div/div/div/div[6]'))).click()
    time.sleep(15)

    # Могут попросить имя
    h = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, '//*[@id="modal-header"]/span/span')))
    if h.text == 'Enter your phone number or username':
        username_input = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH,
                                                                                         '//input[@class="r-30o5oe r-1dz5y72 r-13qz1uu r-1niwhzg r-17gur6a r-1yadl64 r-deolkf r-homxoj r-poiln3 r-7cikom r-1ny4l3l r-t60dpp r-fdjqy7"]')))
        # Имитация ввода
        for i in username:
            username_input.send_keys(i)
            time.sleep(0.1)
        time.sleep(5)
        username_input.send_keys(Keys.ENTER)
    time.sleep(15)

    # Ввод password и вход
    password_input = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH,
                                                                                     '//input[@class="r-30o5oe r-1dz5y72 r-13qz1uu r-1niwhzg r-17gur6a r-1yadl64 r-deolkf r-homxoj r-poiln3 r-7cikom r-1ny4l3l r-t60dpp r-fdjqy7"]')))
    # Имитация ввода
    for s in password:
        password_input.send_keys(s)
        time.sleep(0.1)
    time.sleep(5)
    password_input.send_keys(Keys.ENTER)
    time.sleep(20)



    # Ищем Илона
    search = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH,
                                                                             '//*[@id="react-root"]/div/div/div[2]/main/div/div/div/div[2]/div/div[2]/div/div/div/div[1]/div/div/div/form/div[1]/div/div/div/label/div[2]/div/input')))

    for s in word:
        search.send_keys(s)
        time.sleep(0.1)
    time.sleep(5)

    # Выбираем первого
    WebDriverWait(driver, 20).until(
        EC.presence_of_element_located((By.XPATH, '//*[@id="typeaheadDropdown-1"]/div[4]/div'))).click()
    time.sleep(5)

    pagesource = ''

    # Скроллим посты, чтобы прогрузить
    for i in range(0, 15):
        driver.execute_script("window.scrollTo({ top: window.pageYOffset + 200, behavior: 'smooth' });")
        sleep_time = random.uniform(0.2, 0.5)
        time.sleep(sleep_time)
        pagesource += driver.page_source
        time.sleep(2)
    time.sleep(5)

    driver.quit()

    # Парсим прогруженную страничку
    scraping(pagesource)


if __name__ == '__main__':
    main()