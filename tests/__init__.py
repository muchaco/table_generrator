import string


def generate_test_rules(size, with_default_rows):
    keys = string.ascii_lowercase[:size]
    values = list(range(1, size + 1))

    latin_square_rules = {
        'columns': {i: values for i in keys},
        'rules': {
            'row-rules': [
                '[{}].count({}) == 1'.format(', '.join(keys), i)
                for i in values
            ],
            'count-rules': [
                {
                    'min': 1,
                    'max': 1,
                    'expression': '{} == {}'.format(i, j)
                }
                for i in keys
                for j in values
            ]
        }
    }

    if with_default_rows:
        latin_square_rules['default-rows'] = generate_default_rows(size)[:-1]

    return latin_square_rules


def generate_default_rows(n):
    """
    returning n rows that are properly constructed for the generated rules
    """
    rows = []

    for i in range(n):
        raw_row = [
            j % n + 1
            for j in range(i, n + i)
        ]
        row = {
            string.ascii_lowercase[i]: raw_row[i]
            for i in range(0, n)
        }
        rows.append(row)

    return rows
