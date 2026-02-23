import requests
import json
from datetime import datetime
import pandas as pd

# https://lalafo.kg/api/search/v3/feed/search?expand=url&per-page=20&category_id=1502
from pandas import ExcelWriter

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36 OPR/107.0.0.0",
    "Accept": "application/json, text/plain, */*",
    "device": "pc"
}

url = "https://lalafo.kg/api/search/v3/feed/search?expand=url&per-page=20&category_id=1502"

url_params = f"https://lalafo.kg/api/search/v3/feed/details/{id}?expand=url"

r = requests.get(url, headers=headers)
data = r.json()

def get_json(params):
    """получаем json с данными по заданным запросам"""
    url = f"https://lalafo.kg/api/search/v3/feed/search?"
    response = requests.get(url, headers=headers, params=params)
    return response.json()

def get_auto_param_json(id):
    url_params = f"https://lalafo.kg/api/search/v3/feed/details/{id}"
    auto_params = {
        "expand": "url"
    }
    response = requests.get(url_params, headers=headers, params=auto_params)
    return response.json()

def get_auto_title_json(id):
    url_params = f"https://lalafo.kg/api/seo/v3/metas/details?ad_id={id}"
    auto_params = {
        "expand": "url"
    }
    response = requests.get(url_params, headers=headers, params=auto_params)
    return response.json()

def get_param_value(auto_params, id):
    for i in range(16):
        try:
            if auto_params[i]['id'] == id:
                return auto_params[i]['value']
        except (IndexError, KeyError):
            print('Index error')
            return None

def get_data_from_json(json_file, page):
    domen_photo = 'https://img5.lalafo.com/i/posters/api'
    domen = 'https://lalafo.kg'
    # проходимся по данным и собираем в список то, что нам нужно
    result = []
    i = 0
    for d in json_file['items']:
        try:
            post_id = d['id']
            created_time = d['created_time']
            phone = d['mobile']
            price = d['price']
            url_goods = d['url']

            vip_post = d['is_vip']
            city = d['city']
            try:
                nameseller = d['user']['username']
            except:
                nameseller = ''

            json_auto_params = get_auto_param_json(post_id)
            json_auto_title = get_auto_title_json(post_id)

            brand = json_auto_title['h1']
            title = json_auto_title['title']
            if json_auto_params['description'] == '':
                description = json_auto_title['title'].split('➤')[0]
            else: description = json_auto_params['description']
            if 'images' in json_auto_params and json_auto_params['images']:
                image = json_auto_params['images'][0]['original_url']
            else: image = ''
                # Handle the case when there are no images or 'images' key is missing

            model = get_param_value(json_auto_params['params'], 49)

            condition = get_param_value(json_auto_params['params'], 29)
            year = get_param_value(json_auto_params['params'], 62)
            run_km = get_param_value(json_auto_params['params'], 56)
            fuel_type = get_param_value(json_auto_params['params'], 65)
            body_type = get_param_value(json_auto_params['params'], 63)
            transmission_type = get_param_value(json_auto_params['params'], 64)
            wheel_drive = get_param_value(json_auto_params['params'], 244)
            wheel_side = get_param_value(json_auto_params['params'], 106)
            color = get_param_value(json_auto_params['params'], 105)
            engine_capacity = get_param_value(json_auto_params['params'], 66)
            vin_code = get_param_value(json_auto_params['params'], 1156)
            tech_condition = get_param_value(json_auto_params['params'], 1155)
            clearance_rastamojka = get_param_value(json_auto_params['params'], 1157)
            in_stock = get_param_value(json_auto_params['params'], 242)
            payment = get_param_value(json_auto_params['params'], 1154)

            result.append({
                'post_id': post_id,
                'created_time': datetime.fromtimestamp(created_time).strftime('%d-%m-%Y %H:%M:%S'),
                'city': city,

                'brand': brand,
                'model': model,
                'title': title,
                'description': description,
                'price': price,
                'condition': condition,
                'year': year,
                'run_km': run_km,
                'fuel_type': fuel_type,
                'body_type': body_type,
                'transmission_type': transmission_type,
                'wheel_drive': wheel_drive,
                'wheel_side': wheel_side,
                'color': color,
                'engine_capacity': engine_capacity,
                'vin_code': vin_code,
                'tech_condition': tech_condition,
                'clearance': clearance_rastamojka,

                'image': image,
                'vip_status': vip_post,
                'url': domen + str(url_goods),

                'name_seller': nameseller,
                'payment': payment,
                'phone': phone,
            })

            i = i + 1
            print(i, " - element added (" ,brand ," ", model, "); page -", page)
        except Exception as e:
            print("Error:", e)
            continue
    return result

def save_excel(data, name):
    df = pd.DataFrame(data)
    writer = ExcelWriter(f'../../../templates/dataset/lalafo_results_{name}.xlsx')
    df.to_excel(writer, 'data')
    writer._save()
    print(f'Все сохранено в lalafo_results_{name}.xlsx')

def get_cars_by_brand(brand_name, brand_id, amount, pages):
    params = {
        "expand": "url",
        'price[from]': 100000,
        'currency': 'KGS',
        'per-page': amount,
        'page': 1,  # Start with page 1
        'sort_by': "newest",
        'category_id': brand_id
    }
    all_data = []

    # Pagination loop
    for i in range(1,pages):
        json_data = get_json(params)
        data = get_data_from_json(json_data, i)
        all_data.extend(data)

        if len(data) < params['per-page']:
            break  # No more pages, exit loop

        # Increment page number for next request
        params['page'] += 1

    save_excel(all_data, brand_name)  # Save all data to a single Excel file


#'category_id': '1502' - all_cars
#'1608' - toyota
#'1570' - honda
#'1585' - mercedes
#'1610' - volkswagen
#'1610' - hyundai
#'1555' - audi
#'1557' - bmw
#'1576' - kia
#'1589' - mitsubishi
#'1563' - daewoo

car_brands = {
    # 'all_cars': '1502',
    # 'toyota': '1608',
    'honda': '1570',
    'mercedes': '1585',
    'volkswagen': '1610',
    'hyundai': '1610',
    'audi': '1555',
    'bmw': '1557',
    'mitsubishi': '1589',
    'kia': '1576'
}

#MAIN
for brand_name, brand_id in car_brands.items():
    get_cars_by_brand(brand_name, brand_id, 100, 20)
    print(f"Excel file for {brand_name} cars has been saved.")
