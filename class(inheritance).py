class Dog:
  def __init__(self, name, breed):
      self.name = name
      self.breed = breed

class Puppy(Dog):

  def __init__(self, name, breed):
      super().__init__(name, breed)

  def woof_woof(self):
      print("Woof Woof")

class GuardDog(Dog):

  def __init__(self, name, breed):
      super().__init__(name, breed)
      self.aggresive = True

  def rrrrr(self):
      print("RRRRR")

ruffus = Puppy(name="Ruffus", breed="Poodle")
bibi = GuardDog(name="Bibi", breed="German Shepherd")

print(ruffus.woof_woof())
print(bibi.rrrrr())