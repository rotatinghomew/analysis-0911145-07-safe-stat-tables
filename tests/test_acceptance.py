import json
import os
import threading
import unittest
from app.client import analysis
from app.server import make_server
from app.study_store import load_case


@unittest.skipUnless(os.environ.get('RUN_ACCEPTANCE') == '1', '分析消费接口尚未接入')
class AnalysisContractTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.server = make_server()
        cls.worker = threading.Thread(target=cls.server.serve_forever, daemon=True)
        cls.worker.start()
        cls.base = 'http://127.0.0.1:' + str(cls.server.server_port)

    @classmethod
    def tearDownClass(cls):
        cls.server.shutdown()
        cls.worker.join(timeout=3)
        cls.server.server_close()

    def test_consumer_contract_and_provenance(self):
        result = analysis(self.base)
        self.assertEqual(result['snapshot'], load_case('standard')['_snapshot'])
        for field in ['release', 'pooled', 'backtest', 'diagnostics']:
            self.assertIn(field, result)
        json.dumps(result, allow_nan=False)

    def test_information_limits_are_visible(self):
        result = analysis(self.base, 'edge')
        self.assertEqual(result['snapshot'], load_case('edge')['_snapshot'])
        self.assertTrue(result['diagnostics'])

    def test_copying_the_same_upstream_distribution_does_not_change_its_vote(self):
        original = analysis(self.base)['pooled']
        copied = analysis(self.base, 'edge')['pooled']
        self.assertEqual(original, copied)

    def test_future_truth_versions_cannot_improve_the_current_release(self):
        original = analysis(self.base)['pooled']
        future = analysis(self.base, 'future')['pooled']
        self.assertEqual(original, future)

    def test_pooled_probabilities_remain_a_distribution(self):
        for row in analysis(self.base)['pooled']:
            self.assertTrue(row['pmf'])
            self.assertAlmostEqual(sum(point[1] for point in row['pmf']), 1)
            self.assertTrue(all(point[0] >= 0 and 0 <= point[1] <= 1 for point in row['pmf']))
