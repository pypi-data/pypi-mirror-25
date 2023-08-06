import abc


class JSONSerializable(object):
    __metaclass__ = abc.ABCMeta

    @abc.abstractclassmethod
    def from_dict(self, d):
        pass

    @abc.abstractclassmethod
    def from_json(self, json):
        pass

    @abc.abstractmethod
    def to_json(self):
        pass

    @abc.abstractmethod
    def to_dict(self):
        pass
