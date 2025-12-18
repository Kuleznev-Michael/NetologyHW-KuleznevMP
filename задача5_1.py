from datetime import datetime

while True:
    user_input = str(input())
    if user_input == "q":
        break
    try:
        output = datetime.strptime(user_input, "%A, %B %d, %Y")
    except:
        pass
    try:
        output = datetime.strptime(user_input, "%A, %d.%m.%y")
    except:
        pass
    try:
        output = datetime.strptime(user_input, "%A, %d %B %Y")
    except:
        pass
    try:
        print(output)
    except:
        pass