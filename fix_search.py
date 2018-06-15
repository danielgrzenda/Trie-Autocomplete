import sys
import string


class AmazingAutoComplete():
    def __init__(self, word_list, prefix=False):
        self.root = self.TrieNode()
        self.word_list = word_list
        if prefix:
            for word in self.word_list:
                self.insert(self.root, word)
        else:
            for word in self.word_list:
                self.insert_backward(self.root, word[::-1])

    def insert(self, node, string):
        for letter in string:
            if node[ord(letter) - ord('a')] is not -1:
                node = node[ord(letter) - ord('a')]
                node.contains.append(string)
            else:
                node[ord(letter)-ord('a')] = self.TrieNode()
                node = node[ord(letter)-ord('a')]
                node.contains.append(string)

    def insert_backward(self, node, string):
        for letter in string:
            if node[ord(letter) - ord('a')] is not -1:
                node = node[ord(letter)-ord('a')]
                node.contains.append(string[::-1])
            else:
                node[ord(letter)-ord('a')] = self.TrieNode()
                node = node[ord(letter) - ord('a')]
                node.contains.append(string[::-1])

    def get(self, node, string):
        for letter in string:
            node = node[ord(letter)-ord('a')]
        return node.contains

    class TrieNode(object):
        def __init__(self):
            self.hash = [-1 for x in string.ascii_lowercase]
            self.contains = []

        def __getitem__(self, index):
            return self.hash[index]

        def __setitem__(self, index, item):
            self.hash[index] = item


def parse_input():
    arguments = sys.argv[1:]
    if len(arguments) > 2:
        raise Exception('There were too many command line arguments supplied')
    return arguments


def stdin_input(inp):
    word_list = []
    for line in inp:
        word_list.append(line.strip())
    return word_list


def search_prefix(arguments, word_list):
    prefix = check_args(arguments[1])
    structure = AmazingAutoComplete(word_list, prefix=True)
    return structure.get(structure.root, prefix)


def search_suffix(arguments, structure):
    suffix = check_args(arguments[1])
    structure = AmazingAutoComplete(word_list)
    return structure.get(structure.root, suffix[::-1])


def print_help(arguments):
    if len(arguments) > 1:
        raise Exception('''Too many arguments supplied to the help function!
Type python fix_search.py --help to see the possible arguments.
Only one is allowed''')
    print(f'''usage: fix_search.py [option] ... [-p str | -s str | file | -]...
Options and arguments (and corresponding environment variables):
-h  --help   : get help (you are here!)
-p  --prefix : search for words in the input that start with a prefix
-s  --suffix : search for words in the input that end with a suffix

This is O(n) where n is the number characters, because it only has to
traverse n connections from one Trie node to another.
Then it can return the node.contains.
It is also space efficient due to the storing of only node pointers.
''')


def check_args(substring):
    if len(substring) < 1:
        raise Exception('The substring to search must not be empty!')
    if all(ord(c) < 123 and ord(c) > 64 for c in substring):
        return substring.lower()
    raise Exception('All characters must be ascii')


if __name__ == "__main__":
    # get arguments
    arguments = parse_input()
    # handle it ifs its just a call for help
    if arguments[0] in ('-h', '--help'):
        print_help(arguments)
    # handle prefix and suffix
    elif arguments[0] in ('-p', '--prefix'):
        word_list = stdin_input(sys.stdin)
        words = search_prefix(arguments, word_list)
        print(words)
    elif arguments[0] in ('-s', '--suffix'):
        word_list = stdin_input(sys.stdin)
        words = search_suffix(arguments, word_list)
        print(words)
    else:
        raise Exception('''The arguments you supplied are not supported.
See try python fix_search.py --help for help''')
