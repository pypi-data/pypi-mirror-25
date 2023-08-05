import os
import argparse

from detector import Detector


def is_zero_file(file_path):
    return not (os.path.isfile(file_path) and os.path.getsize(file_path) > 0)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(formatter_class=argparse.RawDescriptionHelpFormatter,
                                     description='Plagiarism Detector: Calculates percentage of N-Tuples '
                                                 'from file1 found in file2',
                                     epilog="Test: python.exe -m unittest discover tests\n\n"
                                            "Example: \n"
                                            "  Returns            100%\n"
                                            "  Synonyms           run jog spring\n"
                                            "  Evaluation File    go for a run \n"
                                            "  Source File        go for a jog \n"
                                            "  N-tuples           3 \n")
    parser.add_argument('syn', metavar='synonym_file_path', type=str, help='Path to file to be used for synonyms')
    parser.add_argument('f1', metavar='evaluation_file_path', type=str, help='Path to file to be evaluated')
    parser.add_argument('f2', metavar='source_file_path', type=str, help='Path to file to be used as source for '
                                                                         'matching')
    parser.add_argument('N', metavar='n-tuples', type=int, nargs='?', default=3, help='Number of N-tuples, '
                                                                                      'Optional and Defaults to 3')
    args = vars(parser.parse_args())

    if is_zero_file(args['syn']):
        print("Synonyms file does not exists")
    elif is_zero_file(args['f1']):
        print("First file does not exists")
    elif is_zero_file(args['f2']):
        print("Second file file does not exists")
    else:
        pd = Detector(args['syn'], args['f1'], args['f2'], args['N'])
        print(pd.detect())
