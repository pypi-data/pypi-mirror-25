
import json
from copy import deepcopy as copy


class Div:
    """"""

    def __init__(self, **kwargs):
        """
        TBD
        """
        # attributes
        self.type = 'Div'
        self.id_name = None
        self.class_name = None
        self.content = None
        self.width = None

        for k, v in kwargs.items():
            setattr(self, k, v)
        self.valid = self.check()

    def check(self, verbose=False):
        isDiv = any([getattr(self, k) is not None for k in [
                    'id_name', 'class_name', 'content', 'width']])
        if verbose:
            print('Div: isDiv=', isDiv)
        msg = 'Div must contain a div element defined by at least one attribute'
        assert isDiv, msg

        return True

    def to_dict(self):
        d = copy(self.__dict__)
        d = {k: v for k, v in d.items() if v is not None}
        return d

    def pprint(self, indent=2):
        d = json.dumps(self.to_dict(), sort_keys=True, indent=indent)
        print(d)

    def __repr__(self):
        return str(self.to_dict())
