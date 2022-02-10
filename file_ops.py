import csv
import yaml
import os


def read_yaml_file(filename):
    if not os.path.isfile(filename):
        raise IOError("Specified input file ({}) does not exist".format(filename))

    with open(filename) as f_in:
        return yaml.safe_load(f_in)


def write_csv_file(filename, data):
    with open(filename, 'w') as cs_file:
        fieldnames = list(data[0].keys())
        writer = csv.DictWriter(cs_file, fieldnames=fieldnames, delimiter='\t')
        writer.writeheader()
        for i in data:
            i = {k: v if v is not None else '-' for k, v in i.items()}
            writer.writerow(i)
