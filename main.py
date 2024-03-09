user = {
  'name': 'sumin',
  'age': 22,
  'fav_food': ['pizza', 'burger'],
}

print(user.get('age'))
print(user.get('name'))
user.pop('age')
print(user)
user['level'] = 3
print(user)
user['fav_food'].append('ice cream')
print(user)