import os
import unittest

from plagiarismdetector.detector import Detector


class TestDetector(unittest.TestCase):
    TEST_DATA_DIR_NAME = "test_data"
    TEST_SYNONYM_FILE_NAME = "syn_file"
    TEST_SYNONYM_FILE_VALUE = "run jog sprint"
    TEST_EVAL_FILE_NAME = "eval_file"
    TEST_EVAL_FILE_VALUE = "go for a run"
    TEST_SOURCE_FILE_NAME = "src_file"
    TEST_SOURCE_FILE_VALUE = "went for a jog"
    TEST_N_TUPLES_VALUE = 3

    def setUp(self):
        if not os.path.exists(self.TEST_DATA_DIR_NAME):
            os.makedirs(self.TEST_DATA_DIR_NAME)

        args = {self.TEST_SYNONYM_FILE_NAME: self.TEST_SYNONYM_FILE_VALUE,
                self.TEST_EVAL_FILE_NAME: self.TEST_EVAL_FILE_VALUE,
                self.TEST_SOURCE_FILE_NAME: self.TEST_SOURCE_FILE_VALUE}

        for file_path in args.keys():
            with open(os.path.join(self.TEST_DATA_DIR_NAME, file_path), "w") as test_file:
                test_file.write(args[file_path])

        self.detector = Detector(os.path.join(self.TEST_DATA_DIR_NAME, self.TEST_SYNONYM_FILE_NAME),
                                 os.path.join(self.TEST_DATA_DIR_NAME, self.TEST_EVAL_FILE_NAME),
                                 os.path.join(self.TEST_DATA_DIR_NAME, self.TEST_SOURCE_FILE_NAME),
                                 self.TEST_N_TUPLES_VALUE)

    def tearDown(self):
        for i in os.listdir(self.TEST_DATA_DIR_NAME):
            os.remove(os.path.join(self.TEST_DATA_DIR_NAME, i))
        os.rmdir(self.TEST_DATA_DIR_NAME)

    def test_detector(self):
        self.assertEqual(self.detector.detect(), 50.0)

    def test_generate_ngrams(self):
        tokens = ("go", "for", "a")
        self.assertEqual(self.detector.generate_ngrams(tokens), hash(tokens))

    def test_open_file_and_tokenize_for_grams(self):
        self.detector.open_file_and_tokenize()
        f2_grams = {hash(("went", "for", "a")): None, hash(("for", "a", 1916106794)): None}
        self.assertEqual(self.detector.f2_grams, f2_grams)

    def test_open_file_and_tokenize_for_unique_counts(self):
        self.detector.open_file_and_tokenize(count_unique=True)
        self.assertEqual(self.detector.f1_f2_common_tuples_count, 1)


if __name__ == '__main__':
    unittest.main()
