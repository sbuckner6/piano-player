from random import randint, random


class Oscillator:

    UP = 0
    DOWN = 1

    def __init__(self):
        self.direction = self.UP if randint(0, 1) == 0 else self.DOWN

    def update(self, tick):
        pass


class BasicUpDownOscillator(Oscillator):

    def __init__(self, length):
        self.length = length
        super().__init__()

    def update(self, tick):
        if tick % self.length == 0:
            self.direction = not self.direction


class RandomOscillator(Oscillator):

    def __init__(self, chance):
        self.chance = chance
        super().__init__()

    def update(self, tick):
        if random() < self.chance:
            self.direction = not self.direction


class FibonacciOscillator(Oscillator):

    def __init__(self, max=0):
        self.n0 = 0
        self.n1 = 1
        self.i = 0
        self.max = max
        self.swaps = 0
        super().__init__()

    def update(self, tick):
        self.i += 1
        if self.i == self.n1:
            temp = self.n0 + self.n1
            self.n0 = self.n1
            self.n1 = temp
            self.i = 0
            self.swaps += 1
            if self.max != 0 and self.swaps == self.max:
                self.swaps = 0
                self.n0 = 0
                self.n1 = 1
            self.direction = not self.direction


class FibonacciSquaredOscillator(Oscillator):

    def __init__(self, max):
        self.n0 = 0
        self.n1 = 1
        self.i = 0
        self.max = max
        self.swaps = 0
        self.osc = FibonacciOscillator(1)
        super().__init__()
        self.direction = self.osc.direction

    def update(self, tick):
        self.i += 1
        if self.i == self.n1:
            temp = self.n0 + self.n1
            self.n0 = self.n1
            self.n1 = temp
            self.osc.max = self.n1
            self.i = 0
            self.swaps += 1
            if self.max != 0 and self.swaps == self.max:
                self.swaps = 0
                self.n0 = 0
                self.n1 = 1
            self.direction = self.osc.direction