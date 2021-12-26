import math
from string import ascii_uppercase
from typing import Union


def int32d(value) -> Union[int, float]:
    try:
        converted = float(value)
        str_abs_v = str(value).lstrip('-')
        if 'e+' in str_abs_v:
            l_int_v = int(str_abs_v.split('+')[-1])
        else:
            str_int_abs_v = str_abs_v.split('.')[0]
            l_int_v = len(str_int_abs_v)

        if converted.is_integer() and l_int_v < 33:
            return int(value)

    except OverflowError:
        converted = math.copysign(math.inf, int(str(value)[:2]))

    return converted


# ----------------------------------------------------------------------------------------------------------------------
# Enigma
ORD_ZERO = ord('A')
ALPHABET = ascii_uppercase
L = len(ALPHABET)


def set_keys_enig(args) -> list:
    optkeys = []
    nb_rotors = max(0, args[1])
    optkeys.extend([f'rotor{i}' for i in range(nb_rotors)])
    optkeys.append('message')

    return optkeys


def build_rotor_from_int(n) -> str:
    rotor = []
    k = L
    alpha = list(ALPHABET)
    while k:
        q, n = divmod(n, factorial(k - 1))
        rotor.append(alpha.pop(q))
        k -= 1

    return ''.join(rotor)


def build_rotor_from_str(s) -> str:
    rotor = dict.fromkeys([e for e in s.upper() if e in ALPHABET] + list(ALPHABET))
    return ''.join(rotor)


def convert_entries_enig(value) -> Union[int, str]:
    try:
        value = int(value) % factorial(L)
    except ValueError:
        if not value.isalpha():
            print(f"Note: {value} n'a pas le format requis et sera transformé pour l'opération")

    return value


def shift_message(msg, shift, dr) -> str:
    shifted_msg = ''
    for i in range(len(msg)):
        shifted_msg += chr(ORD_ZERO + (ord(msg[i]) - ORD_ZERO + dr * (shift + i)) % 26)
    return shifted_msg


def encode(msg, shift, rotors) -> str:
    msg = shift_message(msg, shift, 1)
    for rotor in rotors:
        msg = ''.join(rotor[ord(char) - ORD_ZERO] for char in msg)
    return msg


def decode(msg, shift, rotors) -> str:
    for rotor in reversed(rotors):
        msg = ''.join(chr(ORD_ZERO + rotor.index(char)) for char in msg)
    msg = shift_message(msg, shift, -1)
    return msg


def enigma(args, encrypt=True) -> str:
    init_shift = args[0]

    rotors = []
    for e in args[2:-1]:
        rotor = build_rotor_from_int(e) if type(e) == int else build_rotor_from_str(e)
        rotors.append(rotor)
        print(rotor)

    message = ''.join([('?', e)[e in ALPHABET] for e in str(args[-1]).replace(' ', '').upper()])

    if encrypt:
        return encode(message, init_shift, rotors)

    return decode(message, init_shift, rotors)


def denigma(args) -> str:
    return enigma(args, False)


# ----------------------------------------------------------------------------------------------------------------------
# Maths

def add(xy) -> Union[int, float]:
    return int32d(sum(xy))


def sub(xy) -> Union[int, float]:
    x, y = xy
    return int32d(x - y)


def multi(xy) -> Union[int, float]:
    return int32d(math.prod(xy))


def div(xy) -> Union[int, float]:
    x, y = xy
    return x * math.inf if y == 0 else int32d(x / y)


def div_euc(xy) -> Union[int, float]:
    x, y = xy
    return x * math.inf if y == 0 else int32d(x // y)


def modulo(xy) -> Union[int, float]:
    x, y = xy
    return 0 if y == 0 else int32d(x % y)


def power(xy) -> Union[int, float]:
    x, y = xy
    try:
        res = int32d(math.pow(x, y))
    except ValueError:
        res = math.nan
    except OverflowError:
        res = math.inf if x > 0 else math.inf * math.pow(-1, int(str(y)[-1]) % 2)

    return res


def combination(kn) -> Union[int, float]:
    n = kn[1]
    k = min(kn[0], n - kn[0])
    arrg_kn = factorial(n, n - k, True)
    if arrg_kn in (0, math.nan, math.inf):
        res = arrg_kn
    else:
        res = arrg_kn // factorial(k, comb=True)
    return int32d(res)


def arrangements(kn) -> Union[int, float]:
    k, n = kn
    return factorial(n, n - k)


def factorial(value: Union[list, int], base=0, comb=False) -> Union[int, float]:
    n = value[0] if type(value) == list else value

    if n < 0:
        return math.nan

    if not 0 <= base <= n:
        return 0

    if (not comb and n - base > 170) or n - base > 514:
        return math.inf

    p = 1
    for i in range(n - base):
        p *= base + i + 1

    return p if comb else int32d(p)


def gamma(arg) -> float:
    x = arg[0]

    try:
        res = math.gamma(x)
    except OverflowError:
        res = math.inf if x > 0 else math.inf * math.pow(-1, 1 + math.ceil(x) % 2)
    except ValueError:
        res = math.nan

    return res


def set_keys_lr(args) -> list:
    order = max(1, min(args[1], 10000))
    optkeys = [f'u{i}' for i in range(order)]
    optkeys.extend([f'coef{j}' for j in range(order)])

    return optkeys


def linear_recurrence(values) -> Union[int, float]:
    n = max(0, values[0])
    order = max(1, values[1])
    computations = values[2:(order + 2)]
    coeffs = values[(order + 2):]

    if n > 1e+5 or n * order > 1e+6:
        return math.nan

    if n < order:
        return computations[n]

    for k in range(order, n + 1):
        computations.append(sum(computations[i] * coeffs[i] for i in range(order)))
        del computations[0]

    return int32d(computations[-1])


def fibonacci(n) -> Union[int, float]:
    r = max(0, n[0])
    return linear_recurrence([r, 2, 1, 1, 1, 1])


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
    return sum(scored[i] * scoring_values[i] for i in range(len(scoring_values)))


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
            '+': {
                    'name': 'Addition',
                    'function': add,
                    'convert': int32d,
                    'opt_proc': None,
                    'arg_keys': ('1er terme', '2nd terme'),
                    'opt_keys': None,
                    'opt_conv': None
                },

            '-': {
                    'name': 'Soustraction',
                    'function': sub,
                    'convert': int32d,
                    'opt_proc': None,
                    'arg_keys': ('diminuende', 'diminuteur'),
                    'opt_keys': None,
                    'opt_conv': None
                },

            '*': {
                    'name': 'Multiplication',
                    'function': multi,
                    'convert': int32d,
                    'opt_proc': None,
                    'arg_keys': ('1er terme', '2nd terme'),
                    'opt_keys': None,
                    'opt_conv': None
                },

            '/': {
                    'name': 'Division',
                    'function': div,
                    'convert': int32d,
                    'opt_proc': None,
                    'arg_keys': ('numérateur', 'dénominateur'),
                    'opt_keys': None,
                    'opt_conv': None
                },

            '//': {
                    'name': 'Division Euclidienne',
                    'function': div_euc,
                    'convert': int32d,
                    'opt_proc': None,
                    'arg_keys': ('numérateur', 'dénominateur'),
                    'opt_keys': None,
                    'opt_conv': None
                },

            '%': {
                    'name': 'Modulo',
                    'function': modulo,
                    'convert': int32d,
                    'opt_proc': None,
                    'arg_keys': ('numérateur', 'dénominateur'),
                    'opt_keys': None,
                    'opt_conv': None
                },

            '**': {
                    'name': 'Puissance',
                    'function': power,
                    'convert': int32d,
                    'opt_proc': None,
                    'arg_keys': ('base', 'exposant'),
                    'opt_keys': None,
                    'opt_conv': None
                },

            'xv': {
                    'name': 'Score de rugby à XV',
                    'function': rugby_xv,
                    'convert': convert_entries_sports,
                    'opt_proc': check_entries_rugby,
                    'arg_keys': ('essais', 'transformations', 'pénalités', 'drops'),
                    'opt_keys': None,
                    'opt_conv': None
                },

            'xiii': {
                    'name': 'Score de rugby à XIII',
                    'function': rugby_xiii,
                    'convert': convert_entries_sports,
                    'opt_proc': check_entries_rugby,
                    'arg_keys': ('essais', 'transformations', 'pénalités', 'drops'),
                    'opt_keys': None,
                    'opt_conv': None
                },

            'amf': {
                    'name': 'Score de football américain',
                    'function': american_football,
                    'convert': convert_entries_sports,
                    'opt_proc': check_entries_amf,
                    'arg_keys': ('touchdowns', 'extra-points', '2pts-conversions', 'field goals', 'safeties'),
                    'opt_keys': None,
                    'opt_conv': None
                },

            'bsk': {
                    'name': 'Score de Basketball',
                    'function': basketball,
                    'convert': convert_entries_sports,
                    'opt_proc': None,
                    'arg_keys': ('paniers à 2pts', 'paniers à 3pts', 'lancers-francs'),
                    'opt_keys': None,
                    'opt_conv': None
                },

            '!': {
                    'name': 'Factorielle',
                    'function': factorial,
                    'convert': int,
                    'opt_proc': None,
                    'arg_keys': ('nombre entier',),
                    'opt_keys': None,
                    'opt_conv': None
                },

            'gam': {
                    'name': 'Fonction Gamma',
                    'function': gamma,
                    'convert': int32d,
                    'opt_proc': None,
                    'arg_keys': ('nombre réel',),
                    'opt_keys': None,
                    'opt_conv': None
                },

            'comb': {
                    'name': 'Combinaison de k dans n',
                    'function': combination,
                    'convert': int,
                    'opt_proc': None,
                    'arg_keys': ('entier k', 'entier n'),
                    'opt_keys': None,
                    'opt_conv': None
                },

            'arr': {
                    'name': 'Arrangements de k dans n',
                    'function': arrangements,
                    'convert': int,
                    'opt_proc': None,
                    'arg_keys': ('entier k', 'entier n'),
                    'opt_keys': None,
                    'opt_conv': None
                },

            'fib': {
                    'name': 'Suite de Fibonacci',
                    'function': fibonacci,
                    'convert': int,
                    'opt_proc': None,
                    'arg_keys': ('rang',),
                    'opt_keys': None,
                    'opt_conv': None
                },

            'lr': {
                    'name': 'Récurrence linéaire',
                    'function': linear_recurrence,
                    'convert': int,
                    'opt_proc': None,
                    'arg_keys': ('rang', 'ordre'),
                    'opt_keys': set_keys_lr,
                    'opt_conv': int32d
                },

            'enig': {
                    'name': 'Enigma',
                    'function': enigma,
                    'convert': int,
                    'opt_proc': None,
                    'arg_keys': ('shift', 'nombre de rotors'),
                    'opt_keys': set_keys_enig,
                    'opt_conv': convert_entries_enig
                },

            'denig': {
                    'name': 'Enigma',
                    'function': denigma,
                    'convert': int,
                    'opt_proc': None,
                    'arg_keys': ('shift', 'nombre de rotors'),
                    'opt_keys': set_keys_enig,
                    'opt_conv': convert_entries_enig
                },
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
