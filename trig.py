"""
traimath.trig
-------------
Trigonometrik fonksiyonlar ve açı dönüşüm yardımcıları.

Standart `math` modülü kullanılır. Tüm fonksiyonlar varsayılan olarak
radyan cinsinden açı kabul eder. `_deg` son ekli sürümler derece kabul eder.
"""

import math

Number = int | float

# ── Dönüşüm yardımcıları ─────────────────────────────────────────────────────


def to_radians(degrees: Number) -> float:
    """
    Dereceyi radyana dönüştürür.

    Args:
        degrees (Number): Derece cinsinden açı.

    Returns:
        float: Radyan cinsinden açı.

    Example:
        >>> to_radians(180)
        3.141592653589793
        >>> to_radians(90)
        1.5707963267948966
    """
    return math.radians(degrees)


def to_degrees(radians: Number) -> float:
    """
    Radyanı dereceye dönüştürür.

    Args:
        radians (Number): Radyan cinsinden açı.

    Returns:
        float: Derece cinsinden açı.

    Example:
        >>> to_degrees(math.pi)
        180.0
        >>> round(to_degrees(math.pi / 2), 10)
        90.0
    """
    return math.degrees(radians)


# ── Temel trigonometrik fonksiyonlar (radyan) ─────────────────────────────────


def sin(angle: Number) -> float:
    """
    Açının sinüs değerini hesaplar (radyan).

    Args:
        angle (Number): Radyan cinsinden açı.

    Returns:
        float: sin(angle) değeri [-1, 1] aralığında.

    Example:
        >>> round(sin(math.pi / 2), 10)
        1.0
        >>> round(sin(0), 10)
        0.0
    """
    return math.sin(angle)


def cos(angle: Number) -> float:
    """
    Açının kosinüs değerini hesaplar (radyan).

    Args:
        angle (Number): Radyan cinsinden açı.

    Returns:
        float: cos(angle) değeri [-1, 1] aralığında.

    Example:
        >>> round(cos(0), 10)
        1.0
        >>> round(cos(math.pi), 10)
        -1.0
    """
    return math.cos(angle)


def tan(angle: Number) -> float:
    """
    Açının tanjant değerini hesaplar (radyan).

    π/2 + k·π gibi tekil noktalarda kayan nokta hassasiyeti
    nedeniyle çok büyük (ama sonsuz değil) değerler döner.

    Args:
        angle (Number): Radyan cinsinden açı.

    Returns:
        float: tan(angle) değeri.

    Example:
        >>> round(tan(math.pi / 4), 10)
        1.0
        >>> round(tan(0), 10)
        0.0
    """
    return math.tan(angle)


# ── Derece tabanlı kısayollar ─────────────────────────────────────────────────


def sin_deg(degrees: Number) -> float:
    """
    Açının sinüs değerini hesaplar (derece).

    Args:
        degrees (Number): Derece cinsinden açı.

    Returns:
        float: sin(degrees) değeri.

    Example:
        >>> round(sin_deg(90), 10)
        1.0
        >>> round(sin_deg(30), 10)
        0.5
    """
    return math.sin(math.radians(degrees))


def cos_deg(degrees: Number) -> float:
    """
    Açının kosinüs değerini hesaplar (derece).

    Args:
        degrees (Number): Derece cinsinden açı.

    Returns:
        float: cos(degrees) değeri.

    Example:
        >>> round(cos_deg(60), 10)
        0.5
        >>> round(cos_deg(0), 10)
        1.0
    """
    return math.cos(math.radians(degrees))


def tan_deg(degrees: Number) -> float:
    """
    Açının tanjant değerini hesaplar (derece).

    Args:
        degrees (Number): Derece cinsinden açı.

    Returns:
        float: tan(degrees) değeri.

    Example:
        >>> round(tan_deg(45), 10)
        1.0
    """
    return math.tan(math.radians(degrees))


# ── Ters trigonometrik fonksiyonlar ───────────────────────────────────────────


def asin(x: Number) -> float:
    """
    Arcsin (ters sinüs) değerini radyan cinsinden döndürür.

    Args:
        x (Number): [-1, 1] aralığında sinüs değeri.

    Returns:
        float: Radyan cinsinden açı [-π/2, π/2].

    Raises:
        ValueError: |x| > 1 olduğunda standart math modülü hata fırlatır.

    Example:
        >>> round(asin(1), 10)
        1.5707963268
    """
    return math.asin(x)


def acos(x: Number) -> float:
    """
    Arccos (ters kosinüs) değerini radyan cinsinden döndürür.

    Args:
        x (Number): [-1, 1] aralığında kosinüs değeri.

    Returns:
        float: Radyan cinsinden açı [0, π].

    Example:
        >>> round(acos(1), 10)
        0.0
    """
    return math.acos(x)


def atan(x: Number) -> float:
    """
    Arctan (ters tanjant) değerini radyan cinsinden döndürür.

    Args:
        x (Number): Tanjant değeri (tüm reel sayılar).

    Returns:
        float: Radyan cinsinden açı (-π/2, π/2).

    Example:
        >>> round(atan(1), 10)
        0.7853981634
    """
    return math.atan(x)


def atan2(y: Number, x: Number) -> float:
    """
    İki argümanlı arctan (atan2) fonksiyonu.

    Koordinat düzleminde (x, y) noktasının pozitif x-ekseniyle
    yaptığı açıyı doğru çeyreğe göre döndürür.

    Args:
        y (Number): y koordinatı.
        x (Number): x koordinatı.

    Returns:
        float: Radyan cinsinden açı (-π, π].

    Example:
        >>> round(atan2(1, 1), 10)
        0.7853981634
    """
    return math.atan2(y, x)


# ── Hiperbolik fonksiyonlar ───────────────────────────────────────────────────


def sinh(x: Number) -> float:
    """
    Hiperbolik sinüs değerini hesaplar.

    Args:
        x (Number): Girdi değeri.

    Returns:
        float: sinh(x) değeri.

    Example:
        >>> round(sinh(0), 10)
        0.0
    """
    return math.sinh(x)


def cosh(x: Number) -> float:
    """
    Hiperbolik kosinüs değerini hesaplar.

    Args:
        x (Number): Girdi değeri.

    Returns:
        float: cosh(x) değeri.

    Example:
        >>> round(cosh(0), 10)
        1.0
    """
    return math.cosh(x)


def tanh(x: Number) -> float:
    """
    Hiperbolik tanjant değerini hesaplar.

    Args:
        x (Number): Girdi değeri.

    Returns:
        float: tanh(x) değeri (-1, 1).

    Example:
        >>> round(tanh(0), 10)
        0.0
    """
    return math.tanh(x)