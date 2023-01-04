import openpyxl
import requests
from token_wialon import info

url = ''
sid = ''

def request(svc, params='{}'):
    url = f'https://glonass26.pro/wialon/ajax.html?svc={svc}&params={params}&sid={sid}'
    response = requests.post(url)
    if response.status_code == 200:
        response = response.json()
        return response
    return None


def login_wialon(token):
    # global url
    params = '{"token":' \
             f'"{token}"' \
             '}'
    login = f'{url}/wialon/ajax.html?svc=token/login&params={params}'
    result = requests.post(login)
    if result.status_code == 200:
        result = result.json()
        sid = result['eid']
        print(sid)
        return sid


def loguot_wialon():
    svc = 'report/select_result_rows'
    response = request(svc)
    if not response:
        return []


def set_locale():
    params = '{"tzOffset":134228528,"language":"ru","flags":256,"formatDate":"%Y-%m-%E %H:%M:%S"}'
    svc = 'render/set_locale'
    response = request(svc, params)
    # print(response)
    if not response:
        return []


def valider_car(file_name, name):
    global url
    global sid
    for i in info:
        if i['name'] == name.lower():
            url = i['url']
            sid = login_wialon(i['token'])
    set_locale()
    book = openpyxl.open(f'C:\Bot_wialon\wialon\Report\{file_name}')
    sheet = book.active
    cell_number = sheet['C8':f'C{sheet.max_row}']
    print(sheet.max_row)
    coordin_number = {

    }

    def get_id_car(nm):
        params = '{"spec":' \
                 '{"itemsType":"avl_unit","propName":"sys_name","propValueMask":"*","sortType":"sys_name"},' \
                 '"force":1,"flags":1,"from":0,"to":0}'
        svc = 'core/search_items'
        response = request(svc, params)
        if response:
            for item in response['items']:
                if item['nm'] == nm:
                    return 1
            return 0
        return 'Status_code get_id_car'

    def method(dictionary):
        # print(str(dictionary))
        for coordin in dictionary.keys():
            if (get_id_car(dictionary[coordin])):
                number = dictionary[coordin]
                for coordin_car in dictionary.keys():
                    dictionary[coordin_car] = number
                return dictionary
            else:
                continue
        return {}

    for tuple_number in cell_number:
        for number in tuple_number:
            if number.value != None:
                coordin_number[number.coordinate] = number.value
            elif number.value == None:
                if coordin_number == {}:
                    break
                coordin_number = method(coordin_number)
                # print(str(coordin_number) + '!!!')
                if coordin_number:
                    for coordin in coordin_number.keys():
                        sheet[coordin] = coordin_number[coordin]
                coordin_number.clear()

    book.save(f'C:\Bot_wialon\wialon\Report\{file_name}')
    book.close()
    loguot_wialon()

