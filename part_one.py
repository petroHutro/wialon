import openpyxl
import datetime


nomer_avto, data_raboti, time_start, time_end, result, slovari = [], [], [], [], [], []
flag = 0
format_dat = ['%Y-%m-%d', '%d.%m %Y', '%d %m.%Y', '%d %m %Y', ' %d.%m.%Y']
values = {
    'nm': '',
    'date': '',
    'start': '',
    'end': ''
}
list_coordin = ['C8', 'B8', 'L8', 'M8']
spiski = [nomer_avto, data_raboti, time_start, time_end]

def return_result(file_name):
    book = openpyxl.open(file_name)
    sheet = book.active
    number_car = sheet['C8'].value

    def take_data(spisok, coordin):
        cells = sheet[coordin: f'{sheet[coordin].column_letter}{sheet.max_row}']
        for cell in cells:
            for el in cell:
                if el.value != None and sheet[f'F{el.row}'].value == None:
                    data = str(el.value)
                    data = data.replace(' 00:00:00', '')
                    spisok.append(data)
        return spisok

    def data_format(data):
        for format in format_dat:
            try:
                data = datetime.datetime.strptime(data, format).date()
                return data
            except ValueError:
                continue

    for coordin, spisok in zip(list_coordin, spiski):
        print(take_data(spisok, coordin))

    for nomer, data, start, end in zip(nomer_avto, data_raboti, time_start, time_end):
        # global number_car
        data = data_format(data)
        values['nm'] = nomer
        values['date'] = str(data)
        start = datetime.datetime.strptime(start, '%H:%M:%S').time()
        values['start'] = str(start.strftime('%H:%M'))
        end = datetime.datetime.strptime(end, '%H:%M:%S').time()
        values['end'] = str(end.strftime('%H:%M'))
        if number_car == nomer:
            slovari.append(values.copy())
        else:
            result.append(slovari.copy())
            slovari.clear()
            slovari.append(values.copy())
            number_car = nomer
    result.append(slovari.copy())
    book.close()
    return result
