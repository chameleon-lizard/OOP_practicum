from typing import List, Tuple


class Statistics:
    '''
    Class for counting stats of the experiment.
    '''

    def __init__(self, startingmoney: float) -> None:
        '''
        Constructor for the class.
        '''
        # The step number
        self.step: int = 0
        # Tuple containing step and balance
        self.money: List[Tuple[int, float]] = [(self.step, startingmoney)]
        # Tuple containing how much insurances was sold
        self.sold: List[Tuple[int, int, int]] = [(0, 0, 0)]
        self.payouts: List[float] = [0]

    def __tuple_sum(self, fst: Tuple[int, int, int], snd: Tuple[int, int, int]) -> Tuple[int, int, int]:
        '''
        A helper function to sum tuples.
        '''
        return (fst[0] + snd[0], fst[1] + snd[1], fst[2] + snd[2])

    def add_step(self, sold: Tuple[int, int, int], change: float, payout: float) -> None:
        '''
        Add a step to the statistics class fields.
        '''
        self.step += 1
        self.money.append((self.step, self.money[-1][1] + change))
        self.sold.append(self.__tuple_sum(self.sold[-1], sold))
        self.payouts.append(self.payouts[-1] - payout)
