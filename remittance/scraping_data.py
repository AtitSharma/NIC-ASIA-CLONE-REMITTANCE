from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
import random



def get_currency_details():
    PROXIES = [
        '144.217.197.151:39399',
        '157.230.9.235:3128',
        '3.99.201.168:3128',
        '129.153.150.87:80',
        '54.36.26.122:80'
    ]
    chrome_options = Options()  
    chrome_options.add_argument("--headless")
    driver = webdriver.Chrome(options=chrome_options)
    try:
        datas=[]
        proxy = random.choice(PROXIES)
        chrome_options.add_argument('--proxy-server=%s' % proxy)
        driver.get("https://www.nrb.org.np/forex/")
        tables = WebDriverWait(driver, 5).until(EC.visibility_of_all_elements_located((By.CLASS_NAME, "card-layout")))
        for table in tables:
            table_data = table.text
            datas.append(table_data)
        new_data=[]
        for data in datas:
            splitted_data=data.split("\n")
            new_data.append(splitted_data)
        x=[]
        for i in new_data:
            x.append(i)
        new_data=[]
        for j in x:
            for k in j:
                new_data.append(k)
        driver.quit()
        return new_data
    finally:
        driver.quit() 
        
        



            
        

