class Puppy:

  def __init__(self, name, breed):  # class 안에 있는 method는 자동적으로 argument 하나를 받는다.
    print("Puppy is born")
    self.name = name
    self.breedd = breed

  def __str__(self):
    return f"Puppy name is {self.name}, breed is {self.breedd}"

ruffus = Puppy(name="ruffus", breed="golden")
bibi = Puppy(name="bibi", breed="beagle")
print(ruffus,bibi)