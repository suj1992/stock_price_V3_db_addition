from selenium import webdriver
import warnings
warnings.filterwarnings("ignore")
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
import pandas as pd
from flask import request

# Initialize the WebDriver outside the function


def web_scrap(url):
    driver = webdriver.Chrome(ChromeDriverManager().install())
    driver.get(url)
    
    # Click the desired element
    div_element = driver.find_element(By.XPATH, '//div[@class="holdings101Cta cur-po"]')
    driver.execute_script("arguments[0].click();", div_element)
    
    # Optional: Wait for some time after clicking the element
    driver.implicitly_wait(5)


    page_source = driver.page_source


    soup = BeautifulSoup(page_source, 'html.parser')


    div_elements = soup.find_all('div', class_='holdings101TableContainer')

    # List to store table data
    table_data = []

    # Iterate over each div element
    for div in div_elements:
        # Find all table elements within the div
        table_elements = div.find_all('table')
        
        # Process the table elements as needed
        for table in table_elements:
            # Convert the table to a DataFrame
            df = pd.read_html(str(table))[0]  # Read HTML table into DataFrame
            
            # Append the DataFrame to the list
            table_data.append(df)

    # Concatenate all DataFrames into a single DataFrame
    final_df = pd.concat(table_data, ignore_index=True)

    return final_df