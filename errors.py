"""
traimath.errors
---------------
TRAImath kütüphanesine ait özel hata sınıfları.

Tüm hatalar TRAIMathError temel sınıfından türetilmiştir;
bu sayede kullanıcılar tek bir except bloğuyla tüm kütüphane
hatalarını yakalayabilir.
"""


class TRAIMathError(Exception):
    """
    TRAImath kütüphanesinin temel hata sınıfı.

    Tüm özel hatalar bu sınıftan türetilir.

    Attributes:
        message (str): Hatayı açıklayan mesaj.
        code (str): Hata kodu (opsiyonel, varsayılan "TRAIMATH_ERROR").
    """

    def __init__(self, message: str, code: str = "TRAIMATH_ERROR") -> None:
        self.message = message
        self.code = code
        super().__init__(f"[{self.code}] {self.message}")

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(message={self.message!r}, code={self.code!r})"


class DivisionByZeroError(TRAIMathError):
    """
    Sıfıra bölme işlemi denendiğinde fırlatılır.

    Example:
        >>> from traimath.errors import DivisionByZeroError
        >>> raise DivisionByZeroError()
        [DIVISION_BY_ZERO] Sıfıra bölme işlemi gerçekleştirilemez.
    """

    def __init__(self, message: str = "Sıfıra bölme işlemi gerçekleştirilemez.") -> None:
        super().__init__(message, code="DIVISION_BY_ZERO")


class InvalidExpressionError(TRAIMathError):
    """
    Geçersiz veya ayrıştırılamayan bir ifade girildiğinde fırlatılır.

    Attributes:
        expression (str): Hatalı ifadenin kendisi.

    Example:
        >>> from traimath.errors import InvalidExpressionError
        >>> raise InvalidExpressionError("2 ** ** 3")
        [INVALID_EXPRESSION] Geçersiz ifade: '2 ** ** 3'
    """

    def __init__(
        self,
        expression: str = "",
        message: str = "",
    ) -> None:
        self.expression = expression
        if not message:
            message = (
                f"Geçersiz ifade: {expression!r}"
                if expression
                else "Geçersiz matematiksel ifade."
            )
        super().__init__(message, code="INVALID_EXPRESSION")


class DomainError(TRAIMathError):
    """
    Bir fonksiyona tanım kümesi dışında değer verildiğinde fırlatılır.

    Örnek: sqrt(-1), log(0), log(-5)

    Example:
        >>> from traimath.errors import DomainError
        >>> raise DomainError("sqrt", -1)
        [DOMAIN_ERROR] 'sqrt' fonksiyonu için geçersiz giriş: -1
    """

    def __init__(self, func_name: str, value: float, hint: str = "") -> None:
        self.func_name = func_name
        self.value = value
        msg = f"'{func_name}' fonksiyonu için geçersiz giriş: {value}"
        if hint:
            msg += f". İpucu: {hint}"
        super().__init__(msg, code="DOMAIN_ERROR")