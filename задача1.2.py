half1 = number // 1000
half2 = number % 1000
if (half1 // 100) + ((half1 // 10) % 10) + (half1 % 10) == (half2 // 100) + ((half2 // 10) % 10) + (half2 % 10):
  print("Счастливый билет")
else:
  print("Несчастливый билет")
