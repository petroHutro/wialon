import requests
import datetime
import time
import json
from part_one import return_result
from grouping_data import grouping
from Zapolnenie import the_end
from token_wialon import info


token = ''
url = ''
sid = ''
ResourceId = ''
TemplateId = ''


def date_to_seconds(date):
    seconds = datetime.datetime.strptime(str(date), '%Y-%m-%d %H:%M:%S')
    return int(seconds.timestamp())


def request(svc, params='{}'):
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
    print(item)
    print(item['nm'])

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
    print(nm)
    t_from = date_to_seconds(item['start'] + ' 00:00:00')
    print(item['end'])
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
        # print(response)
        for i in response:
            result.append({'nm': item['nm'],
                           'start': i['c'][1]['t'],
                           'end': i['c'][2]['t'],
                           'mileage': i['c'][3],
                           'duration': i['c'][4],
                           'between': i['c'][5]})
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


def facet(dates, start):
    if dates == []:
        return []
    # print(dates)
    d = date_to_seconds(dates[0]['start'])
    dif = abs(d - start)
    f = dates[0]
    for date in dates:
        d = date_to_seconds(date['start'])
        r = abs(d - start)
        if r < dif:
            dif = r
            f = date
    for date in dates:
        if date == f:
            break
        else:
            dates.remove(date)
    # print(dates)
    return dates


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
            result.append(facet(pred_result.copy(), start))
            pred_result.clear()
            j += 1
            if j < len_talon:
                start, end = get_talon_time(talon[j])
        if i == len_car or j == len_talon:
            result.append(facet(pred_result.copy(), start))
            pred_result.clear()
            break
    # print(result)
    return result


def pars_web(info):
    params = param_pars(info)
    result = []
    print(str(params)+'1')
    print(str(info)+'2')
    for param, el in zip(params, info):
        print(str(param)+':3')
        print(str(el)+':4')
        data = info_car(param, el)
        if data:
            result.append(data)
    return result


def set_locale():
    params = '{"tzOffset":134228528,"language":"ru","flags":256,"formatDate":"%Y-%m-%E %H:%M:%S"}'
    svc = 'render/set_locale'
    response = request(svc, params)
    # print(response)
    if not response:
        return []


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
    time.sleep(5)


def loguot_wialon():
    svc = 'report/select_result_rows'
    response = request(svc)
    if not response:
        return []


def get_report(name, file_name):
    global url
    global sid
    global ResourceId
    global TemplateId
    for i in info:
        if i['name'] == name.lower():
            url = i['url']
            sid = login_wialon(i['token'])
            ResourceId = i['ResourceId']
            TemplateId = i['TemplateId']
    if url == '':
        return 'bad company'
    set_locale()
    rezult = the_end(grouping(pars_web(return_result('Report/' + file_name))), 'Report/' + file_name)
    if rezult != []:
        d = ''
        for i in rezult:
            d += i['nm'] + ' ' + i['date'] + '\n'
        return d
    return 'all nm'

# # # # # # # # # # #
# login_wialon()
# set_locale()
# print(the_end(grouping(pars_web(return_result()))))
# loguot_wialon()
# # # # # # # # # # #