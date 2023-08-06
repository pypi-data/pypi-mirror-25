import argparse
import csv
from collections import Counter

import numpy as np
import sys
from sklearn import tree
from sklearn.ensemble import ExtraTreesClassifier, RandomForestClassifier
from sklearn.feature_extraction.text import CountVectorizer
from csvfilecleaner.clean import CsvFileCleaner


def save_to_file(pattern, classes, output_file):
    f = open(output_file, "w")
    i = 0
    for p, c in zip(pattern, classes):
        i += 1
        f.write(str(i) + "|" + p + "|" + c + "\n")


def get_cardinality(list_of_classes):
    return Counter(list_of_classes).values()


def get_classes(list_of_classes):
    return Counter(list_of_classes).keys()


# the class must be in the last position
def load_dataset_from_csv(csv_file_to_read, class_index, delimiter):
    list_of_offers = []
    list_of_classes = []
    source_file = open(csv_file_to_read)
    reader = csv.reader(source_file, delimiter=delimiter)
    next(reader)
    for row in reader:
        list_of_offers.append(" ".join(row[:class_index]))
        list_of_classes.append(row[class_index])
    return list_of_offers, list_of_classes


class ExpandTrainingSet:
    """
    Add labels to unlabeled data using TriTraining-like approach.
    Trains three classifiers on the same dataset.
    """
    def __init__(self, csv_file, class_index, separator):

        file_cleaner = CsvFileCleaner(csv_file, separator)
        file_cleaner.process()

        pattern, classes = load_dataset_from_csv(csv_file, class_index, separator)
        clf1 = ExtraTreesClassifier(n_estimators=100, n_jobs=12, bootstrap=False, min_samples_split=2, random_state=0)
        clf2 = tree.DecisionTreeClassifier()
        clf3 = RandomForestClassifier(n_estimators=200, n_jobs=12, bootstrap=False, min_samples_split=2, random_state=0)

        count_vect = CountVectorizer(lowercase=False)

        transf_patterns = count_vect.fit_transform(pattern)

        self.separator = separator
        self.class_index = class_index
        self.clf1 = clf1.fit(transf_patterns, classes)
        self.clf2 = clf2.fit(transf_patterns, classes)
        self.clf3 = clf3.fit(transf_patterns, classes)
        self.bow = count_vect

    """
    Add labels to unlabeled data using TriTraining-like approach.
    Trains three classifiers on the same dataset.
    To decide the label to attach to a pattern all possible combination among three classifiers are done.
    If all three classifiers agree on the label -> automatically tag the considered pattern
    Else if two of them agree and both with a confidence greater than the threshold tag the pattern.
    Otherwise skip it.
    """
    def predict_unlabeled_data(self, csv_file, threshold):
        new_pattern = []
        new_classes = []

        file_cleaner = CsvFileCleaner(csv_file, self.separator)
        file_cleaner.process()

        unlabeled_pattern, unlabeled_classes = load_dataset_from_csv(csv_file, self.class_index, self.separator)

        transf_patterns = self.bow.transform(unlabeled_pattern)

        c1 = self.clf1.predict(transf_patterns)
        p1 = self.clf1.predict_proba(transf_patterns)

        c2 = self.clf2.predict(transf_patterns)
        p2 = self.clf2.predict_proba(transf_patterns)

        c3 = self.clf3.predict(transf_patterns)
        p3 = self.clf3.predict_proba(transf_patterns)

        for index, pattern in enumerate(unlabeled_pattern):
            p_max_1 = np.amax(p1[index])
            p_max_2 = np.amax(p2[index])
            p_max_3 = np.amax(p3[index])

            if c1[index] == c2[index] and c2[index] == c3[index]:
                new_pattern.append(pattern)
                new_classes.append(c1[index])

            elif c1[index] == c2[index] and p_max_1 > threshold and p_max_2 > threshold:
                new_pattern.append(pattern)
                new_classes.append(c1[index])

            elif c1[index] == c3[index] and p_max_1 > threshold and p_max_3 > threshold:
                new_pattern.append(pattern)
                new_classes.append(c1[index])

            elif c2[index] == c3[index] and p_max_2 > threshold and p_max_3 > threshold:
                new_pattern.append(pattern)
                new_classes.append(c2[index])

        return new_pattern, new_classes


def main(args):
    labeled_csv_data = args.labeled_file
    unlabeled_csv_data = args.unlabeled_file
    output_file = args.output_file
    class_index = args.class_index
    separator = args.separator
    threshold = args.threshold

    print("Training model on file " + labeled_csv_data)
    expander = ExpandTrainingSet(labeled_csv_data, class_index, separator)
    print("Trying to label unlabeled data " + unlabeled_csv_data)
    exp_pattern, exp_classes = expander.predict_unlabeled_data(unlabeled_csv_data, threshold)
    print("Saving labeled pattern to file " + output_file)
    save_to_file(exp_pattern, exp_classes, output_file)


def parse_arguments(argv):

    parser = argparse.ArgumentParser()
    parser.add_argument('labeled_file', type=str, help='Path of the labeled file')
    parser.add_argument('unlabeled_file', type=str, help='Path of the unlabeled file')
    parser.add_argument('output_file', type=str,
                        help='Path to the result file with pattern to be added to the original dataset')
    parser.add_argument('--class_index', type=int,
                        help='Index of class in the dataset [count from 0 to n - 1], default=1', default=1)
    parser.add_argument('--separator', type=str, help='Separator of the CSV file, default=\',\'', default=",")
    parser.add_argument('--threshold', type=float,
                        help='Threshold for discarding low confidence patterns, default=0.9', default=0.9)

    return parser.parse_args(argv)


if __name__ == '__main__':
    main(parse_arguments(sys.argv[1:]))
