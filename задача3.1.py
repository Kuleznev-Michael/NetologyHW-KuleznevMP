price_less_20 = {name: items[name]['count'] < 20 for name in items.keys()}
print(price_less_20)