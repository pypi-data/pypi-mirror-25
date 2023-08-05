TRANSLATIONS = {
    # Loops
    '에': 'for',
    '전도금': 'pass',
    '단절': 'break',
    '동안': 'while',

    # Conditions
    '만약': 'if',
    '그밖에만약': 'elif',
    '그밖에': 'else',

    # Singleton values
    '그릇된': 'False',
    '없음': 'None',
    '참된': 'True',

    # Operators
    '되려고': 'is',
    '에서': 'in',
    '아니': 'not',
    '또는': 'or',
    '과': 'and',
    '같이': 'as',
    '지우다': 'del',

    # Function/class definitions (TODO)
    '밝히다': 'def',
    # 'clase': 'class',
    # 'defina': 'def',
    # 'función': 'def', 'funcion': 'def',
    # 'generar': 'yield',
    # 'gestiona': 'yield',
    # 'regresar': 'return',
    # 'volver': 'return',

    # Error
    # 'intentar': 'try',
    # 'intente': 'try',
    # 'excepción': 'except', 'excepcion': 'except',
    # 'finalmente': 'finally',
    # 'levantar_error': 'raise',
    # 'levante_error': 'raise',

    # Other
    # 'importar': 'import',
    # 'importe': 'import',
    # 'con': 'with',
}


# Here we can define multiple keyword conversions
SEQUENCE_TRANSLATIONS = {
    # Example
    # ('define', 'function'): 'def',
}


# Here we define sequences of tokens that are definitively errors and the
# corresponding error messages.
ERROR_GROUPS = {
    # ('for', 'for'): 'Repeated use of keyword 'for',
}
