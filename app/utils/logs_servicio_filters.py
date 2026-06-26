from sqlalchemy import and_, func, or_

from app.models.logs_servicio import LogsServicio

SUCURSAL_CODES = frozenset({"ROS", "PAR", "CBA", "BAS", "SFE"})
ESTADO_VALUES = frozenset(
    {"confirmado", "confirmado_parcial", "cancelado", "cancelado_parcial", "pendiente"}
)
LLEGADA_VALUES = frozenset(
    {
        "llego_horario",
        "llego_tarde",
        "en_camino",
        "en_camino_tarde",
        "esperando_respuesta",
        "sin_dato",
    }
)


def _asiste_normalized():
    return func.lower(func.trim(func.coalesce(LogsServicio.asiste, "")))


def _llegada_normalized():
    return func.lower(func.trim(func.coalesce(LogsServicio.llego_a_tiempo, "")))


def apply_sucursal_filter(query, sucursal: str | None):
    if not sucursal or sucursal == "todas":
        return query

    code = sucursal.strip().upper()
    if code not in SUCURSAL_CODES:
        return query

    un_normalized = func.upper(func.trim(func.coalesce(LogsServicio.un, "")))
    return query.where(un_normalized == code)


def _estado_confirmado_parcial():
    asiste = _asiste_normalized()
    return and_(asiste.like("%confirmado%"), asiste.like("%parcial%"))


def _estado_cancelado_parcial():
    asiste = _asiste_normalized()
    return and_(asiste.like("%cancelado%"), asiste.like("%parcial%"))


def _estado_confirmado():
    asiste = _asiste_normalized()
    return or_(
        and_(asiste.like("%confirmado%"), ~asiste.like("%parcial%")),
        asiste == "si",
    )


def _estado_cancelado():
    asiste = _asiste_normalized()
    return or_(
        and_(asiste.like("%cancelado%"), ~asiste.like("%parcial%")),
        asiste == "no",
    )


def _estado_pendiente():
    return ~or_(
        _estado_confirmado_parcial(),
        _estado_cancelado_parcial(),
        _estado_confirmado(),
        _estado_cancelado(),
    )


def apply_estado_filter(query, estado: str | None):
    if not estado or estado == "todos":
        return query

    if estado not in ESTADO_VALUES:
        return query

    conditions = {
        "confirmado_parcial": _estado_confirmado_parcial(),
        "cancelado_parcial": _estado_cancelado_parcial(),
        "confirmado": _estado_confirmado(),
        "cancelado": _estado_cancelado(),
        "pendiente": _estado_pendiente(),
    }

    return query.where(conditions[estado])


def _llegada_esperando_respuesta():
    return _llegada_normalized().like("%esperando respuesta%")


def _llegada_en_camino_tarde():
    llegada = _llegada_normalized()
    return and_(llegada.like("%en camino%"), llegada.like("%tarde%"))


def _llegada_en_camino():
    llegada = _llegada_normalized()
    return and_(llegada.like("%en camino%"), ~llegada.like("%tarde%"))


def _llegada_llego_tarde():
    llegada = _llegada_normalized()
    return and_(llegada.like("%tarde%"), ~llegada.like("%en camino%"))


def _llegada_llego_horario():
    llegada = _llegada_normalized()
    return and_(
        func.length(llegada) > 0,
        ~llegada.like("%esperando respuesta%"),
        ~llegada.like("%en camino%"),
        ~llegada.like("%tarde%"),
    )


def _llegada_sin_dato():
    return or_(
        LogsServicio.llego_a_tiempo.is_(None),
        func.length(func.trim(func.coalesce(LogsServicio.llego_a_tiempo, ""))) == 0,
    )


def apply_llegada_filter(query, llegada: str | None):
    if not llegada or llegada == "todos":
        return query

    if llegada not in LLEGADA_VALUES:
        return query

    conditions = {
        "esperando_respuesta": _llegada_esperando_respuesta(),
        "en_camino_tarde": _llegada_en_camino_tarde(),
        "en_camino": _llegada_en_camino(),
        "llego_tarde": _llegada_llego_tarde(),
        "llego_horario": _llegada_llego_horario(),
        "sin_dato": _llegada_sin_dato(),
    }

    return query.where(conditions[llegada])
