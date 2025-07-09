import requests
from bs4 import BeautifulSoup
import json

url = "https://www.sberbank.ru/ru/person_new?segment=pens"
headers = {'User-Agent': 'Mozilla/5.0'}

response = requests.get(url, headers=headers)
soup = BeautifulSoup(response.text, "html.parser")

results = []

for link in soup.find_all('a'):
    text = link.get_text(strip=True)
    href = link.get('href')
    if text and href:
        if 'segment=pens' in href:
            full_link = "https://www.sberbank.ru" + href if href.startswith('/') else href
            results.append({"title": text, "link": full_link})

# Убираем дубли
unique_results = []
seen = set()
for item in results:
    key = (item['title'], item['link'])
    if key not in seen:
        unique_results.append(item)
        seen.add(key)

with open("data.json", "w", encoding="utf-8") as f:
    json.dump(unique_results, f, ensure_ascii=False, indent=2)

print(f"Готово! Найдено {len(unique_results)} ссылок для пенсионеров и сохранено в data.json")
