import datetime


one_car_info = {
    'nm': '',
    'date': '',
    'start': '',
    'end': '',
    'mileage': '',
    'duration': '',
    'between': '',
    'halt': '',
}
duration_list = []
between_list = []
halt_list = []
list_for_fillings = []
new_spisok = []
final_spisok = []
flag = 0

def sum_time(timelist):
    sum = datetime.timedelta()
    for time in timelist:
        (h, m, s) = time.split(':')
        time_delta = datetime.timedelta(hours=int(h), minutes=int(m), seconds=int(s))
        sum += time_delta
    timelist.clear()
    return str(sum)


def grouping(data_list):
    global flag
    for car in data_list:
        for date in car:
            if date == []:
                break
            time_delta = '0:05:30'
            mileage = 0.0
            start = date[0]['start'][11:16]
            end = date[-1]['end'][11:16]
            date[0]['between'] = '00:00:00'
            # date[0]['between'] = str(datetime.timedelta(hours=00, minutes=00, seconds=00))
            for el in date:
                mileage += float(el['mileage'].replace(' км', ''))
                mileage = float("{0:.2f}".format(mileage))
                duration_list.append(str(el['duration']))
                between_list.append(str(el['between']))
                if str(el['between']) < time_delta:
                    halt_list.append(str(el['between']))
            duration = sum_time(duration_list)
            between = sum_time(between_list)
            halt = sum_time(halt_list)
            list_for_fillings.append({'nm': date[0]['nm'], 'date': date[0]['start'][:10],'start': start, 'end': end,
                                      'mileage': mileage, 'duration': duration[:4], 'between': between[:4],
                                      'halt': halt[:4]})
        flag -= 1

    nm = list_for_fillings[0]['nm']
    for nomer in list_for_fillings:
        if nomer['nm'] == nm:
            new_spisok.append(nomer.copy())
        else:
            final_spisok.append(new_spisok.copy())
            new_spisok.clear()
            new_spisok.append(nomer.copy())
            nm = nomer['nm']
    final_spisok.append(new_spisok.copy())
    return final_spisok

