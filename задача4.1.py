documents = [
 {'type': 'passport', 'number': '2207 876234', 'name': 'Василий Гупкин'},
 {'type': 'invoice', 'number': '11-2', 'name': 'Геннадий Покемонов'},
 {'type': 'insurance', 'number': '10006', 'name': 'Аристарх Павлов'}
]

directories = {
 '1': ['2207 876234', '11-2'],
 '2': ['10006'],
 '3': []
}

while True:
    user_input = input("Введите команду:")
    if user_input == "q":
        break
    elif user_input == "p":
        doc_num = input("Введите номер документа:")
        for doc in documents:
            if doc["number"] == doc_num:
                print("Владелец документа:", doc["name"])
        found = 0
        for doc in documents:
            if doc_num == doc["number"]:
                found = 1
        if found == 0:
            print("Владелец документа: владелец не найден")
        found = 0
    elif user_input == "s":
        doc_num = input("Введите номер документа:")
        for key in directories.keys():
            if doc_num in directories[key]:
                print("Документ хранится на полке:",key)
                break

