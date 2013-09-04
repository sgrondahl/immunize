
class Tweet(object):
    def __init__(self, status=None, translation=None, time=None, _id=None) :
        self.status = status
        self.translation = translation
        self.time = time
    def serialize(self) :
        return { 'status' : self.status,
                 'translation' : self.translation,
                 'time' : self.time }
    @classmethod
    def deserialize(cls, **d) :
        return cls(**d)
