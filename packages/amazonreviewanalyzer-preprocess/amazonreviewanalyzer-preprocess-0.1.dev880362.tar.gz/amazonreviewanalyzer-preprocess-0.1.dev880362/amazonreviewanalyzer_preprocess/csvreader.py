import csv

from amazonreviewanalyzer_preprocess.review import AmazonReview


def readfile(csvfile):
    reader = csv.DictReader(csvfile)
    for dict in reader:
        yield AmazonReview.from_dict(dict)
