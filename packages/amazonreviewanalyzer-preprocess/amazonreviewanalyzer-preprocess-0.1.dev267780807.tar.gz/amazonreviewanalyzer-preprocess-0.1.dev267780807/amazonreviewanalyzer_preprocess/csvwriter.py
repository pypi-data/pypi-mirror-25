import csv

from amazonreviewanalyzer_preprocess.review import AmazonReviewBaseClass


def writecsv(reviews, csvfile):
    writer = csv.DictWriter(csvfile, AmazonReviewBaseClass._fields)
    for review in reviews:
        writer.writerow(review.to_dict())
