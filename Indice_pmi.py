import requests
import pandas as pd
from io import StringIO

def download_and_process_caixin_pmi_mql5():
    """
    Baixa os dados históricos do PMI de Serviços Caixin do mql5.com,
    processa-os usando pandas e salva em um novo arquivo CSV.
    Retorna o DataFrame processado.
    """
    url = "https://www.mql5.com/pt/economic-calendar/china/caixin-services-pmi/export"
    output_filename = "caixin_pmi_mql5_processed.csv"

    print(f"Baixando dados de: {url}")
    try:
        response = requests.get(url)
        response.raise_for_status()  
        print("Download concluído com sucesso.")

        csv_data = StringIO(response.text)
        df = pd.read_csv(csv_data, sep='\t')
        print("Dados carregados em DataFrame pandas.")

        # Tratamento dos dados

        df.rename(columns={
            'Date': 'date',
            'ActualValue': 'actual',
            'ForecastValue': 'forecast',
            'PreviousValue': 'previous'
        }, inplace=True)

        # Converter a coluna 'date' para o tipo datetime

        df['date'] = pd.to_datetime(df['date'], format='%Y.%m.%d')
        print("Coluna 'date' convertida para datetime.")

        # Lidar com valores ausentes (NaN) - aqui, vamos apenas mostrar se existem

        print(f"Valores ausentes por coluna antes de qualquer tratamento:\n{df.isnull().sum()}")

        # Ordenar por data, do mais antigo para o mais recente
        df.sort_values(by='date', ascending=True, inplace=True)
        print("DataFrame ordenado por data.")

        # Salvar o DataFrame processado em um novo arquivo CSV

        df.to_csv(output_filename, index=False, encoding='utf-8')
        print(f"DataFrame processado salvo em: {output_filename}")

        print("\nPrimeiras 5 linhas do DataFrame processado:")
        print(df.head())
        print("\nÚltimas 5 linhas do DataFrame processado:")
        print(df.tail())

        return df, output_filename

    except requests.exceptions.RequestException as e:
        print(f"Erro ao baixar os dados: {e}")
        return None, None
    except Exception as e:
        print(f"Erro ao processar os dados: {e}")
        return None, None

if __name__ == "__main__":
    processed_df, saved_file = download_and_process_caixin_pmi_mql5()
    if processed_df is not None:
        print(f"\nScript concluído. Dados processados e salvos em '{saved_file}'.")
    else:
        print("\nScript falhou.")