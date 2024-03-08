import math
import random
import tkinter as tk
from tkinter import ttk
import numpy as np
import Objects
from scipy.stats import binom


class GUI:

    def __init__(self):
        self.root = tk.Tk()
        self.create_root()

    def choose_virus(self, options_frame):

        choose_virus_frame = tk.Frame(options_frame, bg='#f0e8e6')
        choose_virus_frame.grid(row=0, column=0, padx=20, pady=10)
        choose_virus_frame.config(height=int(0.6 * options_frame.winfo_height()),
                                  width=int(0.25 * options_frame.winfo_width()))
        virus_label = tk.Label(choose_virus_frame)
        virus_label.config(text="Wybierz wirusa")
        virus_label.pack()

        def selection_changed(event):
            virus = combo_box.get()
            print(f"Selected Virus: {virus}")

        combo_box = ttk.Combobox(choose_virus_frame, values=["Odra", "Ospa", "COVID-19", "Robak Morrisa"])
        combo_box.bind("<<ComboboxSelected>>", selection_changed)
        combo_box.pack(expand=True)

    def choose_population(self, options_frame):

        set_population_frame = tk.Frame(options_frame, bg='#f0e8e6')
        set_population_frame.grid(row=0, column=1, padx=20, pady=20)
        set_population_frame.config(height=int(0.6 * options_frame.winfo_height()),
                                    width=int(0.25 * options_frame.winfo_width()))
        population_label = tk.Label(set_population_frame)
        population_label.config(text="Podaj wielkość populacji")
        population_label.pack()
        population_field = tk.Entry(set_population_frame)
        population_field.pack(expand=True)
        def on_entry_return(event):
            population_value = population_field.get()
            print(f"Population set to: {population_value}")

        population_field.bind("<Return>", on_entry_return)
        while population_field.get() is None:

        return population_field.get()

    def create_root(self):

        self.root.title("Symulacja")
        self.root.minsize(width=600, height=600)
        self.root.update_idletasks()

        options_frame = tk.Frame(self.root, bg='#f0e8e6')
        options_frame.pack(fill=tk.X)
        options_frame.config(height=(0.20 * self.root.winfo_height()), width=self.root.winfo_width())

        self.choose_virus(options_frame)
        self.choose_population(options_frame)





        simulation_frame = tk.Frame(self.root, bg='#F6E0DD')
        simulation_frame.pack(fill=tk.X)
        simulation_frame.config(height=(0.8 * self.root.winfo_height()), width=self.root.winfo_width())

        grid_frame = tk.Frame(simulation_frame, bg='#F6E0DD')
        grid_frame.pack()
        grid_frame.config(height=(0.8 * self.root.winfo_height()), width=self.root.winfo_width())
        grid_frame.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

        def start_simulation():  # po wciśnięciu przycisku start
            virus = combo_box.get()
            population_value = population_field.get()
            if virus == "Odra":
                Odra = Objects.BiologicalVirus(0.9, 0.15, 11, np.inf)
                virus = Odra
                simulation = human_simulation(Odra, population_value, grid_frame)
            elif virus == "Ospa":
                Ospa = Objects.BiologicalVirus(0.6, 0.3, 20, np.inf)
                virus = Ospa
                simulation = human_simulation(Ospa, population_value, grid_frame)
            elif virus == "COVID-19":
                COVID19 = Objects.BiologicalVirus(0.9, 0.024, 10, 180)
                virus = COVID19
                simulation = human_simulation(COVID19, population_value, grid_frame)
                simulation.simulation()

                # else:
                # tworzenie instancji obiektu symulacja robaka komputerowego o parametrach: robak i wielkość populacji

        start_button = tk.Button(options_frame, text="Start", command=start_simulation)
        start_button.grid(row=0, column=2, padx=20, pady=20)

        def update_frame_sizes(event):
            options_frame.config(height=int(0.20 * self.root.winfo_height()), width=self.root.winfo_width())
            simulation_frame.config(height=(0.80 * self.root.winfo_height()), width=self.root.winfo_width())

        def update_options_frame_sizes(event):
            choose_virus_frame.config(height=int(0.6 * options_frame.winfo_height()),
                                      width=int(0.25 * options_frame.winfo_width()))
            set_population_frame.config(height=int(0.6 * options_frame.winfo_height()),
                                        width=int(0.25 * options_frame.winfo_width()))

        root.bind("<Configure>", update_frame_sizes)
        options_frame.bind("<Configure>", update_options_frame_sizes)

        root.mainloop()

    def create_grid(grid_frame, rows, columns):
        squares = [[None] * columns for _ in range(rows)]

        for row in range(rows):
            for col in range(columns):
                square = tk.Canvas(grid_frame, width=10, height=10)
                square.configure(bg="green")
                square.grid(row=row, column=col)
                squares[row][col] = square

        return squares

    def change_colors(squares, x, y, color):
        squares[x][y].configure(bg=color)


# LUDZIE
def illness_probability(humans, x, y, infectivity):  # Zwraca prawdopodbieństwo zarażenia
    sick_neighbors = 0
    for i in range(-1, 2):
        for j in range(-1, 2):
            if i == 0 and j == 0:
                continue
            sick_neighbors += humans[(y + i) % len(humans)][(x + j) % len(humans)].is_infected()

    index = 1 / 7
    match sick_neighbors:
        case 0:
            return 0
        case 1:
            return infectivity
        case _:
            return infectivity * (1 + (sick_neighbors - 1) * index)


def infection(humans, x, y, infectivity, mean_duration, squares):
    probability = illness_probability(humans, x, y, infectivity)
    if binom(1, probability):
        humans[x][y].change_state("INFECTED")
        humans[x][y].illness_length = random.randint(mean_duration - 2, mean_duration + 2)
        humans[x][y].day_of_illness = 1
        change_colors(squares, x, y, "red")


# KOMPUTERY
def illness_probabilityC(computers, x, y, infectivity):  # Zwraca prawdopodbieństwo zarażenia

    sick_neighbors = 0
    for i in range(-1, 2):
        for j in range(-1, 2):
            if i == 0 and j == 0:
                continue
            sick_neighbors += computers[(y + i) % len(computers)][(x + j) % len(computers)].is_infected()

    index = 1 / 7
    match sick_neighbors:
        case 1:
            return infectivity
        case _:
            return infectivity * (1 + (sick_neighbors - 1) * index)


def infectionC(computers, x, y, infectivity, squares):
    probability = illness_probability(computers, x, y, infectivity)
    if binom(1, probability):
        computers[x][y].change_state("INFECTED")
        change_colors(squares, x, y, "red")


# GUI


class human_simulation:
    def __init__(self, virus, population, simulation_frame):
        self.virus = virus
        self.population = int(population)
        self.simulation_frame = simulation_frame

    def simulation(self):
        rows = int(math.sqrt(self.population))
        columns = rows
        squares = create_grid(self.simulation_frame, rows, columns)
        humans = [[Objects.Human() for _ in range(rows)] for _ in range(columns)]
        patient_zero_x = random.randint(0, rows - 1)
        patient_zero_y = random.randint(0, rows - 1)
        humans[patient_zero_x][patient_zero_y].change_state("INFECTED")
        change_colors(squares, patient_zero_x, patient_zero_y, "red")
        for i in range(100):
            self.one_day(rows, columns, humans, squares)

    def one_day(self, rows, columns, humans, squares):
        for x in range(rows):
            for y in range(columns):
                if not humans[x][y].is_infected():
                    infection(humans, x, y, self.virus.infectivity, self.virus.mean_duration, squares)


# MAIN
def main():
    # RobakMorrisa = Objects.Worm(0.8) #trzeba eksperymentować
    create_root()


# computers = [[Objects.Computer] * columns for _ in range(rows)]

if __name__ == "__main__":
    main()
