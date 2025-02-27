import pandas as pd
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

def main():
    try:
        print("Start")
        driver.get(url)

        
        iframe = wait_time.until(EC.presence_of_element_located((By.ID, "company_infos")))
        driver.switch_to.frame(iframe)

        # Corrected: Waiting for the element to be present
        price_element = wait_time.until(
            EC.presence_of_element_located((By.XPATH, "/html/body/div/div/div/div[3]/div[1]/div/div[2]/div/div[1]/div[1]/div[2]/div[1]/div[1]/h3"))
        )

        # Extract and print text
        print("Stock Price:", price_element.text)

    except Exception as e:
        print("Error:", e)

    finally:
        driver.quit()  # Ensure the browser is closed after execution

if __name__ == "__main__":
    main()
