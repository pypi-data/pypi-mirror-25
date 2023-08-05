import re


class TreebankWordTokenizer:
    """
    The Treebank tokenizer uses regular expressions to tokenize text as in Penn Treebank.
    This is the method that is invoked by ``tokenize()``.

    This tokenizer performs the following steps:

    - split standard contractions, e.g. ``don't`` -> ``do n't`` and ``they'll`` -> ``they 'll``
    - treat most punctuation characters as separate tokens
    - split off commas and single quotes, when followed by whitespace
    - separate periods that appear at the end of line

        >>> from plagiarismdetector.tokenizer import TreebankWordTokenizer
        >>> s = "They'll save and invest more."
        >>> TreebankWordTokenizer().tokenize(s)
        ['They', "'ll", 'save', 'and', 'invest', 'more', '.']
        >>> s = "hi, my name can't hello,"
        >>> TreebankWordTokenizer().tokenize(s)
        ['hi', ',', 'my', 'name', 'ca', "n't", 'hello', ',']
    """

    def __init__(self):
        pass

    STARTING_QUOTES = [
        (re.compile(r'^\"'), r'``'),
        (re.compile(r'(``)'), r' \1 '),
        (re.compile(r'([ (\[{<])"'), r'\1 `` '),
    ]

    PUNCTUATION = [
        (re.compile(r'([:,])([^\d])'), r' \1 \2'),
        (re.compile(r'([:,])$'), r' \1 '),
        (re.compile(r'\.\.\.'), r' ... '),
        (re.compile(r'[;@#$%&]'), r' \g<0> '),
        (re.compile(r'([^\.])(\.)([\]\)}>"\']*)\s*$'), r'\1 \2\3 '),  # Handles the final period.
        (re.compile(r'[?!]'), r' \g<0> '),
        (re.compile(r"([^'])' "), r"\1 ' "),
    ]

    PARENS_BRACKETS = (re.compile(r'[\]\[\(\)\{\}\<\>]'), r' \g<0> ')

    DOUBLE_DASHES = (re.compile(r'--'), r' -- ')

    ENDING_QUOTES = [
        (re.compile(r'"'), " '' "),
        (re.compile(r'(\S)(\'\')'), r'\1 \2 '),
        (re.compile(r"([^' ])('[sS]|'[mM]|'[dD]|') "), r"\1 \2 "),
        (re.compile(r"([^' ])('ll|'LL|'re|'RE|'ve|'VE|n't|N'T) "), r"\1 \2 "),
    ]

    # Adapted from Robert MacIntyre's tokenizer.
    _contractions = [r"(?i)\b(can)(?#X)(not)\b",
                     r"(?i)\b(d)(?#X)('ye)\b",
                     r"(?i)\b(gim)(?#X)(me)\b",
                     r"(?i)\b(gon)(?#X)(na)\b",
                     r"(?i)\b(got)(?#X)(ta)\b",
                     r"(?i)\b(lem)(?#X)(me)\b",
                     r"(?i)\b(mor)(?#X)('n)\b",
                     r"(?i)\b(wan)(?#X)(na)\s",
                     r"(?i) ('t)(?#X)(is)\b",
                     r"(?i) ('t)(?#X)(was)\b"]
    CONTRACTIONS = list(map(re.compile, _contractions))

    def tokenize(self, text):
        for regexp, substitution in self.STARTING_QUOTES:
            text = regexp.sub(substitution, text)

        for regexp, substitution in self.PUNCTUATION:
            text = regexp.sub(substitution, text)

        # Handles parentheses.
        regexp, substitution = self.PARENS_BRACKETS
        text = regexp.sub(substitution, text)

        # Handles double dash.
        regexp, substitution = self.DOUBLE_DASHES
        text = regexp.sub(substitution, text)

        for regexp, substitution in self.ENDING_QUOTES:
            text = regexp.sub(substitution, text)

        return text.split()
