"""
TRAImath
========
Hafif, güvenli ve genişletilebilir bir Python matematik kütüphanesi.

Modüller
--------
- **basic**    : Temel aritmetik (toplama, çıkarma, çarpma, bölme…)
- **advanced** : Gelişmiş fonksiyonlar (üs, karekök, faktöriyel, log…)
- **geometry** : Geometrik hesaplamalar (alan, çevre, hacim)
- **trig**     : Trigonometrik fonksiyonlar ve açı dönüşümleri
- **parser**   : Güvenli string ifade ayrıştırıcı (Shunting-Yard)
- **errors**   : Özel hata sınıfları

Hızlı Başlangıç
---------------
    >>> import traimath as tm

    # Temel aritmetik
    >>> tm.add(3, 4)
    7
    >>> tm.divide(10, 3)
    3.3333333333333335

    # Gelişmiş
    >>> tm.sqrt(144)
    12.0
    >>> tm.factorial(6)
    720

    # Geometri
    >>> round(tm.circle_area(5), 4)
    78.5398

    # Trigonometri
    >>> round(tm.sin_deg(30), 4)
    0.5

    # Parser
    >>> tm.parse("2 + 3 * (10 - 4)")
    20.0
    >>> tm.parse("sqrt(16) + 2^3")
    12.0

Versiyon
--------
    0.1.0
"""

__version__ = "0.1.0"
__author__ = "TRAImath"
__license__ = "MIT"

# ── Hata sınıfları ────────────────────────────────────────────────────────────
from traimath.errors import (
    DivisionByZeroError,
    DomainError,
    InvalidExpressionError,
    TRAIMathError,
)

# ── Temel aritmetik ───────────────────────────────────────────────────────────
from traimath.basic import (
    absolute,
    add,
    divide,
    floor_divide,
    modulo,
    multiply,
    subtract,
)

# ── Gelişmiş matematik ────────────────────────────────────────────────────────
from traimath.advanced import (
    cbrt,
    exp,
    factorial,
    gcd,
    lcm,
    log,
    log2,
    log10,
    power,
    sqrt,
)

# ── Geometri ──────────────────────────────────────────────────────────────────
from traimath.geometry import (
    circle_area,
    circle_perimeter,
    cube_surface_area,
    cube_volume,
    cylinder_volume,
    rectangle_area,
    rectangle_perimeter,
    sphere_surface_area,
    sphere_volume,
    triangle_area,
    triangle_area_heron,
    triangle_perimeter,
)

# ── Trigonometri ──────────────────────────────────────────────────────────────
from traimath.trig import (
    acos,
    asin,
    atan,
    atan2,
    cos,
    cos_deg,
    cosh,
    sin,
    sin_deg,
    sinh,
    tan,
    tan_deg,
    tanh,
    to_degrees,
    to_radians,
)

# ── Parser ────────────────────────────────────────────────────────────────────
from traimath.parser import parse, parse_safe

# ── Public API listesi ────────────────────────────────────────────────────────
__all__ = [
    # Hatalar
    "TRAIMathError",
    "DivisionByZeroError",
    "DomainError",
    "InvalidExpressionError",
    # Temel
    "add",
    "subtract",
    "multiply",
    "divide",
    "modulo",
    "floor_divide",
    "absolute",
    # Gelişmiş
    "power",
    "sqrt",
    "cbrt",
    "factorial",
    "log",
    "log2",
    "log10",
    "exp",
    "gcd",
    "lcm",
    # Geometri
    "circle_area",
    "circle_perimeter",
    "triangle_area",
    "triangle_area_heron",
    "triangle_perimeter",
    "rectangle_area",
    "rectangle_perimeter",
    "cube_volume",
    "cube_surface_area",
    "sphere_volume",
    "sphere_surface_area",
    "cylinder_volume",
    # Trigonometri
    "sin",
    "cos",
    "tan",
    "sin_deg",
    "cos_deg",
    "tan_deg",
    "asin",
    "acos",
    "atan",
    "atan2",
    "sinh",
    "cosh",
    "tanh",
    "to_radians",
    "to_degrees",
    # Parser
    "parse",
    "parse_safe",
]