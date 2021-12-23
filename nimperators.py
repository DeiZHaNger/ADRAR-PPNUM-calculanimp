import math
from string import ascii_uppercase
from typing import Union

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

    message = ''.join([('?', e)[e in ALPHABET] for e in args[-1].replace(' ', '').upper()])

    if encrypt:
        return encode(message, init_shift, rotors)

    return decode(message, init_shift, rotors)


def denigma(args) -> str:
    return enigma(args, False)


# ----------------------------------------------------------------------------------------------------------------------
# Maths

def combination(kn) -> int:
    k = kn[0]
    return int(arrangements(kn) / factorial(k))


def arrangements(kn) -> int:
    k = kn[0]
    n = kn[1]
    return int(factorial(n) / factorial(n - k))


def factorial(value: Union[list, int]) -> int:
    n = value[0] if type(value) == list else value
    p = 1
    for i in range(n):
        p *= i + 1
    return p


def convert_entries_gam(value) -> float:
    converted = float(value)
    if converted < 1:
        raise ValueError(f'{value}: Le calcul est trop imprécis pour valeur < 1')

    return converted


def gamma(arg) -> float:
    x = arg[0]
    if x.is_integer():
        return factorial([int(x) - 1])

    dt = 1e-3
    res = 0.0
    try:
        for i in range(int(1000/dt)):
            t = i * dt
            res += math.exp(-t) * math.pow(t, x - 1) * dt
    except OverflowError:
        return math.inf

    return round(res, 7)


def set_keys_lr(args) -> list:
    order = max(1, args[1])
    optkeys = [f'u{i}' for i in range(order)]
    optkeys.extend([f'coef{j}' for j in range(order)])

    return optkeys


def linear_recurrence(values) -> float:
    n = max(0, values[0])
    order = max(1, values[1])
    computations = values[2:(order + 2)]
    coeffs = values[(order + 2):]

    if n < order:
        return computations[n]

    for k in range(order, n + 1):
        computations.append(sum(computations[i] * coeffs[i] for i in range(order)))
        del computations[0]

    return computations[-1]


def fibonacci(n) -> float:
    r = max(0, n[0])
    return linear_recurrence([r, 2, 1.0, 1.0, 1.0, 1.0])


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
                    'convert': convert_entries_gam,
                    'opt_proc': None,
                    'arg_keys': ('nombre réel >= 1 ',),
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
                    'opt_conv': float
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
                }
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
