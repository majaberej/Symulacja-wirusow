import copy
import tkinter as tk
from tkinter import ttk
from math import sqrt
import random
import Objects
import numpy as np
import keyboard
import matplotlib.pyplot as plt

class GUI:
    def __init__(self):
        self.game = None
        self.root = tk.Tk()
        self.create_root()
        self.squares = None
        self.selected_virus = None
        self.population = None

    def choose_virus(self, options_frame):
        choose_virus_frame = tk.Frame(options_frame, bg='#f0e8e6')
        choose_virus_frame.grid(row=0, column=0, padx=20, pady=10)
        choose_virus_frame.config(height=int(0.6 * options_frame.winfo_height()),
                                  width=int(0.25 * options_frame.winfo_width()))
        virus_label = tk.Label(choose_virus_frame, text="Wybierz wirusa")
        virus_label.pack()

        def selection_changed(event):
            self.selected_virus = combo_box.get()
            print(f"Selected Virus: {self.selected_virus}")

        combo_box = ttk.Combobox(choose_virus_frame, values=["Odra", "Ospa", "COVID-19"])
        combo_box.bind("<<ComboboxSelected>>", selection_changed)
        combo_box.pack(expand=True)

    def choose_population(self, options_frame):
        def on_entry_return(event):
            self.population = int(population_field.get())
            print(f"Population set to: {self.population}")
            self.create_grid(int(sqrt(int(self.population))), int(sqrt(int(self.population))))
            self.game = Game(self.population, self.selected_virus)
        set_population_frame = tk.Frame(options_frame, bg='#f0e8e6')
        set_population_frame.grid(row=0, column=1, padx=20, pady=20)
        set_population_frame.config(height=int(0.6 * options_frame.winfo_height()),
                                    width=int(0.25 * options_frame.winfo_width()))
        population_label = tk.Label(set_population_frame, text="Podaj wielkość populacji")
        population_label.pack()
        population_field = tk.Entry(set_population_frame)
        population_field.pack(expand=True)
        population_field.bind("<Return>", on_entry_return)

    def print_fatality_rate(self, root, fatality_rate):
        fatality_rate_label = tk.Label(root, text=fatality_rate, font=10)
        fatality_rate_label.config(bg='#F6E0DD')
        fatality_rate_label.pack()

    def create_root(self):
        self.root.title("Symulacja")
        self.root.config(bg='#F6E0DD')
        self.root.minsize(width=600, height=600)
        self.root.update_idletasks()

        options_frame = tk.Frame(self.root, bg='#f0e8e6')
        options_frame.pack(fill=tk.X)
        options_frame.config(height=(0.20 * self.root.winfo_height()), width=self.root.winfo_width())

        self.choose_virus(options_frame)
        self.choose_population(options_frame)
        start_button = tk.Button(options_frame, text="Start", command=self.start_simulation)
        start_button.grid(row=0, column=2, padx=5, pady=5)
        self.root.mainloop()


    def start_simulation(self):
        self.main()

    def create_grid(self, rows, columns):
        simulation_frame = tk.Frame(self.root, bg='#F6E0DD')
        simulation_frame.pack(fill=tk.X)
        simulation_frame.config(height=(0.8 * self.root.winfo_height()), width=self.root.winfo_width())
        grid_frame = tk.Frame(simulation_frame, bg='#F6E0DD')
        grid_frame.pack()
        grid_frame.config(height=(0.8 * self.root.winfo_height()), width=self.root.winfo_width())
        grid_frame.place(relx=0.5, rely=0.5, anchor=tk.CENTER)
        self.squares = [[None] * columns for _ in range(rows)]

        for row in range(rows):
            for col in range(columns):
                square = tk.Canvas(grid_frame, width=10, height=10, bg="green")
                square.grid(row=row, column=col)
                self.squares[row][col] = square

    def change_colors(self, squares, x, y, color):
        squares[x][y].configure(bg=color)


    def main(self):
        rows = int(sqrt(self.population))
        columns = rows
        steps = 50
        self.game.humans = [[Objects.Human() for _ in range(rows)] for _ in range(columns)]
        patient_zero_x = random.randint(0, rows - 1)
        patient_zero_y = random.randint(0, rows - 1)
        self.game.humans[patient_zero_x][patient_zero_y].change_state("INFECTED")
        self.change_colors(self.squares, patient_zero_x, patient_zero_y, "red")
        self.game.humans[patient_zero_x][patient_zero_y].illness_length = int(np.random.normal(self.game.get_virus().mean_duration, 3))
        self.game.humans[patient_zero_x][patient_zero_y].day_of_illness = 1
        control = 1
        self.game.virus = self.game.get_virus()
        self.root.update()
        counter = 0
        deaths = [0]
        immunity = [0]
        uninfected = [0]
        infected = [0]
        while control < steps:
            deaths_counter = 0
            immunity_counter = 0
            uninfected_counter = 0
            infected_counter = 0
            coordinates = self.game.one_day(rows, columns)
            for element in coordinates:
                if element is not None:
                    x = element[0]
                    y = element[1]
                    color = element[2]
                    match color:
                        case 0:
                            self.change_colors(self.squares, element[0], element[1], "black")
                            self.game.humans[x][y].change_state("DEAD")
                            if self.game.humans[x][y].first_dead == 0:
                                counter = counter + 1
                        case 1:
                            self.change_colors(self.squares, element[0], element[1], "red")
                            self.game.humans[x][y].change_state("INFECTED")
                            self.game.humans[x][y].illness_length = int(np.random.normal(self.game.virus.mean_duration, 3))
                        case 2:
                            self.change_colors(self.squares, element[0], element[1], "blue")
                            self.game.humans[x][y].change_state("IMMUNE")
                        case 3:
                            self.change_colors(self.squares, element[0], element[1], "green")
                            self.game.humans[x][y].change_state("UNINFECTED")
                    self.root.update()
                    #time.sleep(0.001)
            deaths_counter = sum(1 for element in coordinates if element[2] == 0)
            immunity_counter = sum(1 for element in coordinates if element[2] == 2)
            infected_counter = sum(1 for element in coordinates if element[2] == 1)
            uninfected_counter = sum(1 for element in coordinates if element[2] == 3)
            deaths.append(100*deaths_counter/self.population)
            immunity.append(100*immunity_counter/self.population)
            infected.append(100*infected_counter/self.population)
            uninfected.append(100*uninfected_counter/self.population)
            control = control + 1
            if keyboard.is_pressed('esc'):
                break
        x = list(range(0, steps))
        plt.plot(x, deaths, label='Zgony', color='black')
        plt.plot(x, immunity, label='Osoby odporne', color='blue')
        plt.plot(x, infected, label='Osoby zakażone', color='red')
        plt.plot(x, uninfected, label='Osoby zdrowe', color='green')
        plt.xlabel('Krok symulacji')
        plt.ylabel('Liczba populacji w danym stanie w danym kroku[%]')
        plt.title('Symulacja rozprzestrzeniania się wirusa choroby: ' + self.selected_virus)
        plt.legend()
        plt.show()

        fatality_result = "Umarło " + "{:.2f}".format(100 * (counter / self.population)) + "% populacji"
        self.print_fatality_rate(self.root, fatality_result)
        self.root.update()
        #exit()

class Game:
    def __init__(self, population, selected_virus):
        self.population = population
        self.virus = selected_virus
        self.humans = None

    def count_neighbors(self, humans, x, y):
        sick_neighbors = 0
        sick_neighbors += humans[x][(y + 1) % len(humans)].is_infected()       # for i in range(-1, 2):
        sick_neighbors += humans[x][(y - 1) % len(humans)].is_infected()       # for i in range(-1, 2):
        sick_neighbors += humans[(x + 1) % len(humans)][y].is_infected()       # for i in range(-1, 2):
        sick_neighbors += humans[(x - 1) % len(humans)][y].is_infected()       # for i in range(-1, 2):
        # for i in range(-1, 2):
        #     for j in range(-1, 2):
        #         if i == 0 and j == 0:
        #             continue
        #         sick_neighbors += humans[(x + i) % len(humans)][(y + j) % len(humans)].is_infected()

        return sick_neighbors

    '''
    3 - juz nieodporny
    1 - zainfekowany 
    '''
    def before_infection(self, humans, x, y, infectivity, mean_duration):
        if humans[x][y].is_uninfected():
            sick_neighbors = self.count_neighbors(humans, x, y)
            binom_sample = sum(np.random.binomial(1, infectivity, sick_neighbors))
            if binom_sample > 0:
                # self.humans[x][y].change_state("INFECTED")
                # humans[x][y].change_state("INFECTED")
                # humans[x][y].illness_length = int(np.random.normal(mean_duration, 3))
                # humans[x][y].day_of_illness = 1
                return [x, y, 1]
            else:
                return[x, y, 3]
        elif humans[x][y].is_immune():
            humans[x][y].immunity_length += 1
            if humans[x][y].immunity_length > humans[x][y].immunity_duration:
                # self.humans[x][y].change_state("UNINFECTED")
                # humans[x][y].change_state("UNINFECTED")
                return [x, y, 3]
            else:
                return [x, y, 2]
        elif humans[x][y].is_dead():
            return [x, y, 0]


    def get_virus(self):
        if self.virus == "Odra":
            return Objects.BiologicalVirus(0.9, 0.085, 11, np.inf) #dopasowanie mortality do rzeczywistych wyników 15%
        elif self.virus == "Ospa":
            return Objects.BiologicalVirus(0.6, 0.1, 20, np.inf) #dopasowanie mortality do rzeczywistych wyników 30%
        elif self.virus == "COVID-19":
            return Objects.BiologicalVirus(0.9, 0.015, 10, 18) #dopasowanie mortality do rzeczywistych wyników 2,4%

    def one_day(self, rows, columns):
        humans_copy = copy.copy(self.humans)
        clear_humans = copy.copy(self.humans)
        coordinate_list = []
        for x in range(rows):
            for y in range(columns):
                humans_copy = copy.copy(self.humans)
                if not self.humans[x][y].is_infected():
                    if self.humans[x][y].is_dead():
                        self.humans[x][y].first_dead = self.humans[x][y].first_dead - 1
                    coordinate_list.append(self.before_infection(humans_copy, x, y, self.virus.infectivity, self.virus.mean_duration))
                else:
                    coordinate_list.append([x, y, self.after_infection(humans_copy[x][y])])
        return coordinate_list

    '''
    0 - umarl
    1 -  nie umarl, pozostaje chory
    2 -  jest odporny
    '''
    def after_infection(self, human):
        if human.day_of_illness <= human.illness_length:
            human.day_of_illness += 1

        if human.day_of_illness >= 0.8 * human.illness_length and human.day_of_illness <= human.illness_length:
            if np.random.binomial(1, self.virus.mortality):
                # human.change_state("DEAD")
                return 0
            else:
                return 1
        elif human.day_of_illness > human.illness_length:
            #human.change_state("IMMUNE")
            if self.virus.immunity_time is np.inf:
                human.immunity_duration = np.inf
                human.immunity_length = 1
            else:
                human.immunity_duration = np.random.normal(self.virus.immunity_time, 3)
            human.immunity_length = 1
            return 2
        else:
            return 1


gui = GUI()
