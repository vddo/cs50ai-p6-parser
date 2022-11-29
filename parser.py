import nltk
import sys

# nltk.download('punkt')
from nltk.tokenize import word_tokenize, regexp_tokenize

TERMINALS = """
Adj -> "country" | "dreadful" | "enigmatical" | "little" | "moist" | "red"
Adv -> "down" | "here" | "never"
Conj -> "and" | "until"
Det -> "a" | "an" | "his" | "my" | "the"
N -> "armchair" | "companion" | "day" | "door" | "hand" | "he" | "himself"
N -> "holmes" | "home" | "i" | "mess" | "paint" | "palm" | "pipe" | "she"
N -> "smile" | "thursday" | "walk" | "we" | "word"
P -> "at" | "before" | "in" | "of" | "on" | "to"
V -> "arrived" | "came" | "chuckled" | "had" | "lit" | "said" | "sat"
V -> "smiled" | "tell" | "were"
"""

NONTERMINALS = """
S -> NP VP
S -> NP VP PP
S -> NP VP CP
S -> NP VP PP CP

NP -> N | Det N | Det N N | Det AP N  
NP -> Det AP N | N NP | AP NP | NP Adv | P NP
# NP -> Det N PP | Det N N PP | Conj NP 
VP -> V | V NP | V VP | NP V | Adv VP | VP Adv
# VP -> VP CP |
AP -> Adj AP | Adj
CP -> Conj | Conj VP | Adv CP | Conj S
PP -> P | P NP | PP NP
"""

grammar = nltk.CFG.fromstring(NONTERMINALS + TERMINALS)
parser = nltk.ChartParser(grammar)


def main():

    # If filename specified, read sentence from file
    if len(sys.argv) == 2:
        with open(sys.argv[1]) as f:
            s = f.read()

    # Otherwise, get sentence as input
    else:
        s = input("Sentence: ")

    # Convert input into list of words
    s = preprocess(s)

    # Attempt to parse sentence
    try:
        trees = list(parser.parse(s))
    except ValueError as e:
        print(e)
        return
    if not trees:
        print("Could not parse sentence.")
        return

    
    # Print each tree with noun phrase chunks
    for tree in trees:
        # list_of_trees.append(tree)
        tree.pretty_print()

        print("Noun Phrase Chunks")
        for np in np_chunk(tree):
            print(" ".join(np.flatten()))

        return trees

def preprocess(sentence):
    """
    Convert `sentence` to a list of its words.
    Pre-process sentence by converting all characters to lowercase
    and removing any word that does not contain at least one alphabetic
    character.
    """
    # Remove common non alphabetic characters from sentence.
    reg = regexp_tokenize(sentence, r'[,\.\?!"1234567890]\s*', gaps=True)
    
    # Tokenizing all words into one list.
    word_list = []
    for r in reg:
        word_list += word_tokenize(r)
    
    # Convert to lowercase and return
    return(list(map(lambda x: x.lower(), word_list)))


def np_chunk(tree):
    """
    Return a list of all noun phrase chunks in the sentence tree.
    A noun phrase chunk is defined as any subtree of the sentence
    whose label is "NP" that does not itself contain any other
    noun phrases as subtrees.
    """
    list_chunk = []
    
    # Loop over subtrees and save all subtrees with label "NP" regardless 
    # of their level.
    for n in tree.subtrees():
    # print(n)
        if n.label() == "NP":
            list_chunk.append(n)
    
    # Loop over subtrees with label "NP" and add those with own
    # NP-subtree to list_remove
    list_remove = []        
    for i in list_chunk:
        for j in i:
            if j.label() == "NP":
                list_remove.append(i)
                continue
            
    # Remove elements of list_remove from list_chunk.
    for i in list_remove:
        list_chunk.remove(i)
    
    return list_chunk


if __name__ == "__main__":
    main()
