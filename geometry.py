"""
traimath.geometry
-----------------
Temel geometrik şekillerin alan, çevre ve hacim hesaplamaları.

Tüm fonksiyonlar pozitif boyut değerleri bekler; negatif veya sıfır
değer girildiğinde TRAIMathError fırlatılır.
"""

import math

from traimath.errors import TRAIMathError

Number = int | float


# ── Yardımcı doğrulama ────────────────────────────────────────────────────────


def _require_positive(*values: Number, label: str = "boyut") -> None:
    """
    Verilen değerlerin hepsinin pozitif (> 0) olduğunu doğrular.

    Args:
        *values: Kontrol edilecek sayısal değerler.
        label (str): Hata mesajında kullanılacak boyut etiketi.

    Raises:
        TRAIMathError: Herhangi bir değer <= 0 ise fırlatılır.
    """
    for v in values:
        if v <= 0:
            raise TRAIMathError(
                f"Geometri hesaplamalarında {label} pozitif olmalıdır, ancak {v!r} verildi.",
                code="INVALID_DIMENSION",
            )


# ── Daire ─────────────────────────────────────────────────────────────────────


def circle_area(radius: Number) -> float:
    """
    Dairenin alanını hesaplar.

    Alan = π · r²

    Args:
        radius (Number): Dairenin yarıçapı (pozitif).

    Returns:
        float: Dairenin alanı.

    Raises:
        TRAIMathError: radius <= 0 olduğunda fırlatılır.

    Example:
        >>> round(circle_area(5), 6)
        78.539816
    """
    _require_positive(radius, label="yarıçap")
    return math.pi * radius ** 2


def circle_perimeter(radius: Number) -> float:
    """
    Dairenin çevresini (çap × π) hesaplar.

    Çevre = 2 · π · r

    Args:
        radius (Number): Dairenin yarıçapı (pozitif).

    Returns:
        float: Dairenin çevresi.

    Raises:
        TRAIMathError: radius <= 0 olduğunda fırlatılır.

    Example:
        >>> round(circle_perimeter(5), 6)
        31.415927
    """
    _require_positive(radius, label="yarıçap")
    return 2 * math.pi * radius


# ── Üçgen ─────────────────────────────────────────────────────────────────────


def triangle_area(base: Number, height: Number) -> float:
    """
    Üçgenin taban ve yüksekliğine göre alanını hesaplar.

    Alan = (taban × yükseklik) / 2

    Args:
        base (Number): Üçgenin taban uzunluğu (pozitif).
        height (Number): Üçgenin yüksekliği (pozitif).

    Returns:
        float: Üçgenin alanı.

    Raises:
        TRAIMathError: base veya height <= 0 olduğunda fırlatılır.

    Example:
        >>> triangle_area(6, 4)
        12.0
    """
    _require_positive(base, height, label="kenar/yükseklik")
    return (base * height) / 2


def triangle_area_heron(a: Number, b: Number, c: Number) -> float:
    """
    Heron formülüyle üç kenar uzunluğundan üçgen alanını hesaplar.

    Alan = √(s(s-a)(s-b)(s-c))  ,  s = (a+b+c)/2

    Args:
        a (Number): Birinci kenar uzunluğu.
        b (Number): İkinci kenar uzunluğu.
        c (Number): Üçüncü kenar uzunluğu.

    Returns:
        float: Üçgenin alanı.

    Raises:
        TRAIMathError: Kenar değerleri geçersizse veya geçerli bir üçgen
                       oluşturmuyorsa fırlatılır.

    Example:
        >>> round(triangle_area_heron(3, 4, 5), 6)
        6.0
    """
    _require_positive(a, b, c, label="kenar")
    s = (a + b + c) / 2
    area_sq = s * (s - a) * (s - b) * (s - c)
    if area_sq < 0:
        raise TRAIMathError(
            f"Verilen kenarlar ({a}, {b}, {c}) geçerli bir üçgen oluşturmuyor.",
            code="INVALID_TRIANGLE",
        )
    return math.sqrt(area_sq)


def triangle_perimeter(a: Number, b: Number, c: Number) -> Number:
    """
    Üçgenin çevresini hesaplar.

    Çevre = a + b + c

    Args:
        a (Number): Birinci kenar.
        b (Number): İkinci kenar.
        c (Number): Üçüncü kenar.

    Returns:
        Number: Üçgenin çevresi.

    Example:
        >>> triangle_perimeter(3, 4, 5)
        12
    """
    _require_positive(a, b, c, label="kenar")
    return a + b + c


# ── Dikdörtgen / Kare ─────────────────────────────────────────────────────────


def rectangle_area(width: Number, height: Number) -> Number:
    """
    Dikdörtgenin alanını hesaplar.

    Alan = genişlik × yükseklik

    Args:
        width (Number): Genişlik (pozitif).
        height (Number): Yükseklik (pozitif).

    Returns:
        Number: Dikdörtgenin alanı.

    Example:
        >>> rectangle_area(5, 3)
        15
    """
    _require_positive(width, height, label="kenar")
    return width * height


def rectangle_perimeter(width: Number, height: Number) -> Number:
    """
    Dikdörtgenin çevresini hesaplar.

    Çevre = 2 × (genişlik + yükseklik)

    Args:
        width (Number): Genişlik (pozitif).
        height (Number): Yükseklik (pozitif).

    Returns:
        Number: Dikdörtgenin çevresi.

    Example:
        >>> rectangle_perimeter(5, 3)
        16
    """
    _require_positive(width, height, label="kenar")
    return 2 * (width + height)


# ── Küp ───────────────────────────────────────────────────────────────────────


def cube_volume(side: Number) -> Number:
    """
    Küpün hacmini hesaplar.

    Hacim = a³

    Args:
        side (Number): Küpün kenar uzunluğu (pozitif).

    Returns:
        Number: Küpün hacmi.

    Raises:
        TRAIMathError: side <= 0 olduğunda fırlatılır.

    Example:
        >>> cube_volume(3)
        27
        >>> cube_volume(2.5)
        15.625
    """
    _require_positive(side, label="kenar")
    return side ** 3


def cube_surface_area(side: Number) -> Number:
    """
    Küpün yüzey alanını hesaplar.

    Yüzey Alanı = 6 × a²

    Args:
        side (Number): Küpün kenar uzunluğu (pozitif).

    Returns:
        Number: Küpün yüzey alanı.

    Example:
        >>> cube_surface_area(4)
        96
    """
    _require_positive(side, label="kenar")
    return 6 * side ** 2


# ── Küre ──────────────────────────────────────────────────────────────────────


def sphere_volume(radius: Number) -> float:
    """
    Kürenin hacmini hesaplar.

    Hacim = (4/3) · π · r³

    Args:
        radius (Number): Kürenin yarıçapı (pozitif).

    Returns:
        float: Kürenin hacmi.

    Example:
        >>> round(sphere_volume(3), 6)
        113.097336
    """
    _require_positive(radius, label="yarıçap")
    return (4 / 3) * math.pi * radius ** 3


def sphere_surface_area(radius: Number) -> float:
    """
    Kürenin yüzey alanını hesaplar.

    Yüzey Alanı = 4 · π · r²

    Args:
        radius (Number): Kürenin yarıçapı (pozitif).

    Returns:
        float: Kürenin yüzey alanı.

    Example:
        >>> round(sphere_surface_area(3), 6)
        113.097336
    """
    _require_positive(radius, label="yarıçap")
    return 4 * math.pi * radius ** 2


# ── Silindir ──────────────────────────────────────────────────────────────────


def cylinder_volume(radius: Number, height: Number) -> float:
    """
    Silindirin hacmini hesaplar.

    Hacim = π · r² · h

    Args:
        radius (Number): Taban yarıçapı (pozitif).
        height (Number): Yükseklik (pozitif).

    Returns:
        float: Silindirin hacmi.

    Example:
        >>> round(cylinder_volume(3, 5), 6)
        141.371669
    """
    _require_positive(radius, height, label="yarıçap/yükseklik")
    return math.pi * radius ** 2 * height