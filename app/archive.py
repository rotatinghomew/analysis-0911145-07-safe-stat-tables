from app.constraints import evaluate


def verify_archive(case):
    errors = []
    for row in case['archive']:
        if abs(evaluate(row['expression'], case['variables']) - row['value']) > 1e-9:
            errors.append(row['id'])
    return errors
