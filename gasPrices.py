import requests
from bs4 import BeautifulSoup

url = "https://www.gasbuddy.com/can"

response = requests.get(url)

if response.status_code == 200:
    html_content = response.content
else:
    print(f"Failed to retrieve the page. Status code: {response.status_code}")
    exit()

soup = BeautifulSoup(html_content, 'html.parser')

search_items = soup.find(id="searchItems")

gas_prices = []

for row in search_items.find_all("a", href=True):
    province_name = row.find("div", class_="siteName").text.strip()
    price = row.find_all("div")[2].text.strip()
    trend = row.find_all("span")[0].text.strip()

    gas_prices.append({
        "province": province_name,
        "price": price,
        "trend": trend,
    })

# User input
user_inp = input("Enter a province: ").lower()
province_found = False

print("Gas Price:")
print("-" * 40)
for gas_price in gas_prices:
    if gas_price["province"].lower() == user_inp:
        print(f"{gas_price['province']:10} | ${gas_price['price']} | {gas_price['trend']:>10}")
        province_found = True
        break

if user_inp == 'all'.lower():
    print("-" * 50)
    print(f"| {'Province':25} | {'Gas Price':10} | Trend |")
    print("-" * 50)
    for gas_price in gas_prices:
        print(f"| {gas_price['province']:25} | {gas_price['price']:^10} | {gas_price['trend']:>5} |")
    print("-" * 50)

if not province_found:
    print("Province not found!")
    exit()

print("-" * 40)

if user_inp == 'Alberta'.lower():
    prov_ab = 'ab'
if user_inp == 'Manitoba'.lower():
    prov_ab = 'mb'
if user_inp == 'New Brunswick'.lower():
    prov_ab = 'nb'
if user_inp == 'Newfoundland'.lower():
    prov_ab = 'nf'
if user_inp == 'Nova Scotia'.lower():
    prov_ab = 'ns'
if user_inp == 'Northwest Territories'.lower():
    prov_ab = 'nt'
if user_inp == 'Ontario'.lower():
    prov_ab = 'on'
if user_inp == 'PEI'.lower():
    prov_ab = 'pe'
if user_inp == 'Quebec'.lower():
    prov_ab = 'qc'
if user_inp == 'Saskatchewan'.lower():
    prov_ab = 'sk'
if user_inp == 'British Columbia'.lower():
    prov_ab = 'bc'

url_province = f"https://www.gasbuddy.com/can/{prov_ab}"

response_p = requests.get(url_province)

if response_p.status_code == 200:
    html_content_p = response_p.content
else:
    print(f"Failed to retrieve the page. Status code: {response_p.status_code}")
    exit()

soup_p = BeautifulSoup(html_content_p, 'html.parser')

search_items_p = soup.find(id="searchItems")

# print(soup_p.prettify())  # This prints the HTML file

city_prices = []

for row in search_items.find_all("a", href=True):
    city_name = row.find("div", class_="siteName").text.strip()
    price_c = row.find_all("div")[2].text.strip()
    trend_c = row.find_all("span")[0].text.strip()

    city_prices.append({
        "province": city_name,
        "price": price_c,
        "trend": trend_c,
    })

# Find all forms with id starting with 'item'
forms = soup_p.find_all('form', id=lambda x: x and x.startswith('item'))
print(f"Available gas prices for cities in {user_inp.capitalize()}:")
print("-" * 40)
for form in forms:
    # City
    city_name = form.find('input', {'name': 'area1'}).get('value')
    
    # Gas price
    gas_price = form.find('div', class_='col-sm-2 col-xs-3 text-right').text.strip()
    
    # Trend
    trend_span = form.find('span', class_='falling') or form.find('span', class_='rising')
    if trend_span:
        trend_text = trend_span.text.strip()
    else:
        trend_text = "0.0"
    
    print(f"{city_name:10} | ${gas_price} | {trend_text:>10}")

print("-" * 40)