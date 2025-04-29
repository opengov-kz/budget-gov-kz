import requests
import pandas as pd

url = 'https://budget.egov.kz/budgetexecutioncontroller/getincomedatajson?type=%D0%9C%D0%B5%D1%81%D1%82%D0%BD%D1%8B%D0%B9%20%D0%B1%D1%8E%D0%B4%D0%B6%D0%B5%D1%82%20%D0%B2%20%D1%80%D0%B0%D0%B7%D1%80%D0%B5%D0%B7%D0%B5%20%D1%84%D1%83%D0%BD%D0%BA%D1%86%D0%B8%D0%BE%D0%BD%D0%B0%D0%BB%D1%8C%D0%BD%D0%BE%D0%B9%20%D0%BA%D0%BB%D0%B0%D1%81%D1%81%D0%B8%D1%84%D0%B8%D0%BA%D0%B0%D1%86%D0%B8%D0%B8&region=%D0%9A%D0%BE%D1%81%D1%82%D0%B0%D0%BD%D0%B0%D0%B9%D1%81%D0%BA%D0%B0%D1%8F%20%D0%BE%D0%B1%D0%BB%D0%B0%D1%81%D1%82%D1%8C&date=01.2023&unit=qwe&_search=false&nd=1745900090737&rows=10000&page=1&sidx=id&sord=asc'

response = requests.get(url)

if response.status_code == 200:
    data = response.json()

    if 'rows' in data:
        df = pd.DataFrame(data['rows'])
        
        file_name = 'Местный бюджет в разрезе функциональной классификации_01_2023.csv'
        df.to_csv(file_name, index=False)
        print(f"Данные успешно сохранены в файл: {file_name}")
    else:
        print("Не удалось найти нужные данные в ответе.")
else:
    print(f"Ошибка загрузки данных: {response.status_code}")
