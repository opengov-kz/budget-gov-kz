
import requests
import pandas as pd
from datetime import datetime, timedelta
import time


budget_type = "Государственный бюджет в разрезе ведомственной классификации"
region = "Республика Казахстан"  
start_date = datetime(2023, 1, 1)
end_date = datetime(2025, 4, 1)


all_data = []


def fetch_month_data(date_str, delay=1):
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

if all_data:
    final_df = pd.concat(all_data, ignore_index=True)
    final_df.to_csv("Государственный бюджет в разрезе ведомственной классификации.csv", index=False)
    print("\n[✔] Государственный бюджет в разрезе ведомственной классификации.csv")
else:
    print("\n[!] Данных не найдено.")
