import yfinance as yf
import pandas as pd
from datetime import datetime

# Configurações
symbol = "CNY=X" 
start_date = "2001-01-01"
end_date = datetime.today().strftime('%Y-%m-%d')
csv_path = "usd_cny_mensal.csv"

print(f"🔍 Buscando dados mensais para {symbol} de {start_date} até {end_date}...")

try:
    # Puxar os dados mensais
    data = yf.download(symbol, start=start_date, end=end_date, interval="1mo", progress=False)

    if data.empty:
        print(f"Nenhum dado encontrado para {symbol}.")
    else:
        data.reset_index(inplace=True)

        data["date"] = pd.to_datetime(data["Date"]).dt.strftime("%Y-%m-%d")

        df_final = data.rename(columns={
            "Open": "open",
            "High": "high",
            "Low": "low",
            "Close": "close",
            "Volume": "volume"
        })[["date", "close", "open", "high", "low", "volume"]]

        # Salvar em CSV
        df_final.to_csv(csv_path, index=False)
        print(f"Dados salvos com sucesso em: {csv_path}")

        #Exibir logs
        print(f"Registros totais: {len(df_final)}")
        print(f"Primeira data: {df_final['date'].iloc[0]}, Última data: {df_final['date'].iloc[-1]}")
        print("\n Amostra dos dados mensais:")
        print(df_final.head())

except Exception as e:
    print(f" Erro ao puxar ou salvar os dados: {e}")