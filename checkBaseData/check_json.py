import json
import requests

headers = {
    'Accept': 'application/json, text/plain, */*',
    'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8,zh-TW;q=0.7',
    'Connection': 'keep-alive',
    'Content-Type': 'application/json',
    'Origin': 'https://manage-global-qa.moretickets.com',
    'Referer': 'https://manage-global-qa.moretickets.com/',
    'Sec-Fetch-Dest': 'empty',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Site': 'same-site',
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36',
    'access_token': 'eyJhbGciOiJSUzI1NiJ9.eyJleHBpcmVUaW1lIjoxNzI3MTc4NTUzMDM4LCJiaXpPcGVyYXRvcklkIjoiNjY1MzAxZmM0ZDIyZDkxZDA3OGY4NWIwIiwiYWxsb3dQYXRoIjoiL21hbmFnZSIsImNyZWF0ZVRpbWUiOjE3MjcwOTIxNTMwMzgsImlkZW50aXR5IjoiNjYzYWVkZDc1ZDVjYjk3NzBjMGU2OTYyIiwib3JnQ29kZSI6Ik1UU19NIiwiY2VsbHBob25lIjoiMTg2NTU1MTE5OTkiLCJ1c2VyTmFtZSI6ImRldmVsb3AifQ.OAMeDxGYn0oDNjjDo_Z8M2_MldeCT25Zo7sWr2PHIV3tKXiT27lVRnzRF7lipP24TY0BvpRdIJFGj3hbldf-j9b9AqpjdXVi3-tjshDWq8XxZ9AUOEfNK_jhXSBuZfuDFmd-5m3z19zInHtjfxCModR_LPfVATdZfXfjViST5O8IY6JEbjGUeLVXQMOrheeDe5bH5O5v8F4f2Ap_nuHD-uY0X9j_N6Uge3EMvlaphBu6RkLaRPssvng8JcBSIXA_z_RQLmZ_Wf3eYwfK3Op5XG5ToimINedx7IdVnC5h3_P6n96jimq583voEizH9r_c0Akvk8O9ueSkChZ7eYUmIw',
    'lan': 'zh-CN',
    'oc': 'MTS_M',
    'sec-ch-ua': '"Chromium";v="128", "Not;A=Brand";v="24", "Google Chrome";v="128"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"macOS"',
}

params = {
    'countryCode': 'CN',
}

response = requests.get(
    'https://api-global-qa.moretickets.com/manage/location/v1/region/cascade/list',
    params=params,
    headers=headers,
)
api_response = response.json()['data']


def read_json(file_path):
    districts_name = set()
    with open(file_path, 'r', encoding='utf-8') as file:
        location_data = json.load(file)
        for province in location_data:
            for city in province['cities']:
                for district in city['districts']:
                    district_name = district['district']
                    districts_name.add(district_name)
        return districts_name

def extract_district_info(api_response):
    district_info = []
    for region in api_response:
        region_name = region['name']
        if 'cityList' in region:
            for city in region['cityList']:
                city_name = city['name']
                if 'districtList' in city:
                    for district in city['districtList']:
                        district_info.append({
                            'region': region_name,
                            'city': city_name,
                            'district': district['name']
                        })
    return district_info


def check_names(api_response, file_path):
    ext_names = read_json(file_path)
    district_info = extract_district_info(api_response)

    missing_info = [
        (info['region'], info['city'], info['district'])
        for info in district_info
        if info['district'] not in ext_names
    ]

    if not missing_info:
        print("所有区名都在文件中存在。")
    else:
        print("差異部分如下：")
        for region, city, district in missing_info:
            print(f"区域: {region}, 城市: {city}, 区名: {district}")


check_names(api_response, 'location2.json')
