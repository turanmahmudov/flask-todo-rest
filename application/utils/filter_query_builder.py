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

                if operator == '=':
                    generated_filter = column.__eq__(matches.group(3))
                    print(matches.group(3))
                elif operator == '!=':
                    generated_filter = column.__ne__(matches.group(3))
                elif operator == '()':
                    generated_filter = column.in_(matches.group(3).split(','))
                elif operator == '>=':
                    generated_filter = column.__ge__(matches.group(3))
                elif operator == '<=':
                    generated_filter = column.__le__(matches.group(3))
                elif operator == '~':
                    generated_filter = column.like('%'+matches.group(3)+'%')
                elif operator == '>':
                    generated_filter = column.__gt__(matches.group(3))
                elif operator == '<':
                    generated_filter = column.__lt__(matches.group(3))

                if generated_filter is not None:
                    generated_filters.append(generated_filter)

    query = table.query.filter(*generated_filters)

    return query
