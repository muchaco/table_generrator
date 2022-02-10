import yaml
import os
import tempfile
import uuid

from table_generator import file_ops
from . import generate_test_rules


def test_read_yaml_file():
    test_file = tempfile.NamedTemporaryFile(delete=False)
    rules = generate_test_rules(size=3, with_default_rows=True)

    with open(test_file.name, 'w') as outfile:
        yaml.dump(rules, outfile)

    readed_yaml = file_ops.read_yaml_file(test_file.name)

    assert readed_yaml == rules

    os.unlink(test_file.name)


def test_read_nonexistent_yaml_file():
    test_file = '/tmp/{}'.format(uuid.uuid4())

    try:
        file_ops.read_yaml_file(test_file)
    except IOError as e:
        assert e.args[0] == "Specified input file ({}) does not exist".format(test_file)
    else:
        assert False


def test_write_csv_file():
    test_file = tempfile.NamedTemporaryFile(delete=False)
    test_input = [
        {'a': 1, 'b': 2, 'c': 3},
        {'a': 2, 'b': 3, 'c': 1},
        {'a': 3, 'b': 1, 'c': 2},
    ]
    test_output = (
        'a\tb\tc\n' +
        '1\t2\t3\n' +
        '2\t3\t1\n' +
        '3\t1\t2\n'
    )
    file_ops.write_csv_file(test_file.name, test_input)

    with open(test_file.name, 'r') as test_file:
        assert test_file.read() == test_output

    os.unlink(test_file.name)
