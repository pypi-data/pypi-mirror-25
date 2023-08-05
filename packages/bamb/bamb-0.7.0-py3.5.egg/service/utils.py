from __future__ import with_statement

from common import utils


class IdGenerator:

    __all_generators = {}

    def __init__(self, category="global", last_id = -1):
        self.__category = category
        self.__last_id = last_id
        IdGenerator.__all_generators[category] = self

    @staticmethod
    def next(category="global"):
        ig = IdGenerator.__all_generators.get(category, None)
        i = -1
        if isinstance(ig, IdGenerator):
            with utils.LockContext(ig):
                ig.__last_id += 1
                i = ig.__last_id
        return i

    @staticmethod
    def setup(d):
        for k, v in d.items():
            if isinstance(v, int) and isinstance(k, str):
                IdGenerator.__all_generators[k] = IdGenerator(category=k, last_id=v)

    @staticmethod
    def reset():
        IdGenerator.__all_generators.clear()


