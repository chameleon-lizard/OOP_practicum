from turtle import width
from typing import List
import matplotlib.pyplot as plt
import tkinter as tk
import sys

from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from insurances import Car, Home, Life

from simulation import Simulation


class App():
    '''
    Class for GUI of the application.
    '''

    def __init__(self) -> None:
        '''
        Constructor that creates the base GUI.
        '''
        # Creating the window
        self.window = tk.Tk()
        self.window.title("Insurance company simulation")

        # Creating plt widget
        self.fig = plt.figure()

        self.ax = plt.gca()
        self.ax.set_xlabel("Time")
        self.ax.set_ylabel("Money")

        self.canvas = FigureCanvasTkAgg(self.fig, master=self.window)
        self.canvas.get_tk_widget().grid(row=0, column=0, rowspan=3)
        self.canvas.draw()

        # Creating button for simulation step
        self.b_step = tk.Button(self.window, text="Step",
                                command=self.__step, width=13, height=3)
        self.b_step.grid(row=0, column=1)

        # Creating the list of expired insurances
        self.l_expired = tk.Listbox(self.window)
        self.l_expired.grid(row=1, column=1)

        # Creating button for changing expired insurance parameters
        self.b_expired = tk.Button(
            self.window, text="Change parameters", command=self.__change)
        self.b_expired.grid(row=2, column=1)

        # Creating listbox widget for logs
        self.l_logs = tk.Listbox(self.window, width=106)
        self.l_logs.grid(row=3, column=0)

        # Creating textbox widget for scores
        self.t_scores = tk.Text(self.window, width=15, height=10)
        # self.t_scores.config(state=tk.DISABLED)
        self.t_scores.grid(row=3, column=1)

        # Binding exit function to close window signal
        self.window.protocol("WM_DELETE_WINDOW", self._close)

        # Simulation
        self.simulation = Simulation()

        # Main loop of the application
        self.window.mainloop()

    def __step(self) -> None:
        '''
        Advance the simulation.
        '''
        text, last = self.simulation.step()

        if not last:
            self.b_step.destroy()

        self.l_expired.delete(0, tk.END)

        for i in self.simulation.company.stopped:
            self.l_expired.insert(tk.END, i)

        self.ax.plot(list(i for i, _ in self.simulation.stats.money),
                     list(i for _, i in self.simulation.stats.money))
        self.canvas.draw()

        self.l_logs.insert(tk.END, text)

        self.t_scores.delete(0.0, tk.END)
        self.t_scores.insert(
            0.0, f"Step: {self.simulation.stats.step}\nScore: {round(self.simulation.stats.money[-1][1], 3)}\nLife sold: {self.simulation.stats.sold[-1][0]}\nCar sold: {self.simulation.stats.sold[-1][1]}\nHome sold: {self.simulation.stats.sold[-1][2]}\n")

    def __close_modal(self, insurancetype: str, insurance_params: List[int | float]) -> None:
        '''
        Closing modal window and making changes.
        '''
        self.simulation.company.change_insurance_params(
            insurancetype=insurancetype, insurance_params=insurance_params)
        self.pop.destroy()

    def __modal(self, insurance: Life | Car | Home) -> None:
        '''
        Creating a popup modal window to configure parameters of the selected insurance.
        '''
        # Creating a popup window
        self.pop: tk.Toplevel = tk.Toplevel(self.window)

        # Setting the parameters of the popup
        self.pop.title("Correct params")
        self.pop.config(bg="white")

        # Create a label for length
        l_length = tk.Label(self.pop, text="Length")
        l_length.grid(row=0, column=0)

        # Create a textbox for length
        t_length = tk.Text(self.pop, height=1, width=10)
        t_length.insert(1.0, f"{insurance.until}")
        t_length.grid(row=1, column=0)

        # Create a label for cost
        l_cost = tk.Label(self.pop, text="Cost")
        l_cost.grid(row=2, column=0)

        # Create a textbox for cost
        t_cost = tk.Text(self.pop, height=1, width=10)
        t_cost.insert(1.0, f"{insurance.cost}")
        t_cost.grid(row=3, column=0)

        # Create a label for payout
        l_payout = tk.Label(self.pop, text="Payout")
        l_payout.grid(row=0, column=1)

        # Create a textbox for payout
        t_payout = tk.Text(self.pop, height=1, width=10)
        t_payout.insert(1.0, f"{insurance.payout}")
        t_payout.grid(row=1, column=1)

        # Create a label for franchise
        l_franchise = tk.Label(self.pop, text="Franchise")
        l_franchise.grid(row=2, column=1)

        # Create a textbox for franchise
        t_franchise = tk.Text(self.pop, height=1, width=10)
        t_franchise.insert(1.0, f"{insurance.franchise}")
        t_franchise.grid(row=3, column=1)

        # Create a button for accept
        # Using lambda for binding reasons
        b_accept = tk.Button(self.pop, text="Accept", command=lambda: self.__close_modal(insurance.type, [float(t_cost.get(1.0, tk.END)), int(
            t_length.get(1.0, tk.END)), float(t_payout.get(1.0, tk.END)), float(t_franchise.get(1.0, tk.END)), insurance.demand]))

        b_accept.grid(row=4, column=0, columnspan=2)

    def __change(self) -> None:
        '''
        Change expired insurance parameters.
        '''
        try:
            selection = self.l_expired.curselection()[0]
            insurance = self.simulation.company.stopped[selection - 1]
            self.__modal(insurance)
            self.simulation.company.stopped.remove(insurance)
            self.l_expired.delete(selection)
        except:
            pass

    def _close(self) -> None:
        '''
        For exiting the application.
        '''
        sys.exit()


if __name__ == "__main__":
    app = App()
