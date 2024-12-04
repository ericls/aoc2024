# Just in case

import re
from collections import OrderedDict
from enum import Enum, auto

expr = """
mul(mul(2, 3), mul(4, 5))
"""


class TokenType(Enum):
    MUL = auto()
    HOW = auto()
    WHEN = auto()
    SELECT = auto()
    WHAT = auto()
    FROM = auto()
    WHY = auto()
    WHO = auto()
    WHERE = auto()

    DO = auto()
    DONT = auto()

    NUMBER = auto()
    LPAREN = auto()
    RPAREN = auto()
    COMMA = auto()

    GARBAGE = auto()


FUNC_NAMES = {
    TokenType.MUL,
    TokenType.HOW,
    TokenType.WHEN,
    TokenType.SELECT,
    TokenType.WHAT,
    TokenType.FROM,
    TokenType.WHY,
    TokenType.WHO,
    TokenType.WHERE,
    TokenType.DO,
    TokenType.DONT,
}

FUNC_ARITY = {
    TokenType.MUL: 2,
    TokenType.DO: 0,
    TokenType.DONT: 0,
}

TOKEN_PATTERNS = OrderedDict(
    {
        TokenType.MUL: re.compile(r"mul"),
        TokenType.HOW: re.compile(r"how"),
        TokenType.WHEN: re.compile(r"when"),
        TokenType.SELECT: re.compile(r"select"),
        TokenType.WHAT: re.compile(r"what"),
        TokenType.FROM: re.compile(r"from"),
        TokenType.WHY: re.compile(r"why"),
        TokenType.WHO: re.compile(r"who"),
        TokenType.WHERE: re.compile(r"where"),
        TokenType.DONT: re.compile(r"don't"),
        TokenType.DO: re.compile(r"do"),
        TokenType.NUMBER: re.compile(r"\d+"),
        TokenType.LPAREN: re.compile(r"\("),
        TokenType.RPAREN: re.compile(r"\)"),
        TokenType.COMMA: re.compile(r","),
    }
)


class Token:
    def __init__(self, type_: TokenType, value: str, location: int):
        self.type = type_
        self.value = value

    def __repr__(self):
        return f"Token({self.type}, {repr(self.value)})"


def tokenize(code):
    tokens = []
    pos = 0
    skipped = ""
    while pos < len(code):
        match = None
        for token_type, pattern in TOKEN_PATTERNS.items():
            match = pattern.match(code, pos)
            if match:
                if skipped:
                    tokens.append(Token(TokenType.GARBAGE, skipped, pos))
                    skipped = ""
                tokens.append(Token(token_type, match.group(0), pos))
                pos = match.end()
                break
        if not match:
            skipped += code[pos]
            pos += 1
    return tokens


class ASTNode:
    def __init__(self, token=None):
        self.token = token

    def dump(self) -> str:
        return ""


class ASTNodeModule(ASTNode):
    def __init__(self, token, expressions):
        super().__init__(token)
        self.expressions = expressions

    def __repr__(self):
        return f"ASTNodeModule({self.expressions})"

    def dump(self):
        return [expr.dump() for expr in self.expressions].__str__()


class ASTNodeName(ASTNode):
    def __init__(self, token, name):
        super().__init__(token)
        self.name = name

    def __repr__(self):
        return f"ASTNodeName({self.name})"

    def dump(self):
        return self.name


class ASTNodeConstant(ASTNode):
    def __init__(self, token, value):
        super().__init__(token)
        self.value = value

    def __repr__(self):
        return f"ASTNodeConstant({self.value})"

    def dump(self):
        return str(self.value)


class ASTNodeCall(ASTNode):
    def __init__(self, token, func_name: ASTNodeName, args: list[ASTNode]):
        super().__init__(token)
        self.func_name = func_name
        self.args = args

    def __repr__(self):
        return f"ASTNodeFuncCall({self.func_name}, {self.args})"

    def dump(self):
        return f"{self.func_name.dump()}({', '.join(arg.dump() for arg in self.args)})"


class ASTNodeGarbage(ASTNode):
    def __init__(self, value):
        super().__init__()
        self.value = value

    def __repr__(self):
        return f"ASTNodeGarbage({self.value})"


class Parser:
    def __init__(self, tokens):
        self.tokens = [t for t in tokens]
        self.current = 0

    def advance(self) -> Token:
        self.current += 1
        return self.previous()

    def previous(self) -> Token:
        return self.tokens[self.current - 1]

    def peek(self) -> Token:
        return self.tokens[self.current]

    def is_at_end(self) -> bool:
        return self.current >= len(self.tokens)

    def check(self, *expected_types: TokenType) -> bool:
        if self.is_at_end():
            return False
        return self.peek().type in expected_types

    def consume(self, *expected_types: TokenType) -> Token:
        if self.check(*expected_types):
            return self.advance()
        raise ValueError(f"Expected {expected_types}, got {self.peek().type}")

    def parse(self) -> ASTNodeModule:
        expressions = []
        while not self.is_at_end():
            expr = self.expression()
            if expr:
                expressions.append(expr)
        return ASTNodeModule(None, expressions)

    def expression(self) -> ASTNode | None:
        current = self.current
        if self.check(*FUNC_NAMES):
            try:
                return self.func_call()
            except ValueError:
                self.current = current + 1
        else:
            self.advance()

    # assume no nested calls
    def func_call(self) -> ASTNodeCall:
        func_name = self.consume(*FUNC_NAMES)
        self.consume(TokenType.LPAREN)
        args: list[ASTNode] = []
        while not self.check(TokenType.RPAREN):
            if self.check(TokenType.NUMBER):
                number = self.consume(TokenType.NUMBER)
                args.append(ASTNodeConstant(number, int(number.value)))
            else:
                self.consume(TokenType.COMMA)
        self.consume(TokenType.RPAREN)
        if func_name.type in FUNC_ARITY and len(args) != FUNC_ARITY[func_name.type]:
            raise ValueError(
                f"Function {func_name.value} expects {FUNC_ARITY[func_name.type]} arguments, got {len(args)}"
            )
        return ASTNodeCall(func_name, ASTNodeName(func_name, func_name.value), args)


class VM:
    def __init__(self, ignore_enabled_state=False):
        self.ignore_enabled_state = ignore_enabled_state
        self.value = 0
        self.enabled = True
        self.call_log = []

    def mul(self, a, b):
        if self.enabled or self.ignore_enabled_state:
            self.value += a * b

    def do(self):
        self.enabled = True

    def dont(self):
        self.enabled = False

    def noop(self, *args, **kwargs):
        pass

    def execute(self, ast: ASTNode):
        funcs = {
            "mul": self.mul,
            "do": self.do,
            "don't": self.dont,
        }

        if isinstance(ast, ASTNodeModule):
            return [self.execute(expr) for expr in ast.expressions]
        elif isinstance(ast, ASTNodeCall):
            func = funcs.get(ast.func_name.name, self.noop)
            args = [self.execute(arg) for arg in ast.args]
            if func != self.noop:
                self.call_log.append((ast.func_name.name, args))
            return func(*args)
        elif isinstance(ast, ASTNodeConstant):
            return ast.value
        else:
            raise ValueError(f"Unknown AST node type {ast}")


def run_code_in_vm(code: str, *args, **kwargs) -> VM:
    tokens = tokenize(code)
    parser = Parser(tokens)
    ast = parser.parse()
    vm = VM(*args, **kwargs)
    vm.execute(ast)
    return vm
