import textacy

def get_ngrams(doc, n):
    '''
    This function takes the spacy doc and number of grams(n) and returns the grams of the formatted doc
    according to the number(n) passed
    :param doc: spaCy doc
    :param n: Int(Number of n grams needed eg: 2,3,4...)
    :return: n grams of the formatted doc with respect to value of n passed
    '''
    n_grams = list(textacy.extract.ngrams(doc, n))
    formatted_nrams = [ngm.text for ngm in n_grams]
    return formatted_nrams