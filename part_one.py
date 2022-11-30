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
poisk_slov = ['Регистрационный номер ТС', 'Дата работы ТС', 'Талон', 'Талон']
spiski = [nomer_avto, data_raboti, time_start, time_end]

def return_result(file_name):
    book = openpyxl.open(file_name)
    sheet = book.active
    number_car = sheet['C8'].value
    def search_word(name):
        global flag
        for row in sheet:
            for value in row:
                if value.value == name:
                    coordin = value.coordinate
                    coordin = sheet[coordin].offset(row=1, column=0).coordinate

        if name == 'Талон' and flag == 0:
            coordin = sheet[coordin].offset(row=1, column=0).coordinate
            flag = 1
        elif name == 'Талон':
            coordin = sheet[coordin].offset(row=1, column=1).coordinate
            flag = 0
        return coordin

    def take_data(spisok, coordin):
        cells = sheet[coordin: f'{sheet[coordin].column_letter}{sheet.max_row}']
        for cell in cells:
            for el in cell:
                if el.value != None:
                    date = str(el.value)
                    date = date.replace(' 00:00:00', '')
                    spisok.append(date)
        return spisok

    def data_format(data):
        for format in format_dat:
            try:
                data = datetime.datetime.strptime(data, format).date()
                return data
            except ValueError:
                continue

    for slova,spisok in zip(poisk_slov, spiski):
        coordin = search_word(slova)
        take_data(spisok, coordin)

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
