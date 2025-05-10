# -*- coding: utf-8 -*-
import requests
from bs4 import BeautifulSoup
import pandas as pd
from datetime import datetime

CAIXIN_URL = "https://br.investing.com/economic-calendar/chinese-caixin-services-pmi-596"


def scrape_caixin_data(url):
    """Raspa os dados históricos do Índice Caixin Services PMI."""
    print(f"Iniciando scraping para Caixin PMI: {url}")
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
        'Accept-Language': 'pt-BR,pt;q=0.9,en-US;q=0.8,en;q=0.7'
    }
    try:
        response = requests.get(url, headers=headers, timeout=30)
        response.raise_for_status() 
        soup = BeautifulSoup(response.content, 'html.parser')

        table = soup.find('table', id='eventHistoryTable596')

        data = []
        if table:
            print("Tabela histórica encontrada. Extraindo dados...")
            rows = table.find('tbody').find_all('tr')
            for row in rows:
                cols = row.find_all('td')
                if len(cols) > 4:
                    date_str = cols[0].text.strip()
                    actual_str = cols[2].text.strip().replace(',', '.')
                    forecast_str = cols[3].text.strip().replace(',', '.')
                    previous_str = cols[4].text.strip().replace(',', '.')
                    try:
                        date_obj = datetime.strptime(date_str, '%d.%m.%Y')
                    except ValueError:
                        print(f"Formato de data inválido encontrado: {date_str}")
                        date_obj = None
                    data.append({
                        'date': date_obj,
                        'actual': float(actual_str) if actual_str and actual_str != '\xa0' else None,
                        'forecast': float(forecast_str) if forecast_str and forecast_str != '\xa0' else None,
                        'previous': float(previous_str) if previous_str and previous_str != '\xa0' else None
                    })
            print(f"Extração da tabela histórica concluída. {len(data)} registros.")
        else:
            print("Tabela histórica não encontrada. Tentando extrair dados recentes...")
            recent_data_div = soup.find('div', class_='economicCalendarData')
            if recent_data_div:
                try:
                    date_str = recent_data_div.find('div', class_='date').text.strip()
                    actual_str = recent_data_div.find('div', class_='actual').find('span').text.strip().replace(',', '.')
                    forecast_str = recent_data_div.find('div', class_='forecast').find('span').text.strip().replace(',', '.')
                    previous_str = recent_data_div.find('div', class_='previous').find('span').text.strip().replace(',', '.')
                    date_obj = datetime.strptime(date_str, '%d.%m.%Y')
                    data.append({
                        'date': date_obj,
                        'actual': float(actual_str) if actual_str and actual_str != '\xa0' else None,
                        'forecast': float(forecast_str) if forecast_str and forecast_str != '\xa0' else None,
                        'previous': float(previous_str) if previous_str and previous_str != '\xa0' else None
                    })
                    print("Extração dos dados recentes concluída. 1 registro.")
                except Exception as e_recent:
                    print(f"Erro ao extrair dados recentes: {e_recent}")
            else:
                print("Dados recentes também não encontrados.")

        if not data:
             print("Nenhum dado do Caixin PMI pôde ser extraído.")
             return pd.DataFrame(columns=['date', 'actual_state', 'close', 'forecast'])

        df = pd.DataFrame(data)
        # Renomear colunas para o schema final solicitado no case original
        df.rename(columns={'actual': 'actual_state', 'previous': 'close'}, inplace=True)
        # Garantir a ordem das colunas
        df = df[['date', 'actual_state', 'close', 'forecast']]
        print(f"Scraping do Caixin concluído. Total de {len(df)} registros encontrados.")
        return df

    except requests.exceptions.RequestException as e:
        print(f"Erro ao acessar a URL do Caixin: {e}")
        return pd.DataFrame(columns=['date', 'actual_state', 'close', 'forecast'])
    except Exception as e:
        print(f"Erro inesperado durante o scraping do Caixin: {e}")
        return pd.DataFrame(columns=['date', 'actual_state', 'close', 'forecast'])

# --- Execução --- #
if __name__ == "__main__":
    print("--- Iniciando processo de scraping do Caixin PMI --- ")

    df_caixin = scrape_caixin_data(CAIXIN_URL)

    if not df_caixin.empty:
        print("\nDados Caixin Services PMI extraídos:")
        print(df_caixin.head())
        # Opcional: Salvar em CSV
        try:
            output_filename = "caixin_pmi_data.csv"
            df_caixin.to_csv(output_filename, index=False, date_format='%Y-%m-%d')
            print(f"\nDados salvos em '{output_filename}'")
        except Exception as e_csv:
            print(f"\nErro ao salvar dados em CSV: {e_csv}")
    else:
        print("\nNão foi possível obter dados do Caixin PMI.")

    print("\n--- Processo concluído ---")