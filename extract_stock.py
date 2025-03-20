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
os.makedirs(log_dir, exist_ok=True)
logging.basicConfig(
    filename=log_filename,
    level=logging.DEBUG,
    format="%(asctime)s - %(levelname)s - %(message)s"
)


def init_driver():
    options = webdriver.ChromeOptions()
    options.add_argument('--headless--')
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    return driver

def extract_stock_prices(driver, xpath):
    element = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, xpath)))
    return element.text.replace('"','').strip()

def process_stock(driver, company, url):
    try:
        driver.get(url)
        iFrame = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "company_infos"))
        )
        driver.switch_to.frame(iFrame)

        stock_data = {
            "open": extract_stock_prices(driver,"/html/body/div/div/div/div[3]/div[1]/div/div[3]/table/tbody/tr[1]/td[4]"),
            "high": extract_stock_prices(driver,"/html/body/div/div/div/div[3]/div[1]/div/div[3]/table/tbody/tr[2]/td[4]"),
            "low": extract_stock_prices(driver,"/html/body/div/div/div/div[3]/div[1]/div/div[3]/table/tbody/tr[3]/td[4]"),
            "close": extract_stock_prices(driver,"/html/body/div/div/div/div[3]/div[1]/div/div[3]/table/tbody/tr[1]/td[6]"),
            "volume": extract_stock_prices(driver,"/html/body/div/div/div/div[3]/div[1]/div/div[3]/table/tbody/tr[3]/td[2]")
        }

        if None in stock_data.values():
            return
        
        update_history(company,[datetime.now().strftime("%m/%d/%Y"), stock_data["open"], stock_data["high"],
                       stock_data["low"], stock_data["close"], stock_data["volume"]])
    
        sleep(5)

    except Exception as e:
        logging.fatal(f"Error in processing {company} - {e}")

def main():
    try:
        logging.info(f"Starting application.....") 

        data = get_urls()
        for _, stock in data.iterrows():
            process_stock(driver, stock.CODE, stock.URL)

    except Exception as e:
        logging.fatal(f"Critical error encountered {e}") 

    finally:
        driver.quit()

if __name__ == "__main__":
    main()