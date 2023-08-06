import pandas as pd
from datetime import datetime, timedelta


def explore(obj):
    print('='*100)
    print(obj)
    print(obj.__class__)
    print(*dir(obj), sep='\n')


def repr_dict(d, offset=4):
    out = ''
    for k, v in sorted(d.items()):
        out += (' ' * offset)+'%s: %s\n' % (k, v)
    return out


def print_horizontal_ruller(label, margin_top=1, margin_bottom=1):
    hr = ('=' * 73)
    insert = ' %s ' % label
    print('\n'*margin_top, hr[:4]+insert+hr[4+len(insert):], '\n'*margin_bottom, sep='')


def print_response(response):
    print_horizontal_ruller('Begin', margin_bottom=0)
    print(datetime.now().strftime('[%d.%m.%Y %H:%M:%S]'), '\n')

    print('Request:', response.request.method, response.request.url)
    # print('Request data:', response.request.body)
    print('Request data:', unquote(response.request.body or ''))
    print('\nRequest headers:', '\n', repr_dict(response.request.headers), sep='')
    print('\nResponse status code:', response.status_code)
    print('Response headers:', '\n', repr_dict(response.headers), sep='')
    # print('\nSession cookies', session.cookies)
    print('\nResponse history:', response.history)
    # print('\nResponse content:', '\n', response.content.decode() if isinstance(response.content, bytes) else response.content)
    for history_response in response.history:
        print(' '*3, history_response.request.method, history_response.status_code, history_response.url)
        print(' '*3, history_response.request)
        print('\n', ' '*4, 'History request headers:', sep='')
        print(repr_dict(history_response.request.headers, 8))
        print('\n', ' '*4, 'History response headers:', sep='')
        print(repr_dict(history_response.headers, 8))
        print('\n', ' '*4, 'History response content: ', history_response.content, sep='')
        if len(response.history) > 1:
            print(' '*3, '='*32)

    print_horizontal_ruller('End')


def print_df(data_frame):
    if data_frame.empty:
        print(data_frame)
        return


    def stringify_value(value):
        str_value = str(value)

        if str_value == 'NaT':
            str_value = ''
        else:
            if isinstance(value, datetime):
                str_value = value.strftime('%d.%m.%Y %H:%M:%S')
            elif isinstance(value, timedelta):
                str_value = str(value).split('.')[0]

        return str_value


    df = data_frame.copy()
    df.insert(0, u'', df.index)
    sep = ' | '

    for col_name in df.columns.values:
        df[col_name] = df[col_name].apply(lambda x: stringify_value(x))

    col_maxs = {col_name: df[col_name].astype(str).str.len().max() for col_name in df.columns.values}
    headers = {col_name: str(col_name) + ' ' * int(col_maxs[col_name] - len(str(col_name))) for col_name in df.columns.values}


    def formatter(row):
        values = []

        for col_index, value in enumerate(row.values):
            col_name = df.columns[col_index]
            value = value + ' ' * (len(headers[col_name]) - len(value))
            values.append(value)

        print(*values, sep=sep)


    print('—' * len(sep.join(headers.values())))
    print(*headers.values(), sep=sep)
    df.apply(formatter, axis=1)


def colored_print(*args, color=None, style=0, sep=' ', end=None, nl=False):
    color_map = {
        'black': 30,
        'white': 97,
        'red': 91,
        'red_dark': 31,
        'green': 92,
        'green_dark': 32,
        'blue': 94,
        'blue_dark': 34,
        'gray': 37,
        'gray_dark': 90,
        'yellow': 93,
        'yellow_dark': 33,
        'magenta': 95,
        'magenta_dark': 35,
        'cyan': 96,
        'cyan_dark': 36,
    }

    color = color_map[color] if color in color_map else 92
    nl = '\n' if nl else ''

    print('\033[{};{}m'.format(style, color)+nl+sep.join([str(a) for a in args])+'\033[0m', end=end)


def print_with_timestamp(*args, sep=' ', nl=False):
    colored_print('[%s]' % datetime.now().strftime('%d.%m.%Y %H:%M:%S'), color='green_dark', sep=sep, end=' ', nl=nl)
    print(*args, sep=sep)