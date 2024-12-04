from lib.input import get_input
from lib.vm import run_code_in_vm


def test_vm():
    code = get_input()
    assert run_code_in_vm(code).value == 82733683
