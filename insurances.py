class Life:
    def __init__(self, cost: float, until: int, payout: float, franchise: float, demand: float) -> None:
        self.type: str = "life"
        self.cost: float = cost
        self.until: int = until
        self.payout: float = payout
        self.franchise: float = franchise
        self.demand: float = demand

    def __str__(self):
        return f"{self.type} insurance, {self.cost}, {self.until}, {self.payout}, {self.franchise}"

class Car:
    def __init__(self, cost: float, until: int, payout: float, franchise: float, demand: float) -> None:
        self.type: str = "car"
        self.cost: float = cost
        self.until: int = until
        self.payout: float = payout
        self.franchise: float = franchise
        self.demand: float = demand

    def __str__(self):
        return f"{self.type} insurance, {self.cost}, {self.until}, {self.payout}, {self.franchise}"


class Home:
    def __init__(self, cost: float, until: int, payout: float, franchise: float, demand: float) -> None:
        self.type: str = "home"
        self.cost: float = cost
        self.until: int = until
        self.payout: float = payout
        self.franchise: float = franchise
        self.demand: float = demand

    def __str__(self):
        return f"{self.type} insurance, {self.cost}, {self.until}, {self.payout}, {self.franchise}"

        