import trafaret as t

from datarobot.models.api_object import APIObject
from datarobot.utils import encode_utf8_if_py2


class WordCloud(APIObject):
    """ Word cloud data for the model.

    Attributes
    ----------
    ngrams: list of dict
        List of the wordcloud ngrams and corresponding data. Dictionary has following keys:
        ngram: str
            Word or ngram value.
        coefficient: float
            Value from [-1.0, 1.0] range, describes effect of this ngram on the target.
            Large negative value means strong effect toward negative class in classification and
            smaller target value in regression models. Large positive - toward positive class and
            bigger value respectively.
        count: int
            Number of rows in the training sample where this ngram appears.
        frequency: float
            Value from (0.0, 1.0] range, relative frequency of given ngram to most frequent ngram.
        is_stopword: bool
            True for ngrams that DataRobot evaluates as stopwords.
    """
    _converter = t.Dict({
        t.Key('ngrams'): t.List(t.Dict({
            t.Key('ngram'): t.String,
            t.Key('coefficient'): t.Float(gte=-1, lte=1),
            t.Key('count'): t.Int,
            t.Key('frequency'): t.Float(gt=0, lte=1),
            t.Key('is_stopword'): t.Bool
        }).ignore_extra('*'))
    }).ignore_extra('*')

    def __init__(self, ngrams):
        self.ngrams = ngrams

    def __repr__(self):
        return encode_utf8_if_py2(u'WordCloud({} ngrams)'.format(len(self.ngrams)))

    def most_frequent(self, top_n=5):
        """ Return most frequent ngrams in the word cloud.

        Parameters
        ----------
        top_n : int
            Number of ngrams to return

        Returns
        -------
        list of dict
            Up to top_n top most frequent ngrams in the word cloud.
            If top_n bigger then total number of ngrams in word cloud - return all sorted by
            frequency in descending order.
        """
        return sorted(self.ngrams,
                      key=lambda ngram: ngram['frequency'],
                      reverse=True)[:top_n]

    def most_important(self, top_n=5):
        """ Return most important ngrams in the word cloud.

        Parameters
        ----------
        top_n : int
            Number of ngrams to return

        Returns
        -------
        list of dict
            Up to top_n top most important ngrams in the word cloud.
            If top_n bigger then total number of ngrams in word cloud - return all sorted by
            absolute coefficient value in descending order.
        """
        return sorted(self.ngrams,
                      key=lambda ngram: abs(ngram['coefficient']),
                      reverse=True)[:top_n]
