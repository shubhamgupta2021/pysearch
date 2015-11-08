from nltk.corpus import wordnet
from nltk.stem import WordNetLemmatizer
from nltk import word_tokenize, sent_tokenize
from getopt import getopt, GetoptError
import sys
from os import walk, path


d = {}

def get_attributes(argv):
    try:
        opts, args = getopt(argv, "hf:d:", ["file", "directory"])
    except GetoptError:
        print """Usage:
            python search.py -f <filename> words_to_search
            OR python search.py -d <directory> words_to_search"""
        sys.exit(2)
    if len(opts) >= 2:
        print """Usage:
                python search.py -f <filename> words_to_search
                OR python search.py -d <directory> words_to_search

                Give only one option either filename or directory"""
        sys.exit(2)

    for opt, arg in opts:
        if opt == '-h':
            print """Usage:
                python search.py -f <filename> words_to_search
                OR python search.py -d <directory> words_to_search"""
            sys.exit(0)

        elif opt == '-f':
            filename = arg
            source_type = 'file'
            return source_type, filename, args

        elif opt == '-d':
            directory = arg
            source_type = 'directory'
            return source_type, directory, args


def find_synonyms(word):
    synonyms = []
    synonyms_sets = wordnet.synsets(word)
    for synonyms_set in synonyms_sets:
        synonyms = synonyms + synonyms_set.lemma_names()
    synonyms = set(synonyms)
    return  list(synonyms)

def search_in_file(file):
    try:
        with open(file,'r') as fp:
            text = fp.read()
            sentences = sent_tokenize(text)
            for sentence in sentences:
                sentence = sentence.replace('\n', ' ')
                for word in word_tokenize(sentence):
                    if word in d:
                        d[word].append(sentence)
            first_match = 1
            for word in d:
                count=len(d[word])
                if count > 0:
                    if first_match == 1:
                        print "Results found in %s file" %(file)
                    first_match = 0
                    print "%d results found for %s" %(count, word)
                    for line in d[word]:
                      print line
                    d[word] = []
            if first_match == 1:
                print "No results found in %s" %(file)
        print "\n"

    except IOError as e:
        print "Error: Cannot Open File"
        sys.exit(e.errno)

def main():
    args = sys.argv[1:]
    (source_type, source, words_to_search) = get_attributes(args)
    for word in words_to_search:
        for synonm in  find_synonyms(word):
            d[synonm] = []
    if source_type == 'directory':
        all_files = []
        for (directorypath, directories, files) in walk(source):
            files = [ path.join(directorypath, file) for file in files ]
            all_files = all_files + files
        for file in all_files:
            search_in_file(file)

    if source_type == 'file':
        search_in_file(source)


if __name__ == "__main__":
    main()