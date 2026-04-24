"""
traimath.parser
---------------
Güvenli matematiksel ifade ayrıştırıcı.

eval() KULLANILMAZ. Bunun yerine iki aşamalı bir yaklaşım benimsenir:

1. **Lexer (Tokenizer):** Ham string'i anlamlı token'lara böler.
   Token türleri: NUMBER, OPERATOR, LPAREN, RPAREN, FUNCTION

2. **Shunting-Yard Algoritması (Dijkstra):** Token listesini
   Reverse Polish Notation'a (RPN / postfix) dönüştürür.
   Operatör önceliği ve sol/sağ ilişkilendirme burada çözülür.

3. **RPN Değerlendirici:** Postfix ifadesini bir yığın (stack)
   kullanarak hesaplar.

Desteklenen sözdizimi:
    - Tam sayı ve ondalıklı sayı sabitleri  (42, 3.14, .5)
    - Operatörler: +, -, *, /, %, ^ (üs)
    - Unary minus: -3, -(2+1)
    - Parantezler: (2+3)*4
    - Fonksiyonlar: sin, cos, tan, sqrt, log, log2, log10, exp,
                    abs, floor, ceil, round
    - Sabitler: pi, e
"""

from __future__ import annotations

import math
import re
from dataclasses import dataclass
from enum import Enum, auto
from typing import Callable

from traimath.errors import DivisionByZeroError, InvalidExpressionError

# ── Token tanımları ───────────────────────────────────────────────────────────


class TokenType(Enum):
    NUMBER = auto()
    OPERATOR = auto()
    LPAREN = auto()
    RPAREN = auto()
    FUNCTION = auto()
    CONSTANT = auto()


@dataclass(frozen=True)
class Token:
    """Bir lexer token'ını temsil eder."""

    type: TokenType
    value: str


# ── Operatör tablosu ──────────────────────────────────────────────────────────

# (öncelik, sağ_ilişkilendirme, işlev)
_OPERATORS: dict[str, tuple[int, bool, Callable[[float, float], float]]] = {
    "+": (1, False, lambda a, b: a + b),
    "-": (1, False, lambda a, b: a - b),
    "*": (2, False, lambda a, b: a * b),
    "/": (2, False, lambda a, b: (_ for _ in ()).throw(DivisionByZeroError()) if b == 0 else a / b),
    "%": (2, False, lambda a, b: (_ for _ in ()).throw(DivisionByZeroError()) if b == 0 else a % b),
    "^": (3, True,  lambda a, b: a ** b),
}

# ── Desteklenen tek argümanlı fonksiyonlar ────────────────────────────────────

_FUNCTIONS: dict[str, Callable[[float], float]] = {
    "sin":   math.sin,
    "cos":   math.cos,
    "tan":   math.tan,
    "asin":  math.asin,
    "acos":  math.acos,
    "atan":  math.atan,
    "sinh":  math.sinh,
    "cosh":  math.cosh,
    "tanh":  math.tanh,
    "sqrt":  math.sqrt,
    "log":   math.log,       # doğal logaritma
    "log2":  math.log2,
    "log10": math.log10,
    "exp":   math.exp,
    "abs":   abs,
    "floor": math.floor,
    "ceil":  math.ceil,
    "round": round,
}

# ── Desteklenen sabitler ──────────────────────────────────────────────────────

_CONSTANTS: dict[str, float] = {
    "pi":  math.pi,
    "e":   math.e,
    "tau": math.tau,
    "inf": math.inf,
}

# ── Lexer ─────────────────────────────────────────────────────────────────────

# Token sıralaması önemli: daha uzun eşleşmeler önce gelmeli.
_TOKEN_PATTERN = re.compile(
    r"""
    (?P<NUMBER>   \d+\.?\d* | \.\d+ )      # sayı: 42, 3.14, .5
    | (?P<FUNCTION> [a-zA-Z_]\w* )          # fonksiyon/sabit adı
    | (?P<OPERATOR> [+\-*/%^] )             # operatör
    | (?P<LPAREN>   \( )                    # sol parantez
    | (?P<RPAREN>   \) )                    # sağ parantez
    | (?P<SKIP>     \s+ )                   # boşluk → atla
    | (?P<MISMATCH> . )                     # bilinmeyen karakter → hata
    """,
    re.VERBOSE,
)


def _tokenize(expression: str) -> list[Token]:
    """
    İfade string'ini Token listesine dönüştürür.

    Args:
        expression (str): Matematiksel ifade.

    Returns:
        list[Token]: Token listesi.

    Raises:
        InvalidExpressionError: Tanınmayan karakter bulunursa.
    """
    tokens: list[Token] = []

    for match in _TOKEN_PATTERN.finditer(expression):
        kind = match.lastgroup
        value = match.group()

        if kind == "SKIP":
            continue
        elif kind == "MISMATCH":
            raise InvalidExpressionError(
                expression,
                f"Tanınmayan karakter: {value!r} (konum {match.start()})",
            )
        elif kind == "NUMBER":
            tokens.append(Token(TokenType.NUMBER, value))
        elif kind == "FUNCTION":
            if value in _FUNCTIONS:
                tokens.append(Token(TokenType.FUNCTION, value))
            elif value in _CONSTANTS:
                tokens.append(Token(TokenType.CONSTANT, value))
            else:
                raise InvalidExpressionError(
                    expression,
                    f"Bilinmeyen fonksiyon veya sabit: {value!r}",
                )
        elif kind == "OPERATOR":
            tokens.append(Token(TokenType.OPERATOR, value))
        elif kind == "LPAREN":
            tokens.append(Token(TokenType.LPAREN, "("))
        elif kind == "RPAREN":
            tokens.append(Token(TokenType.RPAREN, ")"))

    return tokens


def _handle_unary_minus(tokens: list[Token]) -> list[Token]:
    """
    Unary minus (negatif işaret) token'larını işler.

    Unary minus koşulları:
      - İfadenin başındaysa
      - Bir operatörün ardındansa
      - Sol parantezin ardındansa

    Bu durumlarda '-' operatörünü '~' (unary eksi sentinel) ile değiştirir
    ve üs tablosuna ~:(4, True, lambda a: -a) olarak eklenir.

    Args:
        tokens (list[Token]): Ham token listesi.

    Returns:
        list[Token]: Unary minus dönüştürülmüş token listesi.
    """
    result: list[Token] = []
    for i, tok in enumerate(tokens):
        if tok.type == TokenType.OPERATOR and tok.value == "-":
            # Önceki token yoksa ya da önceki token operatör/sol parantezse → unary
            prev = result[-1] if result else None
            is_unary = (
                prev is None
                or prev.type == TokenType.OPERATOR
                or prev.type == TokenType.LPAREN
            )
            if is_unary:
                result.append(Token(TokenType.OPERATOR, "~"))
                continue
        result.append(tok)
    return result


# Unary minus için operatör tablosuna özel girdi ekle
_UNARY_OPERATORS: dict[str, tuple[int, bool, Callable]] = {
    "~": (4, True, lambda a: -a),  # unary minus, yüksek öncelik
}


# ── Shunting-Yard → RPN ───────────────────────────────────────────────────────


def _to_rpn(tokens: list[Token], expression: str) -> list[Token]:
    """
    Shunting-Yard algoritmasıyla token listesini RPN sırasına dönüştürür.

    Args:
        tokens (list[Token]): Unary dönüşümü yapılmış token listesi.
        expression (str): Hata mesajları için orijinal ifade.

    Returns:
        list[Token]: RPN sırasındaki token listesi.

    Raises:
        InvalidExpressionError: Parantez dengesizliği veya başka sözdizim
                                hatası bulunursa.
    """
    output: list[Token] = []
    op_stack: list[Token] = []

    for tok in tokens:

        if tok.type in (TokenType.NUMBER, TokenType.CONSTANT):
            output.append(tok)

        elif tok.type == TokenType.FUNCTION:
            op_stack.append(tok)

        elif tok.type == TokenType.OPERATOR:
            o1 = tok.value
            while op_stack:
                top = op_stack[-1]
                if top.type == TokenType.LPAREN:
                    break
                if top.type == TokenType.FUNCTION:
                    output.append(op_stack.pop())
                    continue
                if top.type == TokenType.OPERATOR:
                    o2 = top.value
                    # Unary operatörleri bul
                    p1 = _UNARY_OPERATORS[o1][0] if o1 in _UNARY_OPERATORS else _OPERATORS[o1][0]
                    ra1 = _UNARY_OPERATORS[o1][1] if o1 in _UNARY_OPERATORS else _OPERATORS[o1][1]
                    p2 = _UNARY_OPERATORS[o2][0] if o2 in _UNARY_OPERATORS else _OPERATORS[o2][0]

                    if (p2 > p1) or (p2 == p1 and not ra1):
                        output.append(op_stack.pop())
                    else:
                        break
                else:
                    break
            op_stack.append(tok)

        elif tok.type == TokenType.LPAREN:
            op_stack.append(tok)

        elif tok.type == TokenType.RPAREN:
            # Sol paranteze kadar yığını boşalt
            matched = False
            while op_stack:
                top = op_stack.pop()
                if top.type == TokenType.LPAREN:
                    matched = True
                    break
                output.append(top)
            if not matched:
                raise InvalidExpressionError(expression, "Eşleşmeyen sağ parantez ')'.")
            # Parantezin ardında fonksiyon varsa çıkart
            if op_stack and op_stack[-1].type == TokenType.FUNCTION:
                output.append(op_stack.pop())

    # Kalan operatörleri çıkart
    while op_stack:
        top = op_stack.pop()
        if top.type == TokenType.LPAREN:
            raise InvalidExpressionError(expression, "Eşleşmeyen sol parantez '('.")
        output.append(top)

    return output


# ── RPN Değerlendirici ────────────────────────────────────────────────────────


def _evaluate_rpn(rpn_tokens: list[Token], expression: str) -> float:
    """
    RPN token listesini yığın tabanlı algoritmayla değerlendirir.

    Args:
        rpn_tokens (list[Token]): RPN sırasındaki token listesi.
        expression (str): Hata mesajları için orijinal ifade.

    Returns:
        float: Hesaplama sonucu.

    Raises:
        InvalidExpressionError: Operand sayısı hatalıysa.
        DivisionByZeroError: Sıfıra bölme yapılırsa.
    """
    stack: list[float] = []

    for tok in rpn_tokens:

        if tok.type == TokenType.NUMBER:
            stack.append(float(tok.value))

        elif tok.type == TokenType.CONSTANT:
            stack.append(_CONSTANTS[tok.value])

        elif tok.type == TokenType.FUNCTION:
            if not stack:
                raise InvalidExpressionError(expression, f"'{tok.value}' için argüman eksik.")
            arg = stack.pop()
            try:
                result = _FUNCTIONS[tok.value](arg)
            except (ValueError, ZeroDivisionError) as exc:
                raise InvalidExpressionError(
                    expression,
                    f"'{tok.value}({arg})' hesaplanamadı: {exc}",
                ) from exc
            stack.append(result)

        elif tok.type == TokenType.OPERATOR:
            op = tok.value

            # Unary operatör
            if op in _UNARY_OPERATORS:
                if not stack:
                    raise InvalidExpressionError(expression, "Unary operatör için operand eksik.")
                a = stack.pop()
                stack.append(_UNARY_OPERATORS[op][2](a))

            # Binary operatör
            else:
                if len(stack) < 2:
                    raise InvalidExpressionError(
                        expression,
                        f"'{op}' operatörü için yeterli operand yok.",
                    )
                b, a = stack.pop(), stack.pop()
                if op in ("/", "%") and b == 0:
                    raise DivisionByZeroError()
                try:
                    stack.append(_OPERATORS[op][2](a, b))
                except ZeroDivisionError:
                    raise DivisionByZeroError()

    if len(stack) != 1:
        raise InvalidExpressionError(expression, "İfade değerlendirilemedi (operand fazlası).")

    return stack[0]


# ── Genel API ─────────────────────────────────────────────────────────────────


def parse(expression: str) -> float:
    """
    Matematiksel ifade string'ini güvenli biçimde hesaplar.

    eval() kullanılmaz. Shunting-Yard algoritması ve RPN değerlendirici
    kullanılarak hesaplama yapılır.

    Desteklenen sözdizimi:
        - Sayılar: 42, 3.14, .5
        - Operatörler: +, -, *, /, %, ^ (üs)
        - Unary minus: -3, -(2+1)
        - Parantezler: (2+3)*4
        - Fonksiyonlar: sin, cos, tan, sqrt, log, log2, log10,
                        exp, abs, floor, ceil, round
        - Sabitler: pi, e, tau, inf

    Args:
        expression (str): Hesaplanacak matematiksel ifade.

    Returns:
        float: Hesaplama sonucu.

    Raises:
        InvalidExpressionError: İfade geçersiz ya da ayrıştırılamaz ise.
        DivisionByZeroError: İfade sıfıra bölme içeriyorsa.

    Example:
        >>> parse("2 + 3 * 5")
        17.0
        >>> parse("(2 + 3) * 5")
        25.0
        >>> parse("sqrt(16) + 2^3")
        12.0
        >>> parse("sin(pi / 2)")
        1.0
        >>> parse("-3 * (4 + 2)")
        -18.0
    """
    if not isinstance(expression, str):
        raise InvalidExpressionError(str(expression), "İfade bir string olmalıdır.")

    stripped = expression.strip()
    if not stripped:
        raise InvalidExpressionError(expression, "Boş ifade değerlendirilemez.")

    tokens = _tokenize(stripped)
    tokens = _handle_unary_minus(tokens)
    rpn = _to_rpn(tokens, stripped)
    return _evaluate_rpn(rpn, stripped)


def parse_safe(expression: str, default: float = float("nan")) -> float:
    """
    parse() fonksiyonunu çağırır; hata oluşursa ``default`` değerini döndürür.

    Hata iletmeye gerek olmayan uygulamalar için kolaylık sarmalayıcısı.

    Args:
        expression (str): Hesaplanacak ifade.
        default (float): Hata durumunda döndürülecek değer (varsayılan: NaN).

    Returns:
        float: Hesaplama sonucu veya default değeri.

    Example:
        >>> parse_safe("2 + 2")
        4.0
        >>> import math; math.isnan(parse_safe("1 / 0 +"))
        True
    """
    try:
        return parse(expression)
    except Exception:
        return default