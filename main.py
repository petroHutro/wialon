import requests
import datetime
import time
import json
from part_one import return_result
from grouping_data import grouping
from Zapolnenie import the_end

sid = ''
# 665 Юг
# 547 Авто

url = 'https://glonass26.pro'
# url = 'https://hosting.wialon.com'
# token = 'ff6277a6c2a5e7f38bb93cad1e1e0e2e1AC1982C54C6E8F9FC3A87DB61B1B4DFDC435CC2'    #ОООРНСНГНАТ
# token = '93f7965888ca74075d36d33d1ee70853041532CA201F80BCC1DDDA5932C014B2034B038A'    # Юг
token = '6c88e28e1e258ae59f4188a472eb5cb76E2F0AA39350ACA692BFEACC1E5B503426EC999F'  # Авто
ResourceId = '547'
TemplateId = '5'


def date_to_seconds(date):
    seconds = datetime.datetime.strptime(str(date), '%Y-%m-%d %H:%M:%S')
    return int(seconds.timestamp())


def request(svc, params='{}'):
    global sid
    url = f'https://glonass26.pro/wialon/ajax.html?svc={svc}&params={params}&sid={sid}'
    response = requests.post(url)
    if response.status_code == 200:
        response = response.json()
        return response
    return None


def get_id_car(nm):
    params = '{"spec":' \
             '{"itemsType":"avl_unit","propName":"sys_name","propValueMask":"*","sortType":"sys_name"},' \
             '"force":1,"flags":1,"from":0,"to":0}'
    svc = 'core/search_items'
    response = request(svc, params)
    if response:
        for item in response['items']:
            if item['nm'] == nm:
                return item['id']
        return 'No car'
    return 'Status_code get_id_car'


def get_info_car(item):
    global ResourceId
    global TemplateId
    print(item['nm'])
    # params = '{"itemId":547,"col":[5],"flags":0}'
    # talon_1 = f'https://glonass26.pro/wialon/ajax.html?svc=report/get_report_data&params={params}&sid={sid}'
    # if requests_post(talon_1, 'e'):
    #     print('talon_1')

    params = '{"params":' \
             '[{"svc":"report/cleanup_result","params":{}},' \
             '{"svc":"report/cleanup_result","params":{}},' \
             '{"svc":"report/get_report_data","params":{' \
             f'"itemId":{ResourceId},"col":["{TemplateId}"],"flags":0' \
             '}}],"flags":0}'
    svc = 'core/batch'
    response = request(svc, params)
    if not response:
        return []

    nm = get_id_car(item['nm'])
    if nm == 'No car':
        return []

    t_from = date_to_seconds(item['start'] + ' 00:00:00')
    t_to = date_to_seconds(item['end'] + ' 23:59:59')
    params = ('{'
              f'"reportResourceId":{ResourceId},'
              f'"reportTemplateId":{TemplateId},'
              '"reportTemplate":null,'
              f'"reportObjectId":{nm},'
              '"reportObjectSecId":0,'
              '"interval":'
              '{"flags":0,'
              f'"from":{t_from},"to":{t_to}'
              '},"remoteExec":1}')
    svc = 'report/exec_report'
    response = request(svc, params)
    if not response:
        return []

    svc = 'report/get_report_status'
    response = request(svc)
    if not response:
        return []

    svc = 'report/apply_report_result'
    response = request(svc)  # row
    if not response:
        return []

    params = ('{"tableIndex":0,"config":{"type":"range","data":{"from":0,'
              f'"to":0'
              ',"level":0,"unitInfo":1}}}')
    svc = 'report/select_result_rows'
    response = request(svc, params)
    if not response:
        return []

    params = ('{"tableIndex":0,"config":{"type":"row","data":{'
              f'"rows":["0"]'
              ',"level":0,"unitInfo":1}}}')
    try:
        svc = 'report/select_result_rows'
        response = request(svc, params)
        if not response:
            return []
        result = []
        print(response)
        for i in response:
            result.append({'nm': item['nm'],
                           'start': i['c'][1]['t'],
                           'end': i['c'][2]['t'],
                           'mileage': i['c'][3],
                           'duration': i['c'][4],
                           'between': i['c'][5]})
        # with open("res.json", "w", encoding='utf-8') as file:
        #     json.dump(response, file, indent=4, ensure_ascii=False)
        response.clear()
    except:
        return []
    time.sleep(1)
    return result


def param_pars(elements):
    result = []
    for el in elements:
        car = el[0]['nm']
        start = el[0]['date']
        days = len(el) - 1
        date = el[days]['date']
        if el[days]['end'] <= el[days]['start']:
            date = str(datetime.datetime.strptime(date, '%Y-%m-%d') + datetime.timedelta(days=1))[:10]
        result.append({'nm': car, 'start': start, 'end': date})
    return result


def get_talon_time(talon):
    start = date_to_seconds(talon['date'] + ' ' + talon['start'] + ':00')
    end = date_to_seconds(talon['date'] + ' ' + talon['end'] + ':00')
    if talon['end'] <= talon['start']:
        new_date = str(datetime.datetime.strptime(talon['date'], '%Y-%m-%d') + datetime.timedelta(days=1))[:10]
        end = date_to_seconds(new_date + ' ' + talon['end'] + ':00')
    return start, end


def info_car(grop, talon):
    car = get_info_car(grop)
    if car == []:
        return car
    result = []
    pred_result = []
    len_talon = len(talon)
    len_car = len(car)
    i = 0
    j = 0
    start, end = get_talon_time(talon[j])
    while 1:
        start_car = date_to_seconds(car[i]['start'])
        if start <= start_car <= end or start - 300 <= start_car <= end:
            pred_result.append(car[i])
            i += 1
        elif start_car < start:
            i += 1
        elif start_car > end:
            result.append(pred_result.copy())
            pred_result.clear()
            j += 1
            if j < len_talon:
                start, end = get_talon_time(talon[j])
        if i == len_car or j == len_talon:
            result.append(pred_result.copy())
            pred_result.clear()
            break
    print(result)
    return result


def pars_web(info):
    params = param_pars(info)
    result = []
    for param, el in zip(params, info):
        data = info_car(param, el)
        if data:
            result.append(data)
    return result


def set_locale():
    params = '{"tzOffset":134228528,"language":"ru","flags":256,"formatDate":"%Y-%m-%E %H:%M:%S"}'
    svc = 'render/set_locale'
    response = request(svc, params)
    print(response)
    if not response:
        return []


def login_wialon():
    global sid
    global url
    global token
    params = '{"token":' \
             f'"{token}"' \
             '}'
    login = f'{url}/wialon/ajax.html?svc=token/login&params={params}'
    result = requests.post(login)
    if result.status_code == 200:
        result = result.json()
        sid = result['eid']
        print(sid)
    time.sleep(5)


def loguot_wialon():
    global sid
    global url
    # params = 'params={}'
    # logout = f'{url}/wialon/ajax.html?svc=core/logout&{params}&sid={sid}'
    svc = 'report/select_result_rows'
    response = request(svc)
    if not response:
        return []
    # result = requests.post(logout)
    # if result.status_code == 200:
    #     result = result.json()
    #     print(result)

# # # # # # # # # # #
login_wialon()
set_locale()
print(the_end(grouping(pars_web(return_result()))))
loguot_wialon()
# # # # # # # # # # #

# # # # # # # # # # #
# login_wialon()
# params = '{"spec":{"itemsType":"avl_resource","propName":"sys_name","propValueMask":"*","sortType":"sys_name"},"force":1,"flags":1,"from":0,"to":0}'
# url = f'http://glonass26.pro/wialon/ajax.html?svc=core/search_items&params={params}&sid={sid}'
# if requests_post(url, 'e'):
#     print('view_t')
# loguot_wialon()
# # # # # # # # # # #

# time_delta = datetime.datetime.strptime(str(mytime), '%Y-%m-%d %H:%M:%S')
# print(int(time_delta.timestamp()))
#
# ts = int(time_delta.timestamp())
# print(datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S'))