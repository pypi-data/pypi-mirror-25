from functools import total_ordering

from django.utils import six
from hashids import Hashids, _is_uint


@total_ordering
class Hashid(object):
    def __init__(self, id, salt='', min_length=0, alphabet=Hashids.ALPHABET):
        self.hashids = Hashids(salt=salt, min_length=min_length, alphabet=alphabet)
        self.id = id
        self.hashid = self.set(id)

    def encode(self, id):
        return self.hashids.encode(id)

    def decode(self, hashid):
        id = self.hashids.decode(hashid)
        if len(id) == 1:
            return id[0]
        else:
            return None

    def set(self, id):
        # First see if we were given an already-encoded and valid Hashids string
        value = self.decode(id)
        if value:
            self.id = value
            self.hashid = id
            return self.hashid

        # Next see if it's a positive integer
        try:
            id = int(id)
        except (TypeError, ValueError):
            raise ValueError("id must be a positive integer or valid Hashid value")
        if not _is_uint(id):
            raise ValueError("id must be a positive integer")

        # Finally, set our internal values
        self.id = id
        self.hashid = self.encode(id)
        return self.hashid

    def __repr__(self):
        return "Hashid({}): {}".format(self.id, self.hashid)

    def __str__(self):
        return self.hashid

    def __int__(self):
        return self.id

    def __eq__(self, other):
        if isinstance(other, self.__class__):
            return self.id == other.id and self.hashid == other.hashid
        if isinstance(other, six.string_types):
            return self.hashid == other
        return NotImplemented

    def __lt__(self, other):
        if isinstance(other, self.__class__):
            return self.id < other.id
        if isinstance(other, type(self.id)):
            return self.id < other
        return NotImplemented

    def __len__(self):
        return len(self.hashid)

    def __hash__(self):
        return hash(self.hashid)
