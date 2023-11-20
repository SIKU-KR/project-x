class Node(object):
    def __init__(self, key):
        self.key = key
        self.children = {}
        self.branch = 0
        self.isLeaf = False  # Initialize the isLeaf attribute

class Trie(object):
    def __init__(self):
        self.root = Node(None)

    def insert(self, word):
        curr_node = self.root
        curr_node.branch += 1

        for i in range(len(word)):
            chr = word[i]
            if chr not in curr_node.children:
                curr_node.children[chr] = Node(chr)  # Fix the Node instance creation
            curr_node = curr_node.children[chr]
            curr_node.branch += 1
            if i == len(word) - 1:
                curr_node.isLeaf = True

    def search_count(self, word):
        curr_node = self.root
        for i in range(len(word)):
            chr = word[i]
            if chr in curr_node.children:
                curr_node = curr_node.children[chr]
                if curr_node.branch == 1:
                    return i + 1
        return len(word)

    def autocomplete(self, prefix):
        def find_words(node, prefix, words):
            if node.isLeaf:
                words.append(prefix)
            for char, next_node in node.children.items():
                find_words(next_node, prefix + char, words)

        curr_node = self.root
        words = []
        for char in prefix:
            if char in curr_node.children:
                curr_node = curr_node.children[char]
            else:
                return []  # Prefix not in trie
        find_words(curr_node, prefix, words)
        return words

# Example Usage
t = Trie()
t.insert("apple")
t.insert("app")
t.insert("apricot")
t.insert("banana")
print(t.autocomplete("ap"))  # Should return ['apple', 'app', 'apricot']
