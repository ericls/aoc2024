import re
from days.day17.day17lib import Machine
from lib.input import get_input

def sol():
    input = get_input()
    digits = map(int, re.findall(r"\d+", input))
    a, b, c, *program = digits
    machine = Machine(a, b, c, program)
    output = machine.run()
    return ",".join(str(i) for i in output)


print(sol())