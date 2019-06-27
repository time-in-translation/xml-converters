import os

from lxml import etree

from swda.swda import CorpusReader


def process_single(language, swda_transcript, out_file):
    """
    Converts an CONLL-U file to the OPUS-xml format.
    """

    # Start a text element and add a first paragraph
    text = etree.Element('text')
    text.set('topic', swda_transcript.topic_description)

    current_utterance_index = 0
    prev_act_tag = ''
    prev_damsl_act_tag = ''
    # Load the file and loop over the sentences
    for utterance in swda_transcript.utterances:
        if current_utterance_index != utterance.utterance_index:
            paragraph = etree.SubElement(text, 'p')
            paragraph.set('id', str(utterance.utterance_index))
            current_utterance_index = utterance.utterance_index

        i = str(current_utterance_index)
        j = str(utterance.subutterance_index)

        # A '+' signals continuation of the previous utterance: use that dialog act annotation
        act_tag = utterance.act_tag if utterance.act_tag != '+' else prev_act_tag
        damsl_act_tag = utterance.damsl_act_tag() if utterance.damsl_act_tag() != '+' else prev_damsl_act_tag

        sentence = etree.SubElement(paragraph, 's')
        sentence.set('id', 's{}.{}'.format(i, j))
        sentence.set('caller', utterance.caller)
        sentence.set('act_tag', act_tag)
        sentence.set('damsl_act_tag', damsl_act_tag)

        prev_act_tag = act_tag
        prev_damsl_act_tag = damsl_act_tag

        # Use lemmata from WordNet, but use the original PoS-tags (TreeTagger-like)
        lem_list = utterance.pos_lemmas(wn_lemmatize=True)
        pos_list = utterance.pos_lemmas(wn_lemmatize=False)
        for k, word in enumerate(utterance.pos_words()):
            lemma = lem_list[k][0]
            pos = pos_list[k][1]
            add_token(language, sentence, word, lemma, pos, i, j, k + 1)

    tree = etree.ElementTree(text)
    tree.write(out_file, pretty_print=True, xml_declaration=True, encoding='utf-8')


def add_token(language, sentence, token, lemma, pos, i, j, k):
    """
    Converts a CONLL-U token to a OPUS-xml 'w'-tag.
    """
    word = etree.SubElement(sentence, 'w')
    word.text = token
    word.set('id', 'w{}.{}.{}'.format(i, j, k))
    word.set('lem', lemma)
    word.set('tree', pos)


if __name__ == '__main__':
    corpus = CorpusReader('swda/swda')
    for transcript in corpus.iter_transcripts():
        out_file = os.path.splitext(os.path.basename(transcript.swda_filename))[0]
        out_path = 'swda-opus'
        os.makedirs(out_path, exist_ok=True)
        process_single('en', transcript, os.path.join(out_path, out_file + '.xml'))
