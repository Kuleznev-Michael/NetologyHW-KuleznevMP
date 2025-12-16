import csv
with open('web_clients_correct.csv') as f:
    reader = csv.reader(f)
    f1 = open("7_1output.txt", "w")
    for row in reader:
        if row[0] == "name":
            continue
        if row[3] == "male":
            sex = "мужского"
        else:
            sex = "женского"
        if row[1] in ["mobile", "tablet"]:
            device_type = "мобильного"
        else:
            device_type = "компьютерного"
        if float(row[4]) % 1 != 0:
            age = "лет"
        elif 10 <= int(row[4]) <= 19 or int(row[4]) % 10 in [0, 5, 6, 7, 8, 9]:
            age = "лет"
        elif int(row[4]) % 10 == 1:
            age = "год"
        else:
            age = "года"
        if sex == "мужского":
            sex2 = "совершил"
        else:
            sex2 = "совершила"
        f1.write(f'Пользователь {row[0]} {sex} пола {row[4]} {age} {sex2} покупку на {row[5]} у.е. с {device_type} '
              f'браузера {row[2]}. Регион, из которого совершалась покупка: {row[6]}.\n')