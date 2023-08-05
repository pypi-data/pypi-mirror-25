=========================
Plagiarism Detector Py2.7
=========================

Calculates percentage of N-Tuples from file1 found in another file2::

    from plagiarismdetector.detector import Detector

    print Detector.detect(synonyms_file_path,
                           eval_file_path,
                           source_file_path,
                           n_tuples_value=3)



Running
=========
``python plagiarismdetector/main.py synonyms_file_path eval_file_path source_file_path 3``


======================
Assumptions & Overview
======================
* Dependent on Python2.7
* English language text, reason being it divides strings based off that might fail for e.g. in Hindi since sentence separators and punctuations are entirely different.
* Adapted Penn TreeBank tokenizer for splitting up strings
* The module is optimized to be as fast as possible, some of the optimizations are:
    * Only n-grams for file 2 are generated and stored, file 1 n-tuples are generated but not stored.
    * Not holding generated n-grams in memory, a generator is used
    * Dictionary of n-grams is created from file2 n-grams for constant time lookup of file1 tuples
    * Keys in file2 n-gram dictionary contains hashes for tuples instead of actual tuples to reduce space complexity.
    * Since we are only concerned with percentage of file1 n-tuples found in file2, we do not need to store any tuples. Therefore, we first generate n-grams for file2 and then calculate count for file1 on the fly instead of generating all n-tuples of file1 and cross referencing it with those of file2.


Testing
=========
``python -m unittest discover tests``

Help
=========
``python plagiarismdetector/main.py -h``

positional arguments
--------------------
  synonym_file_path     Path to file to be used for synonyms
  evaluation_file_path  Path to file to be evaluated
  source_file_path      Path to file to be used as source for matching
  n-tuples              Number of N-tuples, Optional and Defaults to 3

optional arguments
------------------
  -h, --help            show this help message and exit

Example
=========
  ================   ===============
  Returns            100.0
  ================   ===============
  Synonyms           run jog spring
  Evaluation File    go for a run
  Source File        go for a jog
  N-tuples           3
  ================   ===============