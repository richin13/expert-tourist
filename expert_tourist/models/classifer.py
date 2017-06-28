import pickle
import mongoengine as me
import numpy as np

from sklearn.naive_bayes import GaussianNB

from . import db


class Classifier(db.Document):
    meta = {'allow_inheritance': True}
    name = me.StringField(max_length=16, required=True, unique=True)
    data = me.BinaryField()

    def __init__(self, *args, **kwargs):
        super(Classifier, self).__init__(*args, **kwargs)
        if self.name == None:
            self.name = self._get_classifier_name()

    def build(self, rebuild=False) -> GaussianNB:
        clf = Classifier.objects(name=self.name).first()

        if clf != None:
            self.id = clf.id
            self.data = clf.data
        else:
            self.fit()
            rebuild = True

        if rebuild:
            self.save()

        return pickle.loads(self.data)

    def fit(self):
        clf = GaussianNB()
        X, Y = self.dataset()
        clf.fit(X, Y)

        self.data = pickle.dumps(clf)

    def classify(self, instance):
        vector = self.vector(instance)
        classifier = self.build()

        return int(classifier.predict([vector])[0])

    def vector(self, instance):
        vector = list()
        for attribute in self.Meta.attributes:
            vector.append(getattr(instance, attribute))
        return np.array(vector)

    def dataset(self):
        all_ = self.Meta.model.objects
        dataset = list()
        targets = list()
        for record in all_:
            dataset.append(self.vector(record))
            targets.append(getattr(record, self.Meta.class_attribute))

        return np.array(dataset), np.array(targets)

    def _get_classifier_name(self):
        model = self.Meta.model
        return model.__name__.lower()
