import pandas as pd
from pandas.core.frame import DataFrame

file_name = 'phonebook.csv'

# Считываем файл в датафрейм для последующей работы с данными
data = pd.read_csv(file_name, header=None, names=['Surname',
                                                  'Name',
                                                  'Patronymic',
                                                  'Organization',
                                                  'Workphone',
                                                  'Homephone'])

# Удаляем лишнии пробелы в датафрейме
data = data.applymap(lambda x: x.strip() if isinstance(x, str) else x)


def get_entries(chunk_size=2):
    """
    Вывод постранично записей из датафрейма, по умолчанию 2 записи
    """
    total_rows = len(data)
    start_index = 0

    while start_index < total_rows:
        end_index = start_index + chunk_size
        if end_index > total_rows:
            end_index = total_rows

        chunk = data[start_index: end_index]
        print(chunk)

        if end_index == total_rows:
            break

        continue_reading = ''
        while continue_reading not in ('y', 'n'):
            # Для последующего вывода нажать y, для выхода из режима чтения нажать n
            continue_reading = input('Do you want to continue? y/n: ')
        if continue_reading == 'y':
            start_index += chunk_size
            continue
        else:
            break


def add_entry():
    """
    Добавление новой записи в файл
    """
    global data
    surname = input('Enter surname: ')
    name = input('Enter name: ')
    patronymic = input('Enter patronymic: ')
    organization = input('Enter organization: ')
    work_phone_number = input('Enter workphone number: ')
    home_phone_number = input('Enter homephone number: ')

    new_entry = {'Surname': [surname],
                              'Name': [name],
                              'Patronymic': [patronymic],
                              'Organization': [organization],
                              'Workphone': [work_phone_number],
                              'Homephone': [home_phone_number]}

    data = pd.concat([data, pd.DataFrame.from_records(new_entry)], ignore_index=True)
    data.to_csv('phonebook.csv', index=False, header=False)


def search_entry() -> DataFrame:
    """
    Поиск записи по одному или нескольким параметрам, если записей несколько, то можно уточнить следующий параметр,
    пока не останется только одна запись
    :return: датафрейм с единственной записью, которую можно потом изменить
    """
    field = ''
    entry = data.astype(str)

    columns_list_lower = list(map(str.lower, data.columns.tolist()))
    while True:
        while field not in columns_list_lower:
            field = input(f'Enter field name from following values {data.columns.tolist()}, which you want to search: ').strip().lower()
        field_idx = columns_list_lower.index(field)
        field = data.columns.tolist()[field_idx]
        search_value = ''
        while search_value not in list(map(str.strip, entry[field].tolist())):
            search_value = input('Enter field value, which you want to find: ')
            print('There is no entry with such parameter, try again')

        entry = entry[entry[field] == search_value]
        if len(entry) > 1:
            print(entry)
            print('There are more then one entry, choose another column for search from following fields: ')
        elif len(entry) == 1:
            print(entry)
            return entry
        else:
            print('No entries? Please choose one more column for search')


def update_entry():
    # Проводим поиск нужной записи для дальнейшего ее изменения
    entry = search_entry()

    field = ''
    columns_list_lower = list(map(str.lower, data.columns.tolist()))
    while field not in columns_list_lower:
        field = input(f'Enter column name, which you want to change from following {data.columns.tolist()}: ').strip().lower()
    new_value = input('Enter new value: ')
    field_idx = columns_list_lower.index(field)
    entry_idx = entry.index.tolist()[0]
    data.loc[entry_idx, data.columns.tolist()[field_idx]] = new_value
    print(data)
    data.to_csv('phonebook.csv', index=False, header=False)


def main():
    """
    Main loop программы, где можно выбирать последовательно действия, реализующие функционал программы
    """
    actions = {'read': get_entries, 'search': search_entry, 'update': update_entry, 'add': add_entry}
    while True:
        selected_action = input('What would you like to do? (Read, Search, Update, Add, End): ').lower()
        if selected_action in ('read', 'search', 'update', 'add', 'end'):
            if selected_action == 'end':
                break
            else:
                actions[selected_action]()
        else:
            continue


# Точка входа в программу
if __name__ == '__main__':
    main()
