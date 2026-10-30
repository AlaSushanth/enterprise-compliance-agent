"""
AEGIS-OPERATOR Test Runner
Executes all unit, RAG, guardrail, agent, and API tests using standard Python unittest.
"""
import sys
import os
import unittest

# Ensure project root is in path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from tests.test_parser import test_text_chunking
from tests.test_guardrails import test_guardrail_risk_policy_critical, test_guardrail_risk_policy_high, test_guardrail_grounding
from tests.test_rag import test_vector_store_initialization, test_hybrid_search_encryption, test_hybrid_search_sla
from tests.test_agents import test_multi_agent_pipeline_execution
from tests.test_api import test_health, test_sample, test_full_pipeline_flow

class TestAegisOperator(unittest.TestCase):
    def test_01_parser(self):
        test_text_chunking()

    def test_02_guardrail_critical(self):
        test_guardrail_risk_policy_critical()

    def test_03_guardrail_high(self):
        test_guardrail_risk_policy_high()

    def test_04_guardrail_grounding(self):
        test_guardrail_grounding()

    def test_05_vector_store_init(self):
        test_vector_store_initialization()

    def test_06_hybrid_search_encryption(self):
        test_hybrid_search_encryption()

    def test_07_hybrid_search_sla(self):
        test_hybrid_search_sla()

    def test_08_multi_agent_pipeline(self):
        test_multi_agent_pipeline_execution()

    def test_09_api_health(self):
        test_health()

    def test_10_api_sample(self):
        test_sample()

    def test_11_api_full_flow(self):
        test_full_pipeline_flow()

if __name__ == "__main__":
    print("=" * 70)
    print("  RUNNING AEGIS-OPERATOR TEST SUITE (11 TESTS)")
    print("=" * 70)
    suite = unittest.TestLoader().loadTestsFromTestCase(TestAegisOperator)
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    if result.wasSuccessful():
        print("\n[SUCCESS] All 11 tests passed with 100% compliance!")
        sys.exit(0)
    else:
        print("\n[FAILED] One or more tests failed.")
        sys.exit(1)
