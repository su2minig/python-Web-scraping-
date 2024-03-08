age = int(input("How old are you?"))

if age < 18:
  print("You can't drink")
elif age > 18 and age < 35: # and는 둘 다 참일 때만 참이다. 앞부분이 거짓이면 
  print("You drink beer!")  # 뒷부분은 확인하지 않는다.
elif age == 60 or age ==70:
  print("Birthday party!")  # or는 둘 중 하나만 참이면 참이다.
else:
  print("Go ahead!")