from table_generator.Generator import Generator
from . import generate_test_rules, generate_default_rows


def test_duplicate_criteria():
    rules = generate_test_rules(size=3, with_default_rows=True)
    generator = Generator(rules, debug_level=0)
    test_input = [
        {'a': 1, 'b': 2, 'c': 3},
        {'a': 2, 'b': 3, 'c': 1},
        {'a': 3, 'b': 1, 'c': 2},
    ]

    assert generator.duplicate_criteria(test_input[0])
    assert generator.get_stat('duplicate_found') == 1

    assert generator.duplicate_criteria(test_input[1])
    assert generator.get_stat('duplicate_found') == 2

    assert not generator.duplicate_criteria(test_input[2])
    assert generator.get_stat('duplicate_found') == 2


def test_generate_random_row():
    rules = generate_test_rules(size=3, with_default_rows=True)
    generator = Generator(rules, debug_level=0)
    row = generator.generate_random_row()

    assert isinstance(row, dict)
    for k in rules['default-rows'][0].keys():
        assert k in row.keys()
    assert len(row.keys()) == len(rules['default-rows'][0].keys())


def test_drop_criteria():
    table_size = 5
    rules = generate_test_rules(size=table_size, with_default_rows=False)
    generator = Generator(rules, debug_level=0)
    proper_rows = generate_default_rows(table_size)

    for i in range(4):  # drop criteria works only >4 tables
        generator.append_row(proper_rows[i])
        assert not generator.drop_criteria()

    generator.append_row(proper_rows[4])

    for _ in range(5 ** 3 - 1):  # drop criteria works if iteration_in_state >= table_len**3
        generator.fit_criteria(proper_rows[0])
        assert not generator.drop_criteria()

    generator.fit_criteria(proper_rows[0])
    assert generator.drop_criteria()

    assert generator.stat_generated_table_len == table_size


def test_end_criteria():
    rules = generate_test_rules(size=3, with_default_rows=True)
    generator = Generator(rules, debug_level=0)
    last_row = {'a': 3, 'b': 1, 'c': 2}

    assert generator.get_stat('all_iteration') == 0

    assert not generator.end_criteria()
    assert generator.get_stat('all_iteration') == 1

    generator.append_row(last_row)
    assert generator.end_criteria()
    assert generator.get_stat('all_iteration') == 1


def test_fit_criteria():
    rules = generate_test_rules(size=3, with_default_rows=False)
    generator = Generator(rules, debug_level=0)

    test_input = [
        {'a': 1, 'b': 2, 'c': 3},
        {'a': 1, 'b': 3, 'c': 2},
        {'a': 2, 'b': 1, 'c': 3},
        {'a': 2, 'b': 3, 'c': 1},
        {'a': 3, 'b': 1, 'c': 2},
        {'a': 3, 'b': 2, 'c': 1},
    ]

    assert generator.get_stat('iteration_in_state') == 0
    assert generator.get_stat('added_rows') == 0

    assert generator.fit_criteria(test_input[0])
    assert generator.get_stat('iteration_in_state') == 0
    generator.append_row(test_input[0])
    assert generator.get_stat('added_rows') == 1
    assert not generator.fit_criteria(test_input[0])
    assert generator.get_stat('iteration_in_state') == 1

    assert not generator.fit_criteria(test_input[1])
    assert generator.get_stat('iteration_in_state') == 2
    assert not generator.fit_criteria(test_input[2])
    assert generator.get_stat('iteration_in_state') == 3

    assert generator.fit_criteria(test_input[3])
    generator.append_row(test_input[3])
    assert generator.get_stat('iteration_in_state') == 0
    assert generator.get_stat('added_rows') == 2
    assert not generator.fit_criteria(test_input[3])
    assert generator.get_stat('iteration_in_state') == 1

    assert generator.fit_criteria(test_input[4])
    generator.append_row(test_input[4])
    assert generator.get_stat('iteration_in_state') == 0
    assert generator.get_stat('added_rows') == 3
    assert not generator.fit_criteria(test_input[4])
    assert generator.get_stat('iteration_in_state') == 1

    assert not generator.fit_criteria(test_input[5])
    assert generator.get_stat('iteration_in_state') == 2


def test_proper_criteria():
    rules = generate_test_rules(size=3, with_default_rows=True)
    generator = Generator(rules, debug_level=0)
    test_input = [
        {'a': 1, 'b': 2, 'c': 3},
        {'a': 1, 'b': 3, 'c': 2},
        {'a': 2, 'b': 1, 'c': 3},
        {'a': 2, 'b': 3, 'c': 1},
        {'a': 3, 'b': 1, 'c': 2},
        {'a': 3, 'b': 2, 'c': 1},
    ]

    assert generator.get_stat('iteration_in_state') == 0

    for test_row in test_input:
        assert generator.proper_criteria(test_row)
        assert generator.get_stat('iteration_in_state') == 0

    test_input = [
        {'a': 1, 'b': 1, 'c': 3},
        {'a': 3, 'b': 1, 'c': 3},
        {'a': 2, 'b': 2, 'c': 2},
    ]

    count = 0
    assert generator.get_stat('iteration_in_state') == count

    for test_row in test_input:
        assert not generator.proper_criteria(test_row)
        count += 1
        assert generator.get_stat('iteration_in_state') == count
