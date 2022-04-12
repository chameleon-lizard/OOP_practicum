from typing import Dict, List, Tuple
from stats import Statistics
from company import Company
from pathlib import Path

import json


class Simulation:
    '''
    Class for simulation.
    '''

    def __init__(self, path: str = "config.json") -> None:
        '''
        Simulation class constructor.
        '''
        config: Dict[str, int | float | List[int | float]
                     ] = json.loads(Path(path).read_text())
        self.until: int = config["until"]  # type: ignore
        self.time: int = 0
        self.company: Company = Company(
            path, config["startingmoney"])  # type: ignore
        self.stats: Statistics = Statistics(
            config["startingmoney"])  # type: ignore

    def __parse_output(self, text: str) -> Tuple[int, int, int]:
        '''
        Helper function to parse the text for life, car and home insurance sales info.
        '''
        life, car, home = text.split(";")[1:]
        life_amount = int(life[:life.index("life")])
        car_amount = int(car[:car.index("car")])
        home_amount = int(home[:home.index("home")])

        return (life_amount, car_amount, home_amount)

    def step(self) -> Tuple[str, bool]:
        '''
        Progress the simulation for one step.
        '''
        change: float = 0

        # Paying taxes
        text, c = self.company.pay_taxes()
        change += c

        # Stopping insurances
        self.company.stop_insurances(self.stats.step + 1)

        # Selling new insurances
        for i in ["life", "car", "home"]:
            text_, c = self.company.sell_insurance(i)
            text += "; " + text_
            change += c

        self.stats.add_step(self.__parse_output(text), change)

        if self.stats.step == self.until:
            return text, False
        else:
            return text, True
