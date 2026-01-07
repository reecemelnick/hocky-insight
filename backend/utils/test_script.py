from nhlpy import NHLClient
client = NHLClient(debug=True)
scores_dict = client.game_center.daily_scores(date="2024-07-02")
games = scores_dict.get("games", [])
print(games)