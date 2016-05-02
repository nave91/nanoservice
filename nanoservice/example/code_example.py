from nanoservice.codemanager import CodeManager
from sklearn.svm import SVC
from sklearn import datasets


class MyCodeManager(CodeManager):

    @classmethod
    def name(cls):
        return 'svc'

    def load(self):
        # raise NotImplemented
        print("Entered worker")
        clf = SVC()
        iris = datasets.load_iris()
        clf.fit(iris.data, iris.target_names[iris.target])
        return clf

    def evaluate(self, trained_algorithm, input):
        # raise NotImplemented
        return trained_algorithm.predict(input)

    def validate_input(self, input):
        # raise NotImplemented
        validated_input = [float(i) for i in input.split(',')]
        return validated_input
