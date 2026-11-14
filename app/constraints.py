from app.store import finite_number


def evaluate(expression, values):
    return sum(finite_number(coefficient) * finite_number(values[key]) for key, coefficient in expression.items())


def violations(case, values):
    broken = []
    for key, (lower, upper) in case['bounds'].items():
        if not lower <= values[key] <= upper:
            broken.append('bound:' + key)
    for constraint in case['constraints']:
        value = evaluate(constraint['expression'], values)
        if not constraint['lower'] <= value <= constraint['upper']:
            broken.append(constraint['id'])
    return broken
