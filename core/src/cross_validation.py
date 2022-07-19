import numpy as np
from sklearn.model_selection import KFold
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report


# ... Dummy data
X = np.random.random((100, 5))
y = np.zeros((100, ))

# ... Classifier
clf = RandomForestClassifier()


def cross_validation(X, y, clf):
    CV = KFold(
        n_splits=5,
        shuffle=True,
        random_state=42
    )

    all_true_labels = []
    all_predicted_labels = []

    for train_index, test_index in CV.split(X):
        X_train, X_test = X[train_index], X[test_index]
        y_train, y_test = y[train_index], y[test_index]

        clf.fit(X_train, y_train)

        y_pred = clf.predict(X_test)

        all_true_labels.append(y_test.tolist()[0])
        all_predicted_labels.append(y_pred.tolist()[0])

    results = classification_report(
        all_true_labels,
        all_predicted_labels,
        zero_division=0
    )
    print(results)


# ... Cross-validation
cross_validation(X, y, clf)
