import sys
import re
import nimperators as nimp

ERROR_STR_ID = '>>!!'


class CalledHelp(Exception):
    pass

# ----------------------------------------------------------------------------------------------------------------------
# Functions


def get_error_message(msg, except_label) -> str:
    return f"{ERROR_STR_ID}{msg} {str(except_label).split(' (')[0]}"


def get_entries(to_get_list, cmd, convert=None, straight_from_input=False) -> list:
    global path
    path.append(cmd.pop(0))
    path_str = '>'.join(path)

    if convert is None:
        convert = str
    values = []

    for key in to_get_list:
        straight = straight_from_input
        while True:
            try:
                if not straight and cmd:
                    raw, msg, _ = process_input(cmd[0])
                    del cmd[0]
                    straight = True
                else:
                    raw, msg, _ = process_input(input(f'{path_str}>{key.capitalize()}> '))

                if str(msg).find(ERROR_STR_ID) != -1:
                    raise NameError(msg)
                if msg == '$h':
                    raise CalledHelp

                entry = convert(raw)
                values.append(entry)
                break
            except CalledHelp:
                pass
            except NameError as e:
                print(e)
            except ValueError as e:
                print(get_error_message('Warning:', e))
            except TypeError as e:
                print(get_error_message('Warning:', e))

    del path[-1]

    return values


def process_command(cmd) -> tuple[any, str, bool]:
    c = cmd[0]
    if c not in operators.keys():
        return None, get_error_message(f'${c}', 'Commande non valide'), False

    c_keys = operators[c]['arg_keys']
    c_func = operators[c]['function']
    c_conv = operators[c]['convert']
    c_proc = operators[c]['opt_proc']

    if c_keys is not None:
        values = []

        while not values:
            values = get_entries(c_keys, cmd, c_conv)
            if c_proc is not None:
                retry, error = c_proc(values)
                if retry:
                    values.clear()
                    del cmd[:]
                    cmd.append(c)
                    print(get_error_message(error, f'\nNouvelle tentative > ${c}'))

        cmd_args, to_cache = values, True
    else:
        values, cmd_args, to_cache = None, [], False

    rslt = c_func(values)

    return rslt, ' '.join((f'${c}', ' '.join(map(str, cmd_args)))).rstrip(), to_cache


def process_input(string) -> tuple[any, str, bool]:
    if string.startswith('$'):
        rslt, cmd, to_cache = process_command(string.lstrip('$').split())

    elif not re.findall(r'[^0-9e%.()/+*_\- ]', string):
        rslt = None
        cmd = string
        to_cache = False

        try:
            rslt = float(eval(string))
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


def display_operators_list(*_args) -> str:
    doc = '\n'
    for key in operators.keys():
        op = operators[key]
        doc = ''.join((doc, f"${key}: {op['name']}\n"
                            f"\t{str(op['function']).split()[1]}({str(op['arg_keys']).strip('()')})\n"))
    print(doc)
    return 'Fin'


operators = nimp.commands
operators['\\'] = {
                    'name': 'Exit',
                    'function': sys.exit,
                    'convert': None,
                    'opt_proc': None,
                    'arg_keys': None
                    }
operators['h'] = {
                    'name': 'Aide',
                    'function': display_operators_list,
                    'convert': None,
                    'opt_proc': None,
                    'arg_keys': None
                    }

# ----------------------------------------------------------------------------------------------------------------------

calc_cache = []
path = []
print(f'Entrez directement des op??rations (ex: 11.2 + 4**3)\nou $h pour voir les commandes sp??ciales\n')

while True:
    print(f'cache -> {calc_cache}')
    result, command, send_to_cache = process_input(input(f'> ')[:256])

    print(f'{command} -> {result}')
    if send_to_cache:
        calc_cache.append(result)
