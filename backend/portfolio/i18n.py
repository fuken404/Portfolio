"""
Contenido bilingüe.

Cada campo traducible existe como dos columnas: `<campo>_es` y `<campo>_en`.
El español es obligatorio; si falta el inglés se usa el español.
"""

from django.conf import settings
from django.utils.translation import get_language

DEFAULT_LANG = settings.LANGUAGE_CODE  # 'es'
LANGS = [code for code, _ in settings.LANGUAGES]


def current_lang():
    lang = (get_language() or DEFAULT_LANG).split('-')[0]
    return lang if lang in LANGS else DEFAULT_LANG


def translated(obj, field, lang=None):
    """Valor de `field` en el idioma pedido, con respaldo en el idioma por defecto."""
    value = getattr(obj, f'{field}_{lang or current_lang()}', None)
    return value or getattr(obj, f'{field}_{DEFAULT_LANG}')
