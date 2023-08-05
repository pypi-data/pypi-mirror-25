import unittest

from plagiarismdetector.tokenizer import TreebankWordTokenizer


class TestTokenizer(unittest.TestCase):

    def setUp(self):
        self.tokenizer = TreebankWordTokenizer()

    def tearDown(self):
        pass

    def test_tokenize(self):
        self.assertEqual(self.tokenizer.tokenize("run jog sprint"),
                         ["run", "jog", "sprint"])

    def test_tokenize_space(self):
        self.assertEqual(self.tokenizer.tokenize("  run   jog  sprint "),
                         ["run", "jog", "sprint"])

    def test_tokenize_punctuation(self):
        self.assertEqual(self.tokenizer.tokenize(", ,,run , ,, ,jog, ,sprint,,"),
                         [',', ',', ',run', ',', ',', ',', ',', 'jog', ',', ',', 'sprint', ',', ','])

    def test_tokenize_alphanumeric(self):
        self.assertEqual(self.tokenizer.tokenize("run jog342 sprint 370.97 "),
                         ['run', 'jog342', 'sprint', '370.97'])

    def test_tokenize_special_chars(self):
        self.assertEqual(self.tokenizer.tokenize("Good muffins cost $3.88\nin New York.  buy me\ntwo of them."),
                         ['Good', 'muffins', 'cost', '$', '3.88', 'in', 'New', 'York.', 'buy', 'me', 'two', 'of',
                          'them', '.'])

    def test_tokenize_alphanumeric_contractions(self):
        self.assertEqual(self.tokenizer.tokenize("hi, my name can't hello,"),
                         ['hi', ',', 'my', 'name', 'ca', "n't", 'hello', ','])


if __name__ == '__main__':
    unittest.main()

