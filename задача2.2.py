if len(boys) != len(girls):
    print("Результат: Внимание, кто-то может остаться без пары.")
else:
    print("Идеальные пары:")
    girls.sort()
    boys.sort()
    for i in range(len(boys)):
        print(boys[i],"и",girls[i])