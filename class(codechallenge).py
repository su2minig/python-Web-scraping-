class Player:

  def __init__(self, name, team):
    self.name = name
    self.xp = 1400
    self.team = team

  def introduce(self):
    print(f"Hello, I'm {self.name} and I'm on {self.team}")


class Team:

  def __init__(self, team_name):
    self.team_name = team_name
    self.players = []

  def show_players(self):
    for player in self.players:
      player.introduce()

  def show_team_xp(self):
    total_xp = 0
    for player in self.players:
      total_xp += player.xp
    print(f"{self.team_name}Total XP: {total_xp}")

  def add_player(self, name):
    new_player = Player(name, self.team_name)
    self.players.append(new_player)

  def remove_player(self, name):
    for player in self.players:
      if player.name == name:
        self.players.remove(player)

team_CR = Team("CR")
team_CR.add_player("Su")
team_CR.add_player("Jim")
team_T1 = Team("T1")
team_T1.add_player("Min")
team_T1.add_player("Jun")
team_T1.add_player("Jimmy")

team_CR.show_players()
team_T1.show_players()

team_CR.show_team_xp()
team_T1.show_team_xp()