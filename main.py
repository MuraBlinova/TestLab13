from selenium import webdriver

def start_work():
    driver = webdriver.Firefox()
    print(driver)
    adress = "https://ru.spbtv.com"
    driver.get(adress)
    driver.implicitly_wait(5)  # seconds
