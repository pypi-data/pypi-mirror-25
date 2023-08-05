from unittest import TestLoader, TextTestRunner, TestSuite
from test_detector import TestDetector
from test_tokenizer import TestTokenizer

if __name__ == "__main__":
    loader = TestLoader()
    suite = TestSuite((
        loader.loadTestsFromTestCase(TestDetector),
        loader.loadTestsFromTestCase(TestTokenizer),
    ))

    runner = TextTestRunner(verbosity=2)
    runner.run(suite)
