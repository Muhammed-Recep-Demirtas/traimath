"""
traimath.advanced
-----------------
Gelişmiş matematiksel işlemler: üs, karekök, faktöriyel, logaritma, üstel.

Standart kütüphane `math` modülü kullanılır; NumPy veya diğer üçüncü taraf
kütüphanelere bağımlılık yoktur.
"""

import math

from traimath.errors import DivisionByZeroError, DomainError, TRAIMathError

Number = int | float


def power(base: Number, exponent: Number) -> Number:
    """
    Taban sayısının üssünü hesaplar.

    Args:
        base (Number): Taban.
        exponent (Number): Üs.

    Returns:
        Number: base ** exponent sonucu.

    Example:
        >>> power(2, 10)
        1024
        >>> power(9, 0.5)
        3.0
    """
    return base ** exponent


def sqrt(x: Number) -> float:
    """
    Bir sayının karekökünü hesaplar.

    Args:
        x (Number): Karekökü alınacak sayı. Negatif olamaz.

    Returns:
        float: √x değeri.

    Raises:
        DomainError: x < 0 olduğunda fırlatılır.

    Example:
        >>> sqrt(25)
        5.0
        >>> sqrt(2)
        1.4142135623730951
    """
    if x < 0:
        raise DomainError("sqrt", x, "Negatif sayıların karekökü reel sayı değildir.")
    return math.sqrt(x)


def factorial(n: int) -> int:
    """
    Negatif olmayan bir tamsayının faktöriyelini hesaplar.

    Args:
        n (int): Faktöriyeli hesaplanacak tamsayı (n >= 0).

    Returns:
        int: n! değeri.

    Raises:
        DomainError: n < 0 veya n bir tamsayı değilse fırlatılır.

    Example:
        >>> factorial(5)
        120
        >>> factorial(0)
        1
    """
    if not isinstance(n, int):
        raise DomainError("factorial", n, "Faktöriyel yalnızca tamsayılar için tanımlıdır.")
    if n < 0:
        raise DomainError("factorial", n, "Negatif sayıların faktöriyeli tanımlı değildir.")
    return math.factorial(n)


def log(x: Number, base: Number = math.e) -> float:
    """
    Verilen tabana göre logaritmayı hesaplar.

    Taban belirtilmezse doğal logaritma (ln) döndürülür.

    Args:
        x (Number): Logaritması alınacak sayı. Sıfırdan büyük olmalı.
        base (Number): Logaritmanın tabanı (varsayılan: e). Sıfırdan büyük
                       ve 1'den farklı olmalı.

    Returns:
        float: log_base(x) değeri.

    Raises:
        DomainError: x <= 0 veya geçersiz taban verildiğinde fırlatılır.
        TRAIMathError: base == 1 olduğunda fırlatılır.

    Example:
        >>> log(math.e)          # ln(e) = 1
        1.0
        >>> log(100, 10)         # log10(100) = 2
        2.0
        >>> log(8, 2)            # log2(8) = 3
        3.0
    """
    if x <= 0:
        raise DomainError("log", x, "Logaritma yalnızca pozitif sayılar için tanımlıdır.")
    if base <= 0:
        raise DomainError("log", base, "Logaritma tabanı pozitif olmalıdır.")
    if base == 1:
        raise TRAIMathError(
            "Logaritma tabanı 1 olamaz (tanımsız).",
            code="INVALID_BASE",
        )
    return math.log(x, base)


def log10(x: Number) -> float:
    """
    10 tabanında logaritmayı hesaplar.

    Args:
        x (Number): Logaritması alınacak sayı. Sıfırdan büyük olmalı.

    Returns:
        float: log10(x) değeri.

    Raises:
        DomainError: x <= 0 olduğunda fırlatılır.

    Example:
        >>> log10(1000)
        3.0
    """
    if x <= 0:
        raise DomainError("log10", x, "Logaritma yalnızca pozitif sayılar için tanımlıdır.")
    return math.log10(x)


def log2(x: Number) -> float:
    """
    2 tabanında logaritmayı hesaplar.

    Args:
        x (Number): Logaritması alınacak sayı. Sıfırdan büyük olmalı.

    Returns:
        float: log2(x) değeri.

    Raises:
        DomainError: x <= 0 olduğunda fırlatılır.

    Example:
        >>> log2(1024)
        10.0
    """
    if x <= 0:
        raise DomainError("log2", x, "Logaritma yalnızca pozitif sayılar için tanımlıdır.")
    return math.log2(x)


def exp(x: Number) -> float:
    """
    e^x (üstel fonksiyon) değerini hesaplar.

    Args:
        x (Number): Üs değeri.

    Returns:
        float: e^x sonucu.

    Example:
        >>> round(exp(1), 10)
        2.718281828
        >>> exp(0)
        1.0
    """
    return math.exp(x)


def cbrt(x: Number) -> float:
    """
    Bir sayının küp kökünü hesaplar.

    Negatif sayılarda da çalışır (gerçek küp kök).

    Args:
        x (Number): Küp kökü alınacak sayı.

    Returns:
        float: x^(1/3) değeri.

    Example:
        >>> cbrt(27)
        3.0
        >>> cbrt(-8)
        -2.0
    """
    if x < 0:
        return -((-x) ** (1 / 3))
    return x ** (1 / 3)


def gcd(a: int, b: int) -> int:
    """
    İki tamsayının en büyük ortak bölenini (EBOB) hesaplar.

    Args:
        a (int): Birinci tamsayı.
        b (int): İkinci tamsayı.

    Returns:
        int: EBOB(a, b).

    Example:
        >>> gcd(48, 18)
        6
        >>> gcd(100, 75)
        25
    """
    return math.gcd(a, b)


def lcm(a: int, b: int) -> int:
    """
    İki tamsayının en küçük ortak katını (EKOK) hesaplar.

    Args:
        a (int): Birinci tamsayı.
        b (int): İkinci tamsayı.

    Returns:
        int: EKOK(a, b).

    Raises:
        DivisionByZeroError: a veya b == 0 olduğunda fırlatılır.

    Example:
        >>> lcm(4, 6)
        12
        >>> lcm(12, 15)
        60
    """
    if a == 0 or b == 0:
        raise DivisionByZeroError("EKOK hesabında sıfır kullanılamaz.")
    return abs(a * b) // math.gcd(a, b)