import logging

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

log_dir = "logs"
log_filename = os.path.join(log_dir, f"log_{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.txt")
logging.basicConfig(
    filename=log_filename,
    level=logging.DEBUG,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

def get_stocks_list():
    data = get_urls()
    return data


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


def init_driver():
    options = webdriver.ChromeOptions()
    options.add_argument('--headless--')

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    return driver

def extract_stock_prices(driver, company, xpath):
    element = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, xpath)))
    return element.text.replace('"','').strip()

def main():
    try:
        logging.info(f"Starting application.....") 
        current_date = datetime.now().strftime('%m/%d/%Y')

        data = get_stocks_list()
        for _, d in data.iterrows():
            try:
                company = d.CODE
                url = d.URL
                
                logging.info(f"Processing {company}")
                driver.get(url)

                iframe = wait_time.until(EC.presence_of_element_located((By.ID, "company_infos")))
                driver.switch_to.frame(iframe)
                
                openPrice = get_open_price()
                highPrice = get_high_price()
                lowPrice = get_low_price()
                closePrice = get_close_price()
                volume = get_volume()

                logging.info(f"Updating records for {company}")
                update_history(company,[current_date, openPrice, highPrice, lowPrice,
                                        closePrice, volume])
                
                sleep(2)
            
            except Exception as e:
                logging.error(f"Error processing {company}: {e}") 
                continue        

    except Exception as e:
        logging.fatal(f"Critical encountered when processing {company}: {e}") 

    finally:
        driver.quit()

if __name__ == "__main__":
    os.makedirs(log_dir,exist_ok=True)
    main()