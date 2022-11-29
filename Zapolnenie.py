import openpyxl

column = ['N', 'O', 'F', 'G', 'I', 'H']
name_key = ['start', 'end', 'mileage', 'duration', 'between', 'halt']

def the_end(list_for_fillings):
    car_missing = []
    book = openpyxl.open("report_2.xlsx")
    sheet = book.active
    cell_number = sheet['C8':f'C{sheet.max_row}']
    cell_date = sheet['B8':f'B{sheet.max_row}']
    dictionary_car_missing = {
        'nm': '',
        'date': '',
    }

    def search_coordinate(car_number):
        coordin = ''
        for tuple in cell_number:
            for value in tuple:
                if value.value == car_number:
                    coordin = value.coordinate
                    return coordin

    def completion(column, name_key, row):
        sheet[f'{column}{row}'] = data[name_key]

    for car in list_for_fillings:
        car_number = car[0]['nm']
        coordin = search_coordinate(car_number)
        coordin = sheet[f'{coordin}'].row
        for data in car:
            for letter, key in zip(column, name_key):
                completion(letter, key, coordin)
            coordin += 1

    for tuple_1, tuple_2 in zip(cell_number, cell_date):
        for value_1, value_2 in zip(tuple_1, tuple_2):
            if value_1.value != None:
                date_coordin = value_1.coordinate
                date_coordin = sheet[date_coordin].offset(row=0, column=3).coordinate
                if sheet[date_coordin].value == None:
                    dictionary_car_missing['nm'] = value_1.value
                    dictionary_car_missing['date'] = str(value_2.value)[:10]
                    car_missing.append(dictionary_car_missing.copy())


    book.save("report_2.xlsx")
    book.close()
    return car_missing


