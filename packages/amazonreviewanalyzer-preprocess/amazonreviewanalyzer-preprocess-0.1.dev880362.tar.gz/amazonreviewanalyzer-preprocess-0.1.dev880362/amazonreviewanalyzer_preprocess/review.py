import json
from collections import namedtuple


class BreakLoopException(Exception):
    'Used to break from a nested loop'


AmazonReviewBaseClass = namedtuple(
    'AmazonReview',
    'sentivalue categories url name price review_title '
    'review_text review_rating review_num_helpful')


class AmazonReview(AmazonReviewBaseClass):
    @classmethod
    def from_dict(cls, dict):
        # sentivalue is optional (for now)
        sentivalue = dict.get('sentivalue', '')
        categories = dict['categories'].split(',')
        usd_price = get_usd_price(json.loads(dict['prices']))
        try:
            rating = int(dict['reviews.rating'])
        except ValueError:
            # a rating of 0 indicates no rating
            rating = 0
        try:
            num_helpful = int(dict['reviews.numHelpful'])
        except ValueError:
            num_helpful = 0
        return cls(
            sentivalue,
            categories, dict['reviews.sourceURLs'], dict['name'], usd_price,
            dict['reviews.title'], dict['reviews.text'], rating, num_helpful)

    def to_dict(self):
        return {
            'sentivalue': self.sentivalue,
            'categories': self.categories,
            'url': self.url,
            'name': self.name,
            'price': self.price,
            'review_title': self.review_title,
            'review_text': self.review_text,
            'review_rating': self.review_rating,
            'review_num_helpful': self.review_num_helpful
        }


def get_usd_price(prices):
    priceinfo = {}
    for priceinfo in prices:
        try:
            for k, v in priceinfo.items():
                if (k, v) == (u'currency', u'USD'):
                    raise BreakLoopException()
        except BreakLoopException:
            break
    assert priceinfo != {}
    return (priceinfo['amountMin'] + priceinfo['amountMax']) / 2
