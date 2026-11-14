import math
from app.study_schema import rows_by_id, probability


def validate(case):
    products = rows_by_id(case['products'])
    for prediction in case['predictions']:
        if prediction['product'] not in products:
            raise ValueError('未知预测产品')
        if prediction['issued_at'] > prediction['origin'] or prediction['target'] <= prediction['origin']:
            raise ValueError('预测时间不合法')
        if prediction['unit'] != 'boxes':
            raise ValueError('预测单位不可直接混用')
        outcomes = [point[0] for point in prediction['pmf']]
        if not outcomes or len(set(outcomes)) != len(outcomes) or any(point < 0 for point in outcomes):
            raise ValueError('离散分布支持集无效')
        total = sum(probability(point[1]) for point in prediction['pmf'])
        if not math.isclose(total, 1, abs_tol=1e-9):
            raise ValueError('预测概率和不为一')
    return products


def visible_predictions(case, cutoff):
    validate(case)
    latest = {}
    for prediction in case['predictions']:
        if prediction['known_at'] > cutoff:
            continue
        key = (prediction['product'], prediction['origin'], prediction['target'])
        if key not in latest or prediction['revision'] > latest[key]['revision']:
            latest[key] = prediction
    return list(latest.values())


def preview(case):
    products = validate(case)
    predictions = visible_predictions(case, case['as_of'])
    return {'snapshot': case['_snapshot'], 'products': list(products),
            'source_lineage': {key: value['sources'] for key, value in products.items()},
            'prediction_count': len(predictions), 'truth_visible': sum(row['known_at'] <= case['as_of'] for row in case['truth']),
            'descriptive_only': True}
