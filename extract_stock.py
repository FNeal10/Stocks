import os
from time import sleep
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

# URL of the stock page
url = "https://www.pse.com.ph/company-information-BDO/"

# Initialize WebDriver
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
wait_time = WebDriverWait(driver, 20)

def get_open_price():

    openPriceElement = driver.find_element(By.XPATH,"/html/body/div/div/div/div[3]/div[1]/div/div[3]/table/tbody/tr[1]/td[4]")
    return openPriceElement.text

def get_high_price():
    highPriceElement = driver.find_element(By.XPATH, "/html/body/div/div/div/div[3]/div[1]/div/div[3]/table/tbody/tr[2]/td[4]")
    return highPriceElement.text

def get_low_price():
    lowPriceElement = driver.find_element(By.XPATH, "/html/body/div/div/div/div[3]/div[1]/div/div[3]/table/tbody/tr[3]/td[4]")
    return lowPriceElement.text

def get_close_price():
    closeElement = driver.find_element(By.XPATH, "/html/body/div/div/div/div[3]/div[1]/div/div[3]/table/tbody/tr[1]/td[6]")
    return closeElement.text

def get_volume():
    volumeElement = driver.find_element(By.XPATH, "/html/body/div/div/div/div[3]/div[1]/div/div[3]/table/tbody/tr[3]/td[2]")
    return volumeElement.text

def main():
    try:
        print("Start")
        driver.get(url)

        iframe = wait_time.until(EC.presence_of_element_located((By.ID, "company_infos")))
        driver.switch_to.frame(iframe)
        
        openPrice = get_open_price()
        highPrice = get_high_price()
        lowPrice = get_low_price()
        closePrice = get_close_price()
        volume = get_volume()


        # Extract and print text
        print("Open Price:", openPrice)
        print("High Price:", highPrice)
        print("Low Price:", lowPrice)
        print("Close Price:", closePrice)
        print("Volume:", volume)

    except Exception as e:
        print("Error:", e)

    finally:
        driver.quit()  # Ensure the browser is closed after execution

if __name__ == "__main__":
    main() 
