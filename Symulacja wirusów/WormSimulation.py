import copy
import time
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
        virus_label = tk.Label(choose_virus_frame, text="Wybierz robaka")
        virus_label.pack()

        def selection_changed(event):
            self.selected_virus = combo_box.get()
            print(f"Selected Virus: {self.selected_virus}")

        combo_box = ttk.Combobox(choose_virus_frame, values=["Robak Morrisa"])
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
        self.game.computers = [[Objects.Computer() for _ in range(rows)] for _ in range(columns)]
        computer_zero_x = random.randint(0, rows - 1)
        computer_zero_y = random.randint(0, rows - 1)
        self.game.computers[computer_zero_x][computer_zero_y].change_state("INFECTED")
        self.change_colors(self.squares, computer_zero_x, computer_zero_y, "red")
        control = 1
        self.game.worm = self.game.get_worm()
        self.root.update()
        counter = 0
        patched = [0]
        hard_reset = [0]
        uninfected = [0]
        infected = [0]
        while control < steps:
            coordinates = self.game.one_day(rows, columns)
            for element in coordinates:
                if element is not None:
                    x = element[0]
                    y = element[1]
                    color = element[2]
                    match color:
                        case 1:
                            self.change_colors(self.squares, element[0], element[1], "red")
                            self.game.computers[x][y].change_state("INFECTED")
                            if self.game.computers[x][y].first_infected == 0:
                                counter = counter + 1
                        case 2:
                            self.change_colors(self.squares, element[0], element[1], "green")
                            self.game.computers[x][y].change_state("UNINFECTED")
                        case 3:
                            self.change_colors(self.squares, element[0], element[1], "yellow")
                            self.game.computers[x][y].change_state("HARD_RESET")
                        case 4:
                            self.change_colors(self.squares, element[0], element[1], "blue")
                            self.game.computers[x][y].change_state("PATCHED")
                    self.root.update()
            infected_counter = sum(1 for element in coordinates if element[2] == 1)
            patched_counter = sum(1 for element in coordinates if element[2] == 4)
            hard_reset_counter = sum(1 for element in coordinates if element[2] == 3)
            uninfected_counter = sum(1 for element in coordinates if element[2] == 2)
            infected.append(100*infected_counter/self.population)
            patched.append(100*patched_counter/self.population)
            uninfected.append(100*uninfected_counter/self.population)
            hard_reset.append(100*hard_reset_counter/self.population)
            control = control + 1
            if keyboard.is_pressed('esc'):
                break

        x = list(range(0, steps))
        plt.plot(x, infected, label='Zainfekowane', color='red')
        plt.plot(x, uninfected, label='Niezainfekowane', color='green')
        plt.plot(x, patched, label='Patched', color='blue')
        plt.plot(x, hard_reset, label='Hard reset', color='yellow')
        plt.xlabel('Krok symulacji')
        plt.ylabel('Liczba populacji w danym stanie w danym kroku[%]')
        plt.title('Symulacja rozprzestrzeniania się: ' + self.selected_virus)
        plt.legend()
        plt.show()

        fatality_result = "Zainfekowano " + "{:.2f}".format(100 * (counter / self.population)) + "% populacji"
        self.print_fatality_rate(self.root, fatality_result)
        self.root.update()
        #exit()

class Game:
    def __init__(self, population, selected_worm):
        self.population = population
        self.worm = selected_worm
        self.computers = None

    def count_neighbors(self, computers, x, y):
        sick_neighbors = 0
        sick_neighbors += computers[x][(y + 1) % len(computers)].is_infected()       # for i in range(-1, 2):
        sick_neighbors += computers[x][(y - 1) % len(computers)].is_infected()       # for i in range(-1, 2):
        sick_neighbors += computers[(x + 1) % len(computers)][y].is_infected()       # for i in range(-1, 2):
        sick_neighbors += computers[(x - 1) % len(computers)][y].is_infected()       # for i in range(-1, 2):
        # for i in range(-1, 2):
        #     for j in range(-1, 2):
        #         if i == 0 and j == 0:
        #             continue
        #         sick_neighbors += humans[(x + i) % len(humans)][(y + j) % len(humans)].is_infected()

        return sick_neighbors

    '''
    2 - niezainfekowany
    1 - zainfekowany 
    '''
    def before_infection(self, computers, x, y, infectivity):
        if computers[x][y].is_uninfected():
            sick_neighbors = self.count_neighbors(computers, x, y)
            binom_sample = sum(np.random.binomial(1, infectivity, sick_neighbors))
            if binom_sample > 0:
                return [x, y, 1]
            else:
                return[x, y, 2]

    '''
    3 - hard_reset
    4 - patched 
    '''

    def after_infection(self, computers, x, y, infectivity):
        if np.random.binomial(1, 0.2):
            return [x, y, 4]
        elif np.random.binomial(1, 0.35):
            return [x, y, 3]
        else:
            return [x, y, 1]


    def get_worm(self):
        if self.worm == "Robak Morrisa":
            return Objects.Worm(0.3)

    def one_day(self, rows, columns):
        computers_copy = copy.copy(self.computers)
        clear_computers = copy.copy(self.computers)
        coordinate_list = []
        for x in range(rows):
            for y in range(columns):
                computers_copy = copy.copy(self.computers)
                if self.computers[x][y].is_uninfected():
                    if np.random.binomial(1, 0.004):
                        coordinate_list.append([x, y, 4])
                    else:
                        coordinate_list.append(self.before_infection(computers_copy, x, y, self.worm.infectivity))
                elif self.computers[x][y].is_infected():
                    coordinate_list.append(self.after_infection(computers_copy, x, y, self.worm.infectivity))
                    self.computers[x][y].first_infected = self.computers[x][y].first_infected - 1
                elif self.computers[x][y].is_hard_reset():
                    coordinate_list.append([x, y, 2])
                elif self.computers[x][y].is_patched():
                    coordinate_list.append([x, y, 4])
        return coordinate_list


gui = GUI()
