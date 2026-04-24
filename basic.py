"""
traimath.basic
--------------
Temel aritmetik işlemler: toplama, çıkarma, çarpma, bölme.

Tüm fonksiyonlar tam sayı veya ondalıklı sayı alıp döndürür.
Sıfıra bölme durumunda DivisionByZeroError fırlatılır.
"""

from traimath.errors import DivisionByZeroError

Number = int | float


def add(a: Number, b: Number) -> Number:
    """
    İki sayıyı toplar.

    Args:
        a (Number): İlk sayı.
        b (Number): İkinci sayı.

    Returns:
        Number: a + b sonucu.

    Example:
        >>> add(3, 4)
        7
        >>> add(1.5, 2.5)
        4.0
    """
    return a + b


def subtract(a: Number, b: Number) -> Number:
    """
    Birinci sayıdan ikinci sayıyı çıkarır.

    Args:
        a (Number): Azalan (minuend).
        b (Number): Çıkan (subtrahend).

    Returns:
        Number: a - b sonucu.

    Example:
        >>> subtract(10, 4)
        6
        >>> subtract(0.5, 1.5)
        -1.0
    """
    return a - b


def multiply(a: Number, b: Number) -> Number:
    """
    İki sayıyı çarpar.

    Args:
        a (Number): İlk çarpan.
        b (Number): İkinci çarpan.

    Returns:
        Number: a * b sonucu.

    Example:
        >>> multiply(3, 7)
        21
        >>> multiply(-2, 4.5)
        -9.0
    """
    return a * b


def divide(a: Number, b: Number) -> float:
    """
    Birinci sayıyı ikinci sayıya böler.

    Args:
        a (Number): Bölünen (dividend).
        b (Number): Bölen (divisor). Sıfır olamaz.

    Returns:
        float: a / b sonucu.

    Raises:
        DivisionByZeroError: b == 0 olduğunda fırlatılır.

    Example:
        >>> divide(10, 4)
        2.5
        >>> divide(7, 0)
        Traceback (most recent call last):
            ...
        DivisionByZeroError: [DIVISION_BY_ZERO] Sıfıra bölme işlemi gerçekleştirilemez.
    """
    if b == 0:
        raise DivisionByZeroError()
    return a / b


def modulo(a: Number, b: Number) -> Number:
    """
    Birinci sayının ikinci sayıya bölümünden kalanı döndürür.

    Args:
        a (Number): Bölünen.
        b (Number): Bölen. Sıfır olamaz.

    Returns:
        Number: a % b sonucu.

    Raises:
        DivisionByZeroError: b == 0 olduğunda fırlatılır.

    Example:
        >>> modulo(10, 3)
        1
        >>> modulo(7.5, 2)
        1.5
    """
    if b == 0:
        raise DivisionByZeroError()
    return a % b


def floor_divide(a: Number, b: Number) -> int:
    """
    Tamsayı bölümü (floor division) döndürür.

    Args:
        a (Number): Bölünen.
        b (Number): Bölen. Sıfır olamaz.

    Returns:
        int: a // b sonucu.

    Raises:
        DivisionByZeroError: b == 0 olduğunda fırlatılır.

    Example:
        >>> floor_divide(10, 3)
        3
        >>> floor_divide(-7, 2)
        -4
    """
    if b == 0:
        raise DivisionByZeroError()
    return int(a // b)


def absolute(a: Number) -> Number:
    """
    Bir sayının mutlak değerini döndürür.

    Args:
        a (Number): Girdi sayısı.

    Returns:
        Number: |a| değeri.

    Example:
        >>> absolute(-5)
        5
        >>> absolute(3.14)
        3.14
    """
    return abs(a)