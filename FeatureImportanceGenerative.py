# I have no idea what I'm doing
# ~~ Proverbs 4:20

from FeatureImportance import load_prepared_data
from DataPreparation import split_label
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis


def get_LDA_classifier(X_train, y_train):
    # TODO: which solver?
    lda = LinearDiscriminantAnalysis(solver='eigen')
    # TODO: should this be done using CV?
    # X_train_new = lda.fit_transform(X_train, y_train)
    lda.fit(X_train, y_train)
    return lda


def get_LDA_coefficients(lda):
    coefficients = lda.coef_
    max_args = np.argmax(coefficients, axis=1)
    max_args_abs = np.argmax(np.abs(coefficients), axis=1)
    return max_args, max_args_abs, coefficients


def plot_leading_features(max_args, max_args_abs, coefficients, df):
    code_to_name = dict(enumerate(df['Vote'].astype('category').cat.categories))
    attribute_index_to_name = dict(enumerate(df.columns.values))

    for i, max_arg_index in enumerate(max_args_abs):
        print('for party {} the most important index was {} with a linear coefficient of {:.4}'
              .format(code_to_name[i],
                      attribute_index_to_name[max_arg_index],
                      coefficients[i][max_arg_index]))

        plt.figure()
        plt.title('{} most important factors\n(larger (abs) is better)'.format(code_to_name[i]), x=0)
        plt.barh(X_test.columns.values, coefficients[i])
        plt.show()
        # commented out saving since we have the graphics
        # plt.savefig('{}_LDA.png'.format(code_to_name[i]))
        plt.close()


def get_data():
    train, validate, test = load_prepared_data()
    df = pd.concat([train, validate])
    X_train, y_train = split_label(df)
    X_test, y_test = split_label(test)
    return X_train, y_train, X_test, y_test, df


if __name__ == '__main__':
    X_train, y_train, X_test, y_test, df = get_data()
    lda = get_LDA_classifier(X_train, y_train)
    max_args, max_args_abs, coefficients = get_LDA_coefficients(lda)
    plot_leading_features(max_args, max_args_abs, coefficients, df)