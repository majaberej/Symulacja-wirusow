class Human:
    states = {"UNINFECTED": 0, "INFECTED": 1, "IMMUNE": 2, "DEAD": 3}

    def __init__(self):
        self.illness_length = 0
        self.immunity_length = 0
        self.day_of_illness = 0
        self.immunity_duration = 0
        self.state = self.states["UNINFECTED"]
        self.first_dead = 1

    def change_state(self, new_state):
        self.state = self.states[new_state]

    def is_infected(self):
        return self.state == self.states["INFECTED"]

    def is_uninfected(self):
        return self.state == self.states["UNINFECTED"]

    def is_immune(self):
        return self.state == self.states["IMMUNE"]

    def is_dead(self):
        return self.state == self.states["DEAD"]


class Computer:
    states = {"UNINFECTED": 0, "INFECTED": 1, "HARD_RESET": 2, "PATCHED": 3}

    def __init__(self):
        self.state = self.states["UNINFECTED"]
        self.first_infected = 1

    def change_state(self, new_state):
        self.state = self.states[new_state]

    def is_infected(self):
        return self.state == self.states["INFECTED"]

    def is_uninfected(self):
        return self.state == self.states["UNINFECTED"]

    def is_hard_reset(self):
        return self.state == self.states["HARD_RESET"]

    def is_patched(self):
        return self.state == self.states["PATCHED"]


class BiologicalVirus:

    def __init__(self, infectivity, mortality, mean_duration, immunity_time):
        self.infectivity = infectivity
        self.mortality = mortality
        self.mean_duration = mean_duration
        self.immunity_time = immunity_time


class Worm:

    def __init__(self, infectivity):
        self.infectivity = infectivity

#
# class AntiWorm:
#
#     def __init__(self, infectivity):
#         self.infectivity = infectivity
