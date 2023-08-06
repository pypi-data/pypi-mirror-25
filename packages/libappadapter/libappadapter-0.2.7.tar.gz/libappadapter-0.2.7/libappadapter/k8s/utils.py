import re


class Enum(set):
    def __getattr__(self, name):
        if name in self:
            return name
        raise AttributeError


def _match_amount(unitstr):
    if isinstance(unitstr, float):
        return unitstr, None
    if isinstance(unitstr, int):
        return unitstr, None
    if isinstance(unitstr, unicode):
        unitstr = unitstr.encode('ascii')
    amount = float(0)

    regInt = '^0$|^[1-9]\d*'
    regFloat = '^0\.\d+|^[1-9]\d*\.\d+'
    regIntOrFloat = regFloat + '|' + regInt
    patternIntOrFloat = re.compile(regIntOrFloat)
    unit = patternIntOrFloat.split(unitstr)
    amountObj = patternIntOrFloat.search(unitstr)
    if amountObj is not None:
        amount = float(amountObj.group(0))

    return amount, unit


def _format_float(amount):
    if float(int(amount)) == amount:
        return int(amount)
    return round(amount, 2)


def _format_unit(amount, unit_level, max_level):
    while amount >= 1024 and unit_level < max_level:
        amount /= 1024
        unit_level += 1
    while amount < 1 < unit_level:
        amount *= 1024
        unit_level -= 1

    return amount, unit_level


def amount_to_float(unitstr):
    amount, unit = _match_amount(unitstr)

    if unit and len(unit) == 2:
        if unit[1] == 'm':
            amount /= 1000
        elif unit[1].lower() in ['m', 'mi', 'mb']:
            amount *= 1024 * 1024
        elif unit[1].lower() in ['k', 'ki', 'kb']:
            amount *= 1024
        elif unit[1].lower() in ['g', 'gi', 'gb']:
            amount *= 1024 * 1024 * 1024
        elif unit[1].lower() in ['t', 'ti', 'tb']:
            amount *= 1024 * 1024 * 1024 * 1024
        elif unit[1].lower() in ['p', 'pi', 'pb']:
            amount *= 1024 * 1024 * 1024 * 1024 * 1024

    return amount


def format_amount(unitstr):
    """
    Format amount for cpu cores and mem/disk storage
    :param unitstr:
    :return:
    """
    amount, unit = _match_amount(unitstr)

    if unit and len(unit) == 2:
        if unit[1] == 'm':
            return str(_format_float(amount/1000))

        unit_hierarchy = ['B', 'KB', 'MB', 'GB', 'TB']
        validunit = ['m', 'ki', 'k', 'mi', 'g', 'gi']

        unit_1 = unit[1].lower()
        if unit_1 in validunit:
            unit_level = 0
            if unit_1 in ['m', 'mi']:
                unit_level = unit_hierarchy.index('MB')
            elif unit_1 in ['k', 'ki']:
                unit_level = unit_hierarchy.index('KB')
            elif unit_1 in ['g', 'gi']:
                unit_level = unit_hierarchy.index('GB')
            elif unit_1 in ['t', 'ti']:
                unit_level = unit_hierarchy.index('TB')

            amount, unit_level = _format_unit(amount, unit_level + 1, len(unit_hierarchy))
            return str(_format_float(amount)) + unit_hierarchy[unit_level - 1]
        else:
            return str(_format_float(amount)) + unit[1]

    return str(_format_float(amount))


def get_nested_field(obj, nested_field):
    """ Extract data from nested python objects.

    For example with object {1: 'a', 2: {3: 'c'}}, we use
        get_nested_field(a, [1, 2, 3])
    to extract field data 'c'.

    :param obj: a python object as dict
    :param nested_field: a list of nested field sequence
    :return: value or None
    """
    res = None
    intermediate = {}
    for field in nested_field:
        intermediate = obj.get(field, {})
    if not (isinstance(intermediate, dict) and len(intermediate) == 0):
        res = intermediate
    return res
