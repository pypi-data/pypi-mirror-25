import sys

from transpyler import Transpyler
from . import __version__
from .keywords import TRANSLATIONS, SEQUENCE_TRANSLATIONS, ERROR_GROUPS


class PyKorTranspyler(Transpyler):
    """
    Korean support.
    """

    name = 'pykor'
    display_name = 'PyKor'
    version = __version__
    translations = dict(TRANSLATIONS)
    translations.update(SEQUENCE_TRANSLATIONS)
    error_dict = ERROR_GROUPS
    lang = 'ko'


PyKorTranspyler.banner = \
    r'''pykor %s
Python %s

한국 Python PyKor에 오신 것을 환영합니다.''' \
    % (__version__, sys.version.splitlines()[0])
