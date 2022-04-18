import random
import json

from pathlib import Path
from typing import Dict, List, Tuple
from insurances import Car, Home, Life


class Company:
    '''
    Class for company.
    '''

    def __init__(self, money: float, path: str = "config.json",) -> None:
        '''
        Constructor for company class.
        '''
        # Insurances that are currently active
        self.insurances: List[Life | Car | Home] = []
        # The balance of the company
        self.money: float = money

        # Parsed JSON
        insurance_params: Dict[str, int | float | List[int | float]] = json.loads(Path(path).read_text())
        # Life insurance parameters
        self.life_params: List[int | float] = insurance_params["life"] # type: ignore
        # Home insurance parameters
        self.home_params: List[int | float] = insurance_params["home"] # type: ignore
        # Car insurance parameters
        self.car_params: List[int | float] = insurance_params["car"] # type: ignore

    def set_params(self, path: str = "config.json") -> None: 
        '''
        Set params from json.
        '''
        # Parsed JSON
        insurance_params: Dict[str, int | float | List[int | float]] = json.loads(Path(path).read_text())
        # Life insurance parameters
        self.life_params: List[int | float] = insurance_params["life"] # type: ignore
        # Home insurance parameters
        self.home_params: List[int | float] = insurance_params["home"] # type: ignore
        # Car insurance parameters
        self.car_params: List[int | float] = insurance_params["car"] # type: ignore

        self.sell_insurance("life")
        self.sell_insurance("home")
        self.sell_insurance("car")

    def __sell(self, insurance: Life | Car | Home) -> Tuple[str, float]:
        '''
        Sell an insurance by object.
        '''
        # Change on current phase of the step
        change: float = 0
        # Amount of insurances sold on this phase
        amount = random.randint(0, 5) + int(insurance.demand *
                                            (insurance.cost * insurance.until) // insurance.payout)
        for _ in range(amount):
            change += insurance.cost
            self.money += insurance.cost
            self.insurances.append(insurance)

        return (f"{amount} {insurance.type} insurances sold for {change}", change)

    def sell_insurance(self, insurancetype: str) -> Tuple[str, float]:
        '''
        Sell an insurance by type.
        '''
        match insurancetype:
            case "life":
                return self.__sell(Life(*self.life_params))  # type: ignore
            case "car":
                return self.__sell(Car(*self.car_params))  # type: ignore
            case "home":
                return self.__sell(Home(*self.home_params))  # type: ignore

        return ("", 0)

    def change_insurance_params(self, insurancetype: str, insurance_params: List[int | float]) -> None:
        '''
        Change insurance params.
        '''
        match insurancetype:
            case "life":
                self.life_params = insurance_params
            case "car":
                self.car_params = insurance_params
            case "home":
                self.home_params = insurance_params

    def stop_insurances(self, step: int) -> None:
        '''
        Stop insurance from.
        '''
        for i in self.insurances:
            if step == i.until:
                self.insurances.remove(i)

    def payout(self) -> Tuple[str, float]:
        '''
        Calculate the payout.
        '''
        # The payout for those fortunate to buy the insurance
        payout: float = sum(i.payout * random.randint(1, 100) /
                            100 for i in self.insurances if random.randint(0, 5) <= 2)
        self.money -= payout

        return (f"Payout is {round(payout, 2)}", -1 * payout)

    def pay_taxes(self) -> Tuple[str, float]:
        '''
        Pay the taxes.
        '''
        # Amount of taxes to pay
        taxes: float = self.money * 0.09
        self.money -= taxes

        return (f"Taxes are {round(taxes, 2)}", -1 * taxes)
