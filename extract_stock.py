import pandas as pd

from read_from_blob import *
from time import sleep
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
wait_time = WebDriverWait(driver, 20)

def get_stocks_list():
    data = get_urls()
    return data

def update_history(company: str, data: list):
    history = pd.read_csv(f"History/{company}.csv")
    new_data = pd.DataFrame([data], columns=history.columns)
    
    new_data = pd.concat([new_data, history], ignore_index=True)
    new_data.to_csv(f"History/{company}.csv", index=False)  


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
        current_date = datetime.now().strftime('%m/%d/%Y')

        data = get_stocks_list()
        for _, d in data.iterrows():
            company = d.CODE
            url = d.URL
            
            print(f"Processing {company}")
            driver.get(url)

            iframe = wait_time.until(EC.presence_of_element_located((By.ID, "company_infos")))
            driver.switch_to.frame(iframe)
            
            openPrice = get_open_price()
            highPrice = get_high_price()
            lowPrice = get_low_price()
            closePrice = get_close_price()
            volume = get_volume()

            print(f"Updating records for {company}")
            update_history(company,[current_date, openPrice, highPrice, lowPrice,
                                    closePrice, volume])
            
            sleep(2)
    except Exception as e:
        print("Error:", e)

    finally:
        driver.quit()

if __name__ == "__main__":
    main()