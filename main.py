import json
from pathlib import Path
from typing import Dict, List
import matplotlib.pyplot as plt
import tkinter.messagebox as tkmb
import tkinter as tk
import sys


from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from insurances import Car, Home, Life

from simulation import Simulation


class App():
    '''
    Class for GUI of the application.
    '''

    def __init__(self, path: str = "config.json") -> None:
        '''
        Constructor that creates the base GUI.
        '''
        # Creating the window
        self.window = tk.Tk()
        self.window.title("Insurance company simulation")

        self.__show_settings_popup(path)

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
        self.window.protocol("WM_DELETE_WINDOW", self.__close)

        # Simulation
        self.simulation = Simulation()

        # Main loop of the application
        self.window.mainloop()

    def __step(self) -> None:
        '''
        Advance the simulation.
        '''
        text, last = self.simulation.step()

        self.l_expired.delete(0, tk.END)

        self.l_expired.insert(tk.END, Life(*self.simulation.company.life_params))  # type: ignore
        self.l_expired.insert(tk.END, Home(*self.simulation.company.home_params))  # type: ignore
        self.l_expired.insert(tk.END, Car(*self.simulation.company.car_params))  # type: ignore

        self.ax.plot(list(i for i, _ in self.simulation.stats.money),
                     list(i for _, i in self.simulation.stats.money))
        self.canvas.draw()

        self.l_logs.insert(tk.END, text)

        self.t_scores.delete(0.0, tk.END)

        if not last:
            self.b_step["state"] = "disabled"
            self.t_scores.insert(
            0.0, f"The end.\nMoney: {round(self.simulation.stats.money[-1][1], 2)}\nLife sold: {self.simulation.stats.sold[-1][0]}\nCar sold: {self.simulation.stats.sold[-1][1]}\nHome sold: {self.simulation.stats.sold[-1][2]}\nPayouts: {round(self.simulation.stats.payouts[-1], 2)}\nActive: {len(self.simulation.company.insurances)}")
        else:
            self.t_scores.insert(
            0.0, f"Step: {self.simulation.stats.step}\nMoney: {round(self.simulation.stats.money[-1][1], 2)}\nLife sold: {self.simulation.stats.sold[-1][0]}\nCar sold: {self.simulation.stats.sold[-1][1]}\nHome sold: {self.simulation.stats.sold[-1][2]}\nPayouts: {round(self.simulation.stats.payouts[-1], 2)}\nActive: {len(self.simulation.company.insurances)}")

    def __close_modal(self, insurancetype: str, insurance_params: List[int | float]) -> None:
        '''
        Closing modal window and making changes.
        '''
        self.simulation.company.change_insurance_params(
            insurancetype=insurancetype, insurance_params=insurance_params)
        self.pop.grab_release()
        self.pop.destroy()

    def __modal(self, insurance: Life | Car | Home) -> None:
        '''
        Creating a popup modal window to configure parameters of the selected insurance.
        '''
        # Creating a popup window
        self.pop: tk.Toplevel = tk.Toplevel(self.window)
        self.pop.geometry("300x200")
        self.pop.grab_set()

        # Setting the parameters of the popup
        self.pop.title(f"Correct params of {insurance.type}")

        # Create a label for duration
        l_duration = tk.Label(self.pop, text="Duration")
        l_duration.grid(row=0, column=0)

        # Create a textbox for duration
        t_duration = tk.Text(self.pop, height=1, width=10)
        t_duration.insert(1.0, f"{insurance.until}")
        t_duration.grid(row=1, column=0)

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
            t_duration.get(1.0, tk.END)), float(t_payout.get(1.0, tk.END)), float(t_franchise.get(1.0, tk.END)), insurance.demand]))

        b_accept.grid(row=4, column=0)

        # Create a button for cancel
        b_cancel = tk.Button(self.pop, text="Cancel", command=self.pop.destroy)
        b_cancel.grid(row=4, column=1)

    def __change(self) -> None:
        '''
        Change expired insurance parameters.
        '''
        try:
            selection = self.l_expired.curselection()[0]                    
            match selection:
                case 0:
                    self.__modal(Life(*self.simulation.company.life_params))  # type: ignore
                case 1:
                    self.__modal(Home(*self.simulation.company.home_params))  # type: ignore
                case 2:
                    self.__modal(Car(*self.simulation.company.car_params))  # type: ignore
        except:
            pass

    def __show_settings_popup(self, path) -> None:
        '''
        Creating a popup modal window to configure parameters of the simulation.
        '''
        config: Dict[str, int | float | List[int | float]
                     ] = json.loads(Path(path).read_text())

        # Creating a popup window
        self.pop: tk.Toplevel = tk.Toplevel(self.window)

        self.pop.grab_set()

        # Setting the parameters of the popup
        self.pop.title("Simulation parameters")

        # Create a label for game duration
        l_game_duration = tk.Label(self.pop, text="Game duration")
        l_game_duration.grid(row=0, column=0)

        # Create a textbox for game duration
        t_game_duration = tk.Text(self.pop, height=1, width=10)
        t_game_duration.insert(1.0, f"{config['until']}")
        t_game_duration.grid(row=1, column=0)

        # Create a label for starting money
        l_startmoney = tk.Label(self.pop, text="Starting money")
        l_startmoney.grid(row=0, column=1)

        # Create a textbox for starting money
        t_startmoney = tk.Text(self.pop, height=1, width=10)
        t_startmoney.insert(1.0, f"{config['startingmoney']}")
        t_startmoney.grid(row=1, column=1)



        # Life insurance params
        #
        #
        # Create a label for life insurance duration
        l_life_duration = tk.Label(self.pop, text="Life insurance duration")
        l_life_duration.grid(row=2, column=0)

        # Create a textbox for life insurance duration
        t_life_duration = tk.Text(self.pop, height=1, width=10)
        t_life_duration.insert(1.0, f"{config['life'][1]}")  # type: ignore
        t_life_duration.grid(row=3, column=0)

        # Create a label for life insurance cost
        l_life_cost = tk.Label(self.pop, text="Life insurance cost")
        l_life_cost.grid(row=4, column=0)

        # Create a textbox for life insurance cost
        t_life_cost = tk.Text(self.pop, height=1, width=10)
        t_life_cost.insert(1.0, f"{config['life'][0]}")  # type: ignore
        t_life_cost.grid(row=5, column=0)

        # Create a label for life insurance payout
        l_life_payout = tk.Label(self.pop, text="Life insurance payout")
        l_life_payout.grid(row=6, column=0)

        # Create a textbox for life insurance payout
        t_life_payout = tk.Text(self.pop, height=1, width=10)
        t_life_payout.insert(1.0, f"{config['life'][2]}")  # type: ignore
        t_life_payout.grid(row=7, column=0)

        # Create a label for life insurance franchise
        l_life_franchise = tk.Label(self.pop, text="Life insurance franchise")
        l_life_franchise.grid(row=8, column=0)

        # Create a textbox for life insurance franchise
        t_life_franchise = tk.Text(self.pop, height=1, width=10)
        t_life_franchise.insert(1.0, f"{config['life'][3]}")  # type: ignore
        t_life_franchise.grid(row=9, column=0)

        # Create a label for life insurance demand
        l_life_demand = tk.Label(self.pop, text="Life insurance demand")
        l_life_demand.grid(row=10, column=0)

        # Create a textbox for life insurance franchise
        t_life_demand = tk.Text(self.pop, height=1, width=10)
        t_life_demand.insert(1.0, f"{config['life'][4]}")  # type: ignore
        t_life_demand.grid(row=11, column=0)



        # Car insurance params
        #
        #
        # Create a label for car insurance duration
        l_car_duration = tk.Label(self.pop, text="Car insurance duration")
        l_car_duration.grid(row=2, column=1)

        # Create a textbox for car insurance duration
        t_car_duration = tk.Text(self.pop, height=1, width=10)
        t_car_duration.insert(1.0, f"{config['car'][1]}")  # type: ignore
        t_car_duration.grid(row=3, column=1)

        # Create a label for car insurance cost
        l_car_cost = tk.Label(self.pop, text="Car insurance cost")
        l_car_cost.grid(row=4, column=1)

        # Create a textbox for car insurance cost
        t_car_cost = tk.Text(self.pop, height=1, width=10)
        t_car_cost.insert(1.0, f"{config['car'][0]}")  # type: ignore
        t_car_cost.grid(row=5, column=1)

        # Create a label for car insurance payout
        l_car_payout = tk.Label(self.pop, text="Car insurance payout")
        l_car_payout.grid(row=6, column=1)

        # Create a textbox for car insurance payout
        t_car_payout = tk.Text(self.pop, height=1, width=10)
        t_car_payout.insert(1.0, f"{config['car'][2]}")  # type: ignore
        t_car_payout.grid(row=7, column=1)

        # Create a label for car insurance franchise
        l_car_franchise = tk.Label(self.pop, text="Car insurance franchise")
        l_car_franchise.grid(row=8, column=1)

        # Create a textbox for car insurance franchise
        t_car_franchise = tk.Text(self.pop, height=1, width=10)
        t_car_franchise.insert(1.0, f"{config['car'][3]}")  # type: ignore
        t_car_franchise.grid(row=9, column=1)

        # Create a label for car insurance demand
        l_car_demand = tk.Label(self.pop, text="Car insurance demand")
        l_car_demand.grid(row=10, column=1)

        # Create a textbox for car insurance franchise
        t_car_demand = tk.Text(self.pop, height=1, width=10)
        t_car_demand.insert(1.0, f"{config['car'][4]}")  # type: ignore
        t_car_demand.grid(row=11, column=1)



        # Home insurance params
        #
        #
        # Create a label for home insurance duration
        l_home_duration = tk.Label(self.pop, text="Home insurance duration")
        l_home_duration.grid(row=2, column=2)

        # Create a textbox for home insurance duration
        t_home_duration = tk.Text(self.pop, height=1, width=10)
        t_home_duration.insert(1.0, f"{config['home'][1]}")  # type: ignore
        t_home_duration.grid(row=3, column=2)

        # Create a label for home insurance cost
        l_home_cost = tk.Label(self.pop, text="Home insurance cost")
        l_home_cost.grid(row=4, column=2)

        # Create a textbox for home insurance cost
        t_home_cost = tk.Text(self.pop, height=1, width=10)
        t_home_cost.insert(1.0, f"{config['home'][0]}")  # type: ignore
        t_home_cost.grid(row=5, column=2)

        # Create a label for home insurance payout
        l_home_payout = tk.Label(self.pop, text="Home insurance payout")
        l_home_payout.grid(row=6, column=2)

        # Create a textbox for home insurance payout
        t_home_payout = tk.Text(self.pop, height=1, width=10)
        t_home_payout.insert(1.0, f"{config['home'][2]}")  # type: ignore
        t_home_payout.grid(row=7, column=2)

        # Create a label for home insurance franchise
        l_home_franchise = tk.Label(self.pop, text="Home insurance franchise")
        l_home_franchise.grid(row=8, column=2)

        # Create a textbox for home insurance franchise
        t_home_franchise = tk.Text(self.pop, height=1, width=10)
        t_home_franchise.insert(1.0, f"{config['home'][3]}")  # type: ignore
        t_home_franchise.grid(row=9, column=2)

        # Create a label for home insurance demand
        l_home_demand = tk.Label(self.pop, text="Home insurance demand")
        l_home_demand.grid(row=10, column=2)

        # Create a textbox for home insurance franchise
        t_home_demand = tk.Text(self.pop, height=1, width=10)
        t_home_demand.insert(1.0, f"{config['home'][4]}")  # type: ignore
        t_home_demand.grid(row=11, column=2)

        # Create a button for accept
        # Using lambda for binding reasons

        def create_dict() -> Dict[str, int | float | List[int | float]] | None:
            try:
                self.pop.grab_release()
                return {
                        "until": int(t_game_duration.get(1.0, tk.END)), 
                        "startingmoney": float(t_startmoney.get(1.0, tk.END)),
                        "life": [int(t_life_cost.get(1.0, tk.END)), int(t_life_duration.get(1.0, tk.END)), int(t_life_payout.get(1.0, tk.END)), int(t_life_franchise.get(1.0, tk.END)), int(t_life_demand.get(1.0, tk.END))],
                        "home": [int(t_home_cost.get(1.0, tk.END)), int(t_home_duration.get(1.0, tk.END)), int(t_home_payout.get(1.0, tk.END)), int(t_home_franchise.get(1.0, tk.END)), int(t_home_demand.get(1.0, tk.END))],
                        "car": [int(t_car_cost.get(1.0, tk.END)), int(t_car_duration.get(1.0, tk.END)), int(t_car_payout.get(1.0, tk.END)), int(t_car_franchise.get(1.0, tk.END)), int(t_car_demand.get(1.0, tk.END))],
                    }
            except:
                tkmb.showerror("Error", "Incorrect input!")
                self.pop.grab_release()
                self.pop.destroy()
                self.__close()

        def accept() -> None:
            Path(path).write_text(json.dumps(create_dict(), indent=2))
            self.simulation.set_params()
            self.simulation.company.set_params()
            self.pop.destroy()

        b_accept = tk.Button(self.pop, text="Accept", command=accept)
        b_accept.grid(row=12, column=2)
            
        b_close = tk.Button(self.pop, text="Close", command=lambda: self.__close())
        b_close.grid(row=12, column=3)

    def __close(self) -> None:
        '''
        For exiting the application.
        '''
        sys.exit()

if __name__ == "__main__":
    app = App()
