import random

class EloManager:

    def win_probability(self, rating_a, rating_b):
        return 1 / (1 + 10 ** ((rating_b - rating_a) / 400)) # ** is: 2^3 --> 2 ** 3
    
    def update_ratings(self, r_a, r_b, result, k=20):
        p_a = self.win_probability(r_a, r_b)

        r_a_new = r_a + k * (result - p_a)
        r_b_new = r_b + k * ((1 - result) - (1 - p_a))
        return r_a_new, r_b_new
    
    # function only for testing purposes
    def simulate_games(self):
        t_a = Team("Edmonton")
        t_b = Team("Vancouver")

        result = 1

        for i in range(5):
            team_a_prob = self.win_probability(t_a.elo, t_b.elo)

            num = random.random()
            if num <= team_a_prob:
                result = 1
            else:
                result = 0

            t_a.elo, t_b.elo = self.update_ratings(t_a.elo, t_b.elo, result)

        print(f"Edmonton: {t_a.elo}, Vancouver: {t_b.elo}")

class Team:
    def __init__(self, name):
        self.name = name
        self.elo = 1500     

e = EloManager()
e.simulate_games()


    