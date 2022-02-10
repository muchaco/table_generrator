from math import ceil
from operator import xor
import random
import sys


def exception_handling(fn):
    def decorated_func(*args, **kwargs):
        generator = args[0]
        try:
            fn(*args, **kwargs)
        except KeyboardInterrupt:
            generator.stat_printer(force=True)
            print("Interrupted! Already generated table rows are dumped to the output file.", file=sys.stderr)
        except Exception as e:
            generator.stat_printer(force=True)
            raise e
        else:
            generator.stat_printer(force=True)
        finally:
            return

    return decorated_func


class Generator:
    def __init__(self, descriptor, debug_level):
        self.__descriptor = descriptor
        self.__debug_level = debug_level
        self.__table_changed = False

        lambda_namespace = {
            'self': descriptor,
            'xor': xor
        }

        for i in range(len(descriptor['rules']['row-rules'])):
            self.__descriptor['rules']['row-rules'][i] = eval(
                'lambda {}: {}'.format(
                    ', '.join(descriptor['columns'].keys()),
                    descriptor['rules']['row-rules'][i]
                ),
                lambda_namespace
            )

        for i in range(len(descriptor['rules']['count-rules'])):
            self.__descriptor['rules']['count-rules'][i]['expression'] = eval(
                'lambda {}: {}'.format(
                    ', '.join(descriptor['columns'].keys()),
                    descriptor['rules']['count-rules'][i]['expression']
                ),
                lambda_namespace
            )

        if 'default-rows' not in descriptor:
            self.__descriptor['default-rows'] = []

        self.__stats = {
            'dropped_rows': 0,
            'added_rows': 0,
            'duplicate_found': 0,
            'iteration_in_state': 0,
            'all_iteration': 0,
        }

        self.__generated_table = []

    def get_stat(self, stat):
        return self.__stats[stat]

    @property
    def stat_generated_table_len(self):
        return len(self.__generated_table)

    @property
    def stat_table_len(self):
        return self.stat_generated_table_len + len(self.__descriptor['default-rows'])

    def stat_printer(self, force=False):
        if (
            force or
                self.__debug_level != 0 and
                self.__stats['all_iteration'] % ceil(10000 / self.__debug_level) == 0
        ):
            stat_line = (
                'generated: {:2d}, '
                'sum: {:2d}, '
                'dropped: {:3d}, '
                'added: {:3d}, '
                'duplicate: {:3d}, '
                'iteration: {:4d}, '
                'all_iteration: {:5d}'.format(
                    self.stat_generated_table_len,
                    self.stat_table_len,
                    self.get_stat('dropped_rows'),
                    self.get_stat('added_rows'),
                    self.get_stat('duplicate_found'),
                    self.get_stat('iteration_in_state'),
                    self.get_stat('all_iteration'))
            )

            end = '\n' if force else '\r'
            print(stat_line, end=end)

    @exception_handling
    def generate_table(self):
        while not self.end_criteria():
            if self.drop_criteria():
                self.drop_random()

            row_candidate = self.generate_random_row()

            if (
                self.duplicate_criteria(row_candidate) or
                    not self.proper_criteria(row_candidate) or
                    not self.fit_criteria(row_candidate)
            ):
                continue
            else:
                self.append_row(row_candidate)

    def end_criteria(self):
        self.stat_printer()

        if not self.__table_changed:
            self.__stats['all_iteration'] += 1

            return False

        self.__table_changed = False

        tmp_table = self.__generated_table + self.__descriptor['default-rows']
        for rule in self.__descriptor['rules']['count-rules']:
            if rule['min'] > len([i for i in tmp_table if rule['expression'](**i)]):
                self.__stats['all_iteration'] += 1

                return False
        else:
            return True

    def drop_criteria(self):
        if self.stat_generated_table_len < 5:
            return False

        elif self.__stats['iteration_in_state'] < self.stat_generated_table_len ** 3:
            return False

        return True

    def drop_random(self):
        random_index = random.randrange(len(self.__generated_table))
        self.__generated_table.pop(random_index)
        self.__stats['iteration_in_state'] = 0
        self.__stats['dropped_rows'] += 1
        self.__table_changed = True

    def generate_random_row(self):
        row_candidate = {}
        for k, v in self.__descriptor['columns'].items():
            row_candidate[k] = random.choice(v)

        return row_candidate

    def duplicate_criteria(self, row_candidate):
        if row_candidate in self.__generated_table or \
                row_candidate in self.__descriptor['default-rows']:
            self.__stats['iteration_in_state'] += 1
            self.__stats['duplicate_found'] += 1

            return True

        return False

    def proper_criteria(self, row_candidate):
        for rule in self.__descriptor['rules']['row-rules']:
            if not rule(**row_candidate):
                self.__stats['iteration_in_state'] += 1
                return False

        return True

    def fit_criteria(self, row_candidate):
        tmp_table = self.__generated_table + self.__descriptor['default-rows'] + [row_candidate]

        for rule in self.__descriptor['rules']['count-rules']:
            if rule['max'] < len([i for i in tmp_table if rule['expression'](**i)]):
                self.__stats['iteration_in_state'] += 1
                return False

        return True

    def append_row(self, row_candidate):
        self.__generated_table.append(row_candidate)
        self.__stats['iteration_in_state'] = 0
        self.__stats['added_rows'] += 1
        self.__table_changed = True

    def get_table(self):
        return self.__generated_table + self.__descriptor['default-rows']
