#!/usr/bin/python
# -*- coding: utf-8 -*-
# vim: ts=4
"""
Módulo unificado para la gestión de contracciones fonético-ortográficas.
"""

import re

from andaluh.de import transformar_preposicion_de
from andaluh.en import transformar_preposicion_en
from andaluh.pa import transformar_preposicion_pa
from andaluh.ya import transformar_adverbio_ya
from andaluh.pronombres import transformar_pronombres_atonos
from andaluh.articulos import transformar_articulos


# Patrón: cualquier carácter de palabra o puntuación seguido de espacio(s)
# y luego un apóstrofe que NO está precedido de letra (es decir, empieza la contracción).
# Cubre 'e, 'r, 'n y cualquier otra contracción con apóstrofe inicial.
_RE_APOSTROFE_INICIAL = re.compile(r"(\S)\s+'(?=[^\s])", re.UNICODE)


def _pegar_apostrofe_inicial(texto: str) -> str:
    """Elimina el espacio entre la palabra anterior y un apóstrofe inicial.

    Transforma casos como ``puñao 'e pan`` → ``puñao'e pan`` o
    ``iré 'n zinco`` → ``iré'n zinco``.

    No afecta a contracciones con letra antes del apóstrofe (``d'``, ``p'``,
    ``l'``, ``m'``, etc.) porque esas no tienen espacio previo al apóstrofe.
    """
    return _RE_APOSTROFE_INICIAL.sub(r"\1'", texto)


def apply_contractions(texto: str) -> str:
    """
    Aplica todas las contracciones fonéticas y ortográficas soportadas:
    - Pronombres átonos 'me', 'te', 'se', 'le', 'la', 'lo' (m', t', s', l')
    - Preposición 'en' (n'el, 'n) - Ejecutada antes para prioridad n'el
    - Artículos determinados 'el', 'la' (l', 'r)
    - Preposición 'de' (d', 'e)
    - Preposición 'pa' (p')
    - Adverbio 'ya' (y')

    Args:
        texto (str): Cadena de texto de entrada.

    Returns:
        str: Texto con todas las contracciones aplicadas.
    """
    if not texto:
        return texto

    texto = transformar_pronombres_atonos(texto)
    texto = transformar_preposicion_en(texto)
    texto = transformar_articulos(texto)
    texto = transformar_preposicion_de(texto)
    texto = transformar_preposicion_pa(texto)
    texto = transformar_adverbio_ya(texto)
    texto = _pegar_apostrofe_inicial(texto)
    return texto


# Alias en español para la API
aplicar_contracciones = apply_contractions
