import io
from os.path import dirname, join
import pycrfsuite
from underthesea.util.singleton import Singleton
from underthesea.word_sent.transformer import Transformer


@Singleton
class CRFModel:
    def __init__(self):
        """
        load trained data from crf-model
        """
        self.model = pycrfsuite.Tagger()
        filepath = join(dirname(__file__), "wordsent_crf_v1.model")
        self.model.open(filepath)

    def predict(self, text, format=None):
        """

        :param unicode|str text: raw text
        :return: segmented text
        :rtype: unicode|str
        """
        tokens = Transformer.transform(text)
        tags = self.model.tag(tokens)
        if len(tags) > 0:
            tags[0] = "B_W"
        tokens = [item[0] for item in tokens]
        output = []
        for tag, token in zip(tags, tokens):
            if tag == "I_W":
                output[-1] = output[-1] + u" " + token
            else:
                output.append(token)
        if format == "text":
            output = u" ".join([item.replace(" ", "_") for item in output])
        return output

