from distutils import util as dist_util
import re

from flask_sqlalchemy import orm


def filter_query_builder(table, filter_str):
    if not filter_str:
        return table.query

    regex = r"([a-zA-Z0-9]+)(=|!=|\(\)|>=|<=|~|>|<)([a-zA-Z0-9 ]+)"

    filters = filter_str.split(';')

    generated_filters = []

    for filter_item in filters:
        generated_filter = None
        if filter_item:
            matches = re.search(regex, filter_item, re.IGNORECASE)
            if matches:
                mapper = orm.class_mapper(table)
                if not hasattr(mapper.columns, matches.group(1)):
                    continue

                column = mapper.columns[matches.group(1)]

                operator = matches.group(2)
                val = matches.group(3)

                if operator == '=':
                    if val == "true" or val == "false":
                        val = dist_util.strtobool(val)
                        generated_filter = column.is_(bool(val))
                    else:
                        generated_filter = column.__eq__(val)
                elif operator == '!=':
                    if val == "true" or val == "false":
                        val = dist_util.strtobool(val)
                        generated_filter = column.is_not(bool(val))
                    else:
                        generated_filter = column.__ne__(val)
                elif operator == '()':
                    generated_filter = column.in_(val.split(','))
                elif operator == '>=':
                    generated_filter = column.__ge__(val)
                elif operator == '<=':
                    generated_filter = column.__le__(val)
                elif operator == '~':
                    generated_filter = column.like(val)
                elif operator == '>':
                    generated_filter = column.__gt__(val)
                elif operator == '<':
                    generated_filter = column.__lt__(val)

                if generated_filter is not None:
                    generated_filters.append(generated_filter)

    query = table.query.filter(*generated_filters)

    return query
