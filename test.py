from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
from webdriver_manager.chrome import ChromeDriverManager

driver = webdriver.Chrome(ChromeDriverManager().install())
driver.get("http://127.0.0.1:5000/")

email = driver.find_element_by_id("email")
email.send_keys("gustavo.penagos")

password = driver.find_element_by_id("password")
password.send_keys("gustavo")

password.send_keys(Keys.ENTER)

time.sleep(3)

driver.close()