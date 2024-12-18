from typing import ClassVar


class Machine:
    a: int
    b: int
    c: int
    program: list[int]
    output: list[int]

    use_combo: ClassVar = {
        0: True,
        1: False,
        2: True,
        3: False,
        4: False,  # ignored
        5: True,
        6: True,
        7: True,
    }
    ops: ClassVar = {
        0: "adv",
        1: "bxl",
        2: "bst",
        3: "jnz",
        4: "bxc",
        5: "out",
        6: "bdv",
        7: "cdv",
    }

    def __init__(self, a, b, c, program) -> None:
        self.a = a
        self.b = b
        self.c = c
        self.program = program
        self.count = 0
        self.output = []

    def combo_operand(self, operand):
        if 0 <= operand <= 3:
            return operand
        elif operand == 4:
            return self.a
        elif operand == 5:
            return self.b
        elif operand == 6:
            return self.c
        else:
            raise ValueError("wrong operand")

    def run(self):
        while self.count < len(self.program):
            op = self.program[self.count]
            operand = self.program[self.count + 1]
            if self.use_combo[op]:
                operand = self.combo_operand(operand)
            getattr(self, self.ops[op])(operand)
            if op != 3:
                self.count += 2
        return self.output

    def adv(self, value):
        self.a >>= value

    def bxl(self, value):
        self.b ^= value

    def bst(self, value):
        self.b = value % 8

    def jnz(self, value):
        if self.a == 0:
            self.count += 2
            return
        self.count = value

    def bxc(self, _):
        self.b ^= self.c

    def out(self, value):
        self.output.append(value % 8)

    def bdv(self, value):
        self.b = self.a >> value

    def cdv(self, value):
        self.c = self.a >> value

    def next(self):
        while not self.output:
            op = self.program[self.count]
            operand = self.program[self.count + 1]
            if self.use_combo[op]:
                operand = self.combo_operand(operand)
            getattr(self, self.ops[op])(operand)
            if op != 3:
                self.count += 2
        return self.output[0]


# 2,4,1,5,7,5,4,5,0,3,1,6,5,5,3,0

# b = a % 8
# b ^= 5
# c = a >> b
# b ^= c
# a >>= 3
# b ^= 6
# output(b % 8)
# repeat


def run(input_a):
    a = input_a
    b = 0
    c = 0

    if a == 0:
        yield 0

    while a != 0:
        b = a % 8
        b ^= 5
        c = a >> b
        b ^= c
        a >>= 3
        b ^= 6
        yield b % 8


# a = ...XXXYYYZZZ
# b = ZZZ
# b = ZZZ ^ 101
# c = ...XXXYYYZZZ >> (ZZZ ^ 101)
# b = (ZZZ ^ 101) ^ (...XXXYYYZZZ >> (ZZZ ^ 101))
# a = ...XXXYYY
# b = (ZZZ ^ 101) ^ (...XXXYYYZZZ >> (ZZZ ^ 101)) ^ 110 = (ZZZ ^ 010) ^ (...XXXYYYZZZ >> (ZZZ ^ 101))
# yield b % 8

# max shift: 7, max num of trailing bits affecting result: 7 + 3 = 10

# 000 => 011 ^ XXY
# 001 => 010 ^ XYY
# 010 => 001 ^ WXX
# 011 => 000 ^ XXX
# 100 => 111 ^ Y10 => (!Y)01
# 101 => 110 ^ 101 = 011 = 3
# 111 => 100 ^ YYY

# ZZZ = 000 => 010 ^ XXY
# b = 000
# b = 101
# c = ...XXXY
# b = 101 ^ ...XXXY
# a = ...XXXYYY
# b = 101 ^ ...XXXY ^ 110 = 011 ^ ...XXY

# ZZZ = 001
# b = 001
# b = 100
# c = ...XXXYY
# b = 100 ^ ...XXXYY
# a = ...XXXYYY
# b = 100 ^ ...XXXYY ^ 110 = 010 ^ ...XYY

# ZZZ = 010
# b = 010
# b = 111
# c = ...WXX
# b = 111 ^ ...WXX
# b = 111 ^ ...WXX ^ 110 = 001 ^ WXX
