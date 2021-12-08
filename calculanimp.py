import sys
import re
import nimperators as nimp

# ----------------------------------------------------------------------------------------------------------------------
# Functions


def get_error_message(msg, except_label) -> str:
    return f"{msg} {str(except_label).split(' (')[0]}"


def get_from_command(value_lst, cmd, convert) -> bool:
    got = False
    if not cmd:
        return got

    value, _, __ = process_input(cmd[0])

    try:
        value = convert(value)
        value_lst.append(value)
        del cmd[0]
        got = True
    except ValueError:
        pass
    except TypeError:
        pass
    # except NameError:
    #     pass

    return got


def get_entries(to_get_list, cmd, convert=None, straight_from_input=False) -> list:
    global path
    path.append(cmd.pop(0))
    path_str = '>'.join(path)

    if convert is None:
        convert = int
    values = []

    for key in to_get_list:
        if straight_from_input or not get_from_command(values, cmd, convert):
            while True:
                try:
                    raw, _, __ = process_input(input(f'{path_str}>{key.capitalize()}> '))
                    entry = convert(raw)
                    values.append(entry)
                    break
                except ValueError as e:
                    print(get_error_message('Warning:', e))
                except TypeError as e:
                    print(get_error_message('Warning:', e))

    del path[-1]

    return values


def process_command(cmd) -> tuple:
    c = cmd[0]
    if c not in operators.keys():
        return None, get_error_message(f'${c}', 'InvalidCommand'), False

    c_keys = operators[c]['arg_keys']
    c_func = operators[c]['function']

    if c_keys is not None:
        values = get_entries(c_keys, cmd)
        cmd_args, to_cache = values, True
    else:
        values, cmd_args, to_cache = None, [], False

    rslt = c_func(values)

    return rslt, ' '.join((c, ' '.join(map(str, cmd_args)))).rstrip(), to_cache


def process_input(string) -> tuple:
    if string.startswith('$'):
        rslt, cmd, to_cache = process_command(string.lstrip('$').split())

    elif not re.findall(r'[^0-9e%.()/+*_\- ]', string):
        rslt = None
        cmd = string
        to_cache = False

        try:
            rslt = eval(string)
            to_cache = True

        except SyntaxError as e:
            cmd += get_error_message(' Warning:', e)
        except ZeroDivisionError as e:
            cmd += get_error_message(' Warning:', e)
        except TypeError as e:
            cmd += get_error_message(' Warning:', e)
        except NameError as e:
            cmd += get_error_message(' Warning:', e)

    else:
        rslt = string
        cmd = 'str'
        to_cache = True

    return rslt, cmd, to_cache

# -----------------------------------------------------------------------------------------------------------------------
# Operators Dictionary


def get_operators_list(*_args) -> str:
    doc = '\n'
    for key in operators.keys():
        op = operators[key]
        doc = ''.join((doc, f"${key}: {op['name']}\n"
                            f"\t{str(op['function']).split()[1]}({str(op['arg_keys']).strip('()')})\n"))
    return doc


operators = nimp.commands
operators['\\'] = {
                    'name': 'Exit',
                    'function': sys.exit,
                    'arg_keys': None
                    }
operators['h'] = {
                    'name': 'Aide',
                    'function': get_operators_list,
                    'arg_keys': None
                    }

# ----------------------------------------------------------------------------------------------------------------------

calc_cache = []
path = []
print(f'Entrez directement des opérations (ex: 11.2 + 4**3)\nou $h pour voir les commandes spéciales')

while True:
    print(f'cache -> {calc_cache}')
    result, command, send_to_cache = process_input(input(f'> ')[:256])

    print(f'{command} -> {result}')
    if send_to_cache:
        calc_cache.append(result)
