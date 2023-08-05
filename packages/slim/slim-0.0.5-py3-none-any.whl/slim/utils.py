import re
import math
import time
import binascii

_valid_sql_operator = {
    '=': '=',
    '==': '=',
    '!=': '!=',
    '<>': '<>',
    '<': '<',
    '<=': '<=',
    '>': '>',
    '>=': '>=',
    'eq': '=',
    'ne': '!=',
    'ge': '>=',
    'gt': '>',
    'le': '<=',
    'lt': '<',
    'in': 'in',
    'is': 'is',
    'isnot': 'isnot',
}

RegexPatternType = type(re.compile(''))


def dict_filter(obj, keys):
    return {k: v for k, v in obj.items() if k in keys}


# noinspection PyUnresolvedReferences
class _MetaClassForInit(type):
    def __new__(mcs, *args, **kwargs):
        new_class = super().__new__(mcs, *args, **kwargs)
        new_class.cls_init()
        return new_class


class ResourceException(Exception):
    pass

to_hex = lambda x: str(binascii.hexlify(x), 'utf-8')
to_bin = lambda x: binascii.unhexlify(bytes(x, 'utf-8'))


def time_readable():
    x = time.localtime(time.time())
    return time.strftime('%Y-%m-%d %H:%M:%S', x)


def pagination_calc(count_all, page_size, cur_page=1, nearby=2):
    """
    :param nearby:
    :param count_all: count of all items
    :param page_size: size of one page
    :param cur_page: current page number, accept string digit
    :return: num of pages, an iterator
    """
    if type(cur_page) == str:
        # noinspection PyUnresolvedReferences
        cur_page = int(cur_page) if cur_page.isdigit() else 1
    elif type(cur_page) == int:
        if cur_page <= 0:
            cur_page = 1
    else:
        cur_page = 1

    page_count = int(math.ceil(count_all / page_size))
    items_length = nearby * 2 + 1

    # if first page in page items, first_page is None,
    # it means the "go to first page" button should not be available.
    first_page = None
    last_page = None

    prev_page = cur_page - 1 if cur_page != 1 else None
    next_page = cur_page + 1 if cur_page != page_count else None

    if page_count <= items_length:
        items = range(1, page_count + 1)
    elif cur_page <= nearby:
        # start of items
        items = range(1, items_length + 1)
        last_page = True
    elif cur_page >= page_count - nearby:
        # end of items
        items = range(page_count - items_length + 1, page_count + 1)
        first_page = True
    else:
        items = range(cur_page - nearby, cur_page + nearby + 1)
        first_page, last_page = True, True

    if first_page:
        first_page = 1
    if last_page:
        last_page = page_count

    return {
        'cur_page': cur_page,
        'prev_page': prev_page,
        'next_page': next_page,

        'first_page': first_page,
        'last_page': last_page,

        'page_numbers': list(items),
        'page_count': page_count,

        'info': {
            'page_size': page_size,
            'count_all': count_all,
        }
    }


def async_run(func):
    loop = asyncio.get_event_loop()
    loop.run_until_complete(func())
