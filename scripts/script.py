import requests
import pandas as pd
from datetime import datetime, timedelta
import time
import sys

def fetch_data(budget_type, region, start_date, end_date, delay=1):
    all_data = []
    
    def fetch_month_data(date_str):
        base_url = "https://budget.egov.kz/budgetexecutioncontroller/getincomedatajson"
        params = {
            "type": budget_type,
            "region": region,
            "date": date_str,
            "unit": "qwe",
            "_search": "false",
            "nd": str(int(time.time() * 1000)),
            "rows": "10000",
            "page": "1",
            "sidx": "id",
            "sord": "asc"
        }

        response = requests.get(base_url, params=params)
        if response.status_code == 200:
            json_data = response.json()
            if 'rows' in json_data and json_data['rows']:
                df = pd.DataFrame(json_data['rows'])
                df["month"] = date_str
                all_data.append(df)
                print(f"[✓] Добавлено: {date_str}")
            else:
                print(f"[!] Нет данных за: {date_str}")
        else:
            print(f"[✗] Ошибка {response.status_code} за {date_str}")
        time.sleep(delay)

    current_date = start_date
    while current_date <= end_date:
        month_str = current_date.strftime('%m.%Y')
        fetch_month_data(month_str)
        current_date += timedelta(days=31)
        current_date = current_date.replace(day=1)

    return all_data

def save_data_to_csv(data, filename):
    if data:
        final_df = pd.concat(data, ignore_index=True)
        final_df.to_csv(filename, index=False, sep=";")
        print(f"\n[✔] Все данные сохранены в {filename}")
    else:
        print("\n[!] Данных не найдено.")

def main():
    if len(sys.argv) != 6:
        print("Usage: python script.py <budget_type> <region> <start_date> <end_date> <filename>")
        sys.exit(1)
    budget_type = sys.argv[1]
    region = sys.argv[2]
    start_date = datetime.strptime(sys.argv[3], '%Y-%m-%d')
    end_date = datetime.strptime(sys.argv[4], '%Y-%m-%d')
    filename = sys.argv[5]

    all_data = fetch_data(budget_type, region, start_date, end_date)
    save_data_to_csv(all_data, filename)

if __name__ == "__main__":
    main()
