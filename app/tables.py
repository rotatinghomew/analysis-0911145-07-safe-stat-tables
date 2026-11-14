from collections import defaultdict
from app.archive import verify_archive
from app.constraints import evaluate, violations
from app.store import unique


def internal_tables(case):
    unique(case['cells'], 'id')
    if violations(case, case['variables']):
        raise ValueError('source totals violate business constraints')
    if verify_archive(case):
        raise ValueError('source values disagree with immutable archive')
    tables = defaultdict(list)
    for cell in case['cells']:
        actual = evaluate(cell['expression'], case['variables'])
        if abs(actual - cell['value']) > 1e-9:
            raise ValueError('cell formula does not match recorded value')
        tables[cell['table']].append(dict(cell))
    return dict(tables)


def preview(case):
    tables = internal_tables(case)
    return {'snapshot': case['_snapshot'], 'internal_only': True,
            'tables': tables, 'protected_count': len(case['protected']),
            'archive_count': len(case['archive'])}
