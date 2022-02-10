# Table Generator

This script is designed to generate two dimensional tables from a predefined ruleset as an input.

## Rules

Rules should be written in JSON or YAML format in the following structure:

```yaml
{
    "columns": {...},
    "rules": {
        "row-rules": [
            ...
        ],
        "count-rules": [
            ...
        ]
    },
    "default-rows": [
        ...
    ]
}

```

*columns*: Contains key-value pairs. The key will be used in the rule descriptions, and the value part contains a list
with the possible values. The rules and default-rows should contain exactly these columns.

*row_rules*: List of strings. Every string must contain a python evaluable boolean expression with a potential row from
the generated table. The row's columns can be accessed my the column's name. The expression should return True only
if the columns combine a valid row for the table.

A row is valid if and only if every rule in this list accepts it as valid.

*count_rules*: List of dictionaries, with the following mandatory keys: `min`, `max`, `expression`. Expression is a string
that contains a python evaulable boolean expression with a potential row from the generated table. The row's columns can be
accessed my the column's name.
Min and max should contain integers representing that for how many rows should the expression return true in the final
matrix.

*default_rows*: List of dictionaries where every item of the list is a valid row for the final table, but will be
certainly used.

You can define other parts in the yaml (or json), and access them from the expressions with `self` variable. E.g. the first default
row can be accessed from any defined expression with `self['default-rows'][0]`.

## Usage

**Install requirements**

`pip install -r requirements.txt`

**Print help**

`python3 -m table_generator --help`

**Run unit tests**

`pytest`

**Generate table**

`python3 -m table_generator -i <input_yaml> -o <output_csv>`

With debug logging:

`python3 -m table_generator -i <input_yaml> -o <output_csv> -d <debug_level>`

where debug_level means throughout generation process how many times do we want to print the current status. Should be
bewteen 1 and 10000. 1 means status will be printed after every 10000th row that was tried for fitting. 10000 means that
after every try the status will be printed. Large debug level slows down the generation.

Debug level is handy for determining if the rules are impossible to be applied.

*ctrl+c* will print the last state of the table where every *row-rules* are guaranteed to be applied, and every *max*
number is applied from the *count-rules*, but *min* has not reached yet.
