from tokenizer import TreebankWordTokenizer


class Detector:
    """Calculates percentage of N-Tuples from file1 found in another file2

    Usage::

        >>> from plagiarismdetector.detector import Detector
        >>> synonym_file = 'synonym.txt'
        >>> file1 = 'file1.txt'
        >>> file2 = 'file2.txt'
        >>> n = 6 # Optional
        >>> Detector.detect(synonym_file, file1, file2, n)

    :param str synonym_file_path: Path for synonyms files
    :param str file1_path: Path for file 1
    :param str file2_path: Path for file 2
    :param int n: Number of tuples (Optional, Defaults to 3)
    :return Percentage of N-tuples found from file1 in file2
    :rtype: float
    """
    synonyms = {}
    f2_grams = {}
    f1_f2_common_tuples_count = 0
    tokenizer = TreebankWordTokenizer()

    def __init__(self, synonym_file_path, file1_path, file2_path, n=3):
        self.syn = synonym_file_path
        self.f1 = file1_path
        self.f2 = file2_path
        self.n = n

    """ Loads synonyms from the synonyms file into a dictionary
        All words that are synonym of each other point to a unique hash
        e.g. run jog sprint
        synonyms = { 'run': 15232132, 'jog': 15232132, 'sprint': 15232132 }
    """
    def load_synonyms(self):
        with open(self.syn, 'r') as synonyms_file:
            for synonym in synonyms_file.readlines():
                words = tuple(synonym.rstrip("\n").split(" "))
                unique_hash = hash(words)
                for word in words:
                    self.synonyms[word] = unique_hash

    """ Generates n grams from input string starting index i
    :param list of str tokens: list of words to generate n grams from tokens
    :return hash of n-tuple so as to reduce space complexity 
            and still get the benefits of constant time key lookup
    :rtype: int
    """
    def generate_ngrams(self, tokens):
        return hash(tuple([self.synonyms.get(x, x) for x in tokens]))

    """ 1. Opens up a file
        2. Tokenize it's contents 
        3. Count unique nodes of source file in evaluation file
        4. Builds a list of n grams from source file
    :param boolean count_unique: decide whether to generate grams or count unique nodes  
                                 found in evaluation file from source file
    """
    def open_file_and_tokenize(self, count_unique=False):
        file_path = self.f1 if count_unique else self.f2
        with open(file_path, 'r') as f:
            tokens = self.tokenizer.tokenize(f.read())
            for i in range(len(tokens) - self.n + 1):
                if count_unique:
                    if self.generate_ngrams(tokens[i:i + self.n]) in self.f2_grams:
                        self.f1_f2_common_tuples_count += 1
                else:
                    self.f2_grams[self.generate_ngrams(tokens[i:i + self.n])] = None

    """ Calculates the percentage of N-tuples in evaluation file inside source file 
    :rtype float
    """
    def detect(self):
        self.load_synonyms()
        self.open_file_and_tokenize()
        self.open_file_and_tokenize(count_unique=True)

        if self.f1_f2_common_tuples_count > 0:
            return float(self.f1_f2_common_tuples_count) / len(self.f2_grams) * 100
        else:
            return 0.
