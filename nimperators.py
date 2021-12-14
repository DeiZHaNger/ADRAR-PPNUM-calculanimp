import functools
# ----------------------------------------------------------------------------------------------------------------------
# Maths


def combination(kn) -> int:
    k = kn[0]
    n = kn[1]

    return int(factorial([n]) / factorial([k]) / factorial([n - k]))


def arrangements(kn) -> int:
    k = kn[0]
    n = kn[1]

    return int(factorial([n]) / factorial([n - k]))


def factorial(n) -> int:
    p = 1
    for i in range(n[0]):
        p *= i + 1
    return p


# @functools.lru_cache(1028)
# def linear_recurrence(args) -> float:
#     n = args[0]
#     init_values = args[1]
#     parameters = args[2]
#
#     order = len(init_values)
#     len_diff = len(parameters) - order
#
#     if len_diff > 0:
#         for i in range(len_diff):
#             init_values.append(0)
#     if len_diff < 0:
#         for i in range(len_diff):
#             parameters.append(1)
#
#     if n < order:
#         return init_values[n]
#
#     n_rank_value = sum(linear_recurrence(n - i) * parameters[(n - i) % order] for i in range(order, 0, -1))
#
#     return n_rank_value


# ----------------------------------------------------------------------------------------------------------------------
# Sports

def check_entries_rugby(values) -> tuple[bool, str]:
    tries, conversions = values[0], values[1]
    retry, error = False, None

    if conversions > tries:
        error = f'{conversions} conversions pour {tries} essais/touchdowns: Nombres non valides'
        retry = True

    return retry, error


def check_entries_amf(values) -> tuple[bool, str]:
    return check_entries_rugby([values[0], values[1] + values[2]])


def convert_entries_sports(value) -> int:
    converted = int(float(value))
    if not 0 <= converted < 50000:
        raise ValueError(f'{value} n\'est pas adapté pour du sport :p')

    return converted


def get_score(scored, scoring_values) -> int:
    return sum(scored[i] * scoring_values[i] for i in range(len(scored)))


def rugby_xv(scored_nbs) -> int:
    scoring_values = [5, 2, 3, 3]
    return get_score(scored_nbs, scoring_values)


def rugby_xiii(scored_nbs) -> int:
    scoring_values = [4, 2, 2, 1]
    return get_score(scored_nbs, scoring_values)


def american_football(scored_nbs) -> int:
    scoring_values = [6, 1, 2, 3, 2]
    return get_score(scored_nbs, scoring_values)


def basketball(scored_nbs) -> int:
    scoring_values = [2, 3, 1]
    return get_score(scored_nbs, scoring_values)


# ----------------------------------------------------------------------------------------------------------------------
# Dictonary

commands = {

            'xv': {
                    'name': 'Score de rugby à XV',
                    'function': rugby_xv,
                    'convert': convert_entries_sports,
                    'opt_proc': check_entries_rugby,
                    'arg_keys': ('essais', 'transformations', 'pénalités', 'drops')
                },

            'xiii': {
                    'name': 'Score de rugby à XIII',
                    'function': rugby_xiii,
                    'convert': convert_entries_sports,
                    'opt_proc': check_entries_rugby,
                    'arg_keys': ('essais', 'transformations', 'pénalités', 'drops')
                },

            'amf': {
                    'name': 'Score de football américain',
                    'function': american_football,
                    'convert': convert_entries_sports,
                    'opt_proc': check_entries_amf,
                    'arg_keys': ('touchdowns', 'extra-points', '2pts-conversions', 'field goals', 'safeties')
                },

            'bsk': {
                    'name': 'Score de Basketball',
                    'function': basketball,
                    'convert': convert_entries_sports,
                    'opt_proc': None,
                    'arg_keys': ('paniers à 2pts', 'paniers à 3pts', 'lancers-francs')
                },

            '!': {
                    'name': 'Factorielle',
                    'function': factorial,
                    'convert': int,
                    'opt_proc': None,
                    'arg_keys': ('nombre entier',)
                },

            'comb': {
                    'name': 'Combinaison de k dans n',
                    'function': combination,
                    'convert': int,
                    'opt_proc': None,
                    'arg_keys': ('entier k', 'entier n')
                },

            'arr': {
                    'name': 'Arrangements de k dans n',
                    'function': arrangements,
                    'convert': int,
                    'opt_proc': None,
                    'arg_keys': ('entier k', 'entier n')
                },

            # not implemented 'fib': 'fibonacci',
            'lr': {
                    'name': 'Récurrence linéaire',
                    'function': linear_recurrence,
                    'convert': float,
                    'opt_proc': None,
                    'arg_keys': ('rang', 'valeurs initiales', 'coefficients')
                },
            # not implemented 'enig': 'enigma',
            # not implemented 'cc': 'clear_cache',
            # not implemented 'gc': 'get_from_cache',
            }

# ----------------------------------------------------------------------------------------------------------------------

if __name__ == '__main__':

    def get_operators_list() -> str:
        doc = '\n'
        for key in commands.keys():
            elm = commands[key]
            doc = ''.join((doc, f"{key}: {elm['name']}\n\t{str(elm['function']).split()[1]}{elm['arg_keys']}\n"))

        return doc

    print(get_operators_list())
