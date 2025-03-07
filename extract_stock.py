import os
import git

import pandas as pd
from time import sleep
from datetime import datetime
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

def get_stocks_list():
    data = pd.read_csv("stocks_list.csv")
    return data

def update_history(code: str, data: list):
    history = pd.read_csv(f"History/{code}.csv")
    new_data = pd.DataFrame([data], columns=history.columns)
    
    new_data = pd.concat([new_data, history], ignore_index=True)
    new_data.to_csv(f"History/{code}.csv", index=False)  

def push_to_giDt(file: str):
    repo = git.Repo("https://github.com/FNeal10/Stocks")
    repo.index.add(file)
    repo.index.commit(f"Updated {file}")
    origin = repo.remotes.origin
    origin.push('main') 

    import git

def push_to_git(file: str, repo_path: str, commit_message: str = "Updated the file"):
    try:
        # Open the local Git repository
        repo = git.Repo(repo_path)
        
        # Check if there are uncommitted changes
        #if repo.is_dirty(untracked_files=True):
        #    print("Changes detected. Proceeding with commit and push.")
        #else:
        #    print("No changes detected.")
        #    return  # Exit if there are no changes

        # Stage the file for commit
        repo.git.add([file])

        # Commit the changes
        repo.index.commit(commit_message)

        # Push the changes to the remote repository (replace 'main' with your branch if needed)
        origin = repo.remotes.origin
        origin.push('main')  # Replace 'main' with your branch name if it's different
        print(f"Changes pushed to the remote repository: {commit_message}")
    except Exception as e:
        print(e) 

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

            print("Upadating history")
            update_history(company,[current_date, openPrice, highPrice, lowPrice,
                                    closePrice, volume])

            print("Pushing to Git")
            push_to_git(f"{company}.csv", r"C:\Users\faltares\Documents\DEV\Stocks\History", f"Updated {company}")
            
            sleep(5)
    except Exception as e:
        print("Error:", e)

    finally:
        driver.quit()

if __name__ == "__main__":
   main()