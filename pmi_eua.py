from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import pandas as pd
from datetime import datetime
import time

URL = "https://br.investing.com/economic-calendar/ism-non-manufacturing-pmi-176"

def scrape_full_ism_history():
    options = Options()
    options.add_argument('--headless')
    options.add_argument('--disable-gpu')
    options.add_argument('--no-sandbox')
    options.add_argument('--lang=pt-BR')
    driver = webdriver.Chrome(service=Service(), options=options)
    driver.get(URL)

    # Aceita cookies se houver
    try:
        WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.ID, "onetrust-accept-btn-handler"))
        ).click()
    except:
        pass 

    while True:
        try:
            exibir_mais = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.ID, "showMoreHistory176"))
            )
            driver.execute_script("arguments[0].click();", exibir_mais)
            time.sleep(1)
        except:
            break  

    soup = BeautifulSoup(driver.page_source, 'html.parser')
    driver.quit()

    table = soup.find('table', id='eventHistoryTable176')
    data = []

    if table:
        rows = table.find('tbody').find_all('tr')
        for row in rows:
            cols = row.find_all('td')
            if len(cols) > 4:
                date_str = cols[0].text.strip().split(' ')[0]
                actual_str = cols[2].text.strip().replace(',', '.')
                forecast_str = cols[3].text.strip().replace(',', '.')
                previous_str = cols[4].text.strip().replace(',', '.')
                try:
                    date_obj = datetime.strptime(date_str, '%d.%m.%Y')
                except ValueError:
                    date_obj = None
                data.append({
                    'date': date_obj,
                    'actual_state': float(actual_str) if actual_str and actual_str != '\xa0' else None,
                    'forecast': float(forecast_str) if forecast_str and forecast_str != '\xa0' else None,
                    'close': float(previous_str) if previous_str and previous_str != '\xa0' else None,
                })

    df = pd.DataFrame(data)
    return df

# --- Execução
if __name__ == "__main__":
    df = scrape_full_ism_history()
    print(f"\n{len(df)} registros extraídos.")
    print(df.head())
    df.to_csv("ism_services_pmi_full.csv", index=False, date_format='%Y-%m-%d')