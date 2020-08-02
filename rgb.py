import spacy
from flair.data import Sentence
from flair.models import SequenceTagger
from flair.tokenization import SegtokTokenizer
import time


# edit this to be a list of strings you wish to correct.
# to guarantee all formats of string are supported, it is suggested
# you surround the strings with triple quotes (e.g. """ some text """)
# instead of the typical 'some text' or "some text". this will allow
# multi-line strings and avoids clashes with internal ' and " characters.
# if the text ends with a " character you will still need to modify it to
# \" because it will read the first three " characters, then the fourth
# will confuse it.
text_list = ["""this is
some 'text'""",
"""who is he speaking to?""",
"""who's he speaking to?""",
"""He shouted at The Who""",
"""He shouted at who?"""]

nlp = spacy.load('en_core_web_sm')
tagger = SequenceTagger.load('ner')


# return start of corrected phrase, end of phrase, and whether starts with whom.
def i_span(doc, token):

    i_token = token.i
    i_head = token.head.i

    if i_token < i_head:
        return i_token, i_head, True
    else:
        return i_head, i_token, False


# checks for various surrounding tokens which produce false flags
# due to the typically terrible overall grammar and prevelance of
# typos in forum posts written with these.
def check_for_exceptions(doc, token):

    i = token.i

    if i > 0 and doc[i - 1].text.lower() in ['the', '\"']:
        return True

    if len(doc) > i + 1:
        if doc[i + 1].text.lower in ['tf', '\"']:
            return True
        if doc[i + 1].text[0] == '\'':
            return True

    if len(doc) > i + 2:
        the_check = doc[i + 1].text.lower() in ['the', 'teh', 'th3', 't3h', 'da', 'd4', 'tha', 'th4', 't']
        fuck_check = doc[i + 2].text.lower() in ['fuck', 'fck', 'fk', 'f', 'fuuck', 'fuuuck', 'fuuuuck', 'fuuuuuck']

        if the_check and fuck_check:
            return True

    return False


# use all caps or Spongebob-case if being used, otherwise append lowercase m.
# surrounds with * on each side to emphasize the corrected word - on reddit
# this italicizes the word.
def whom_string(who_string):
    if who_string == 'WHO':
        return '*WHOM*'
    elif who_string == 'wHo':
        return '*wHoM*'
    else:
        return '*' + who_string + 'm*'


# checks if 'who' is used where 'whom' should be used (i.e. as an object), and
# for each such instance prints the text along with a correction to 'whom'
# either starting at 'whom' and ending with the relevant verb/root, or vice versa.
def correct_who_to_whom(text):

    doc = nlp(text)

    phrases = []

    token_number = 0

    for token in doc:

        token_number += 1

        # it is very difficult for named entity recognizer to recognize 'Who'
        # in isolation - the motivating text was repeated exclamation of
        # 'Who! Who!' in a The Grinch fan fiction.
        if token.text.lower() in ['grinch', 'whoville']:
            return

        if token.text.lower() == 'who' :
            if token.dep_ in ['dobj', 'iobj', 'pobj']:

                # check for the hard-coded exceptions
                if not check_for_exceptions(doc, token):
                    should_be_whom = True

                    sentence = Sentence(text, use_tokenizer=SegtokTokenizer())
                    tagger.predict(sentence)

                    # make sure it is not part of a named entity
                    for entity in sentence.get_spans('ner'):
                        if token.idx >= entity.start_pos and token.idx <= entity.end_pos:
                            should_be_whom = False

                    if should_be_whom:

                        phrase_start, phrase_end, whom_first = i_span(doc, token)

                        if whom_first:
                            # detokenizes the corrected excerpt (e.g. removes added space
                            # between last word in sentence and punctutation, rejoins
                            # don and 't to form don't, etc., only if such joins were
                            # present in the original text)
                            phrase = whom_string(token.text) + (''.join([tkn.text_with_ws for tkn in doc[phrase_start:phrase_end + 1]]))[3:]

                            phrases.append(phrase)
                        else:
                            # detokenizes the corrected excerpt (e.g. removes added space
                            # between last word in sentence and punctutation, rejoins
                            # don and 't to form don't, etc., only if such joins were
                            # present in the original text)
                            phrase = ''.join([tkn.text_with_ws for tkn in doc[phrase_start:phrase_end]]) + whom_string(token.text)

                            phrases.append(phrase)

    # if any corrections were found, then print the original text and the corrections.
    if phrases:
        joined_phrases = '\n\n'.join(phrases)

        print('<<<  TEXT  >>>')
        print(text)
        print('<<<  CORRECTIONS  >>>')
        print(joined_phrases)
        print()
        print()


# keep track of submissions already replied to, to avoid buggy repeats
#already_replied_to = []
def main():

    for text in text_list:
        correct_who_to_whom(text)


main()
