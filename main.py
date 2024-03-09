days_of_week = [
    "Monday",
    "Tuesday",
    "Wednesday",
    "Thursday",
    "Friday",
    "Saturday",
    "Sunday",
]

print(days_of_week.count("Wednesday")) # method count()
# 메소드는 데이터 타입에 따라 사용할 수 있는 함수를 의미한다.
days_of_week.remove("Sunday")
print(days_of_week)
days_of_week.append("Sunday")
print(days_of_week)