from sklearn import tree


def decision_tree(x_train, y_train, x_predict):
    clf_model = tree.DecisionTreeClassifier()
    clf_model = clf_model.fit(x_train, y_train)
    y_predict = clf_model.predict(x_predict)

    return y_predict
