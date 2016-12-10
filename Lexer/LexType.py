import re

lex_types = (

        ("words", ['^if$', '^while$', '^else$',
            '^elif$']),

        ("bool_op", ['^and$', '^or$', '^not$']),

        ("bools", ['^True$', '^False$']),

        ("alg_ops", ['^\+$', '^-$', '^\*$', '^\+=$', '^-=$',
            '^\*=$', '^=$', '^/=$', '^/$']),

        ("comp_op", ['^<$', '^>$', '^<=$', '^>=$', '^==$']),

        ("brackets", ['^\($', '^\)$']),

        ("spec_symbols", ['^:$', '^\t$']),

        ("num", ['^[0-9]+$']),
        ("float_num", ['^\d+\.\d+$']),

        ("string", ['^".*"$']),

        ("var_name", ['^[a-zA-Z_]+[a-zA-Z0-9]*$']),

        ("space", ['^\s?$']),

        ("string_start", ['^".*']),

        ("space", ['^\d+\.$'])
)


def get_type(string):

        for type in lex_types:
                for pattern in type[1]:
                        if re.match(re.compile(pattern), string):
                                return type[0]
        return None