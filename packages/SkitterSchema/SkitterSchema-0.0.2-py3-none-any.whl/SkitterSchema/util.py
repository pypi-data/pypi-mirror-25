import re


def extract_hashtags(stc):
    tmp = set(part for part in re.split(" ", re.sub("\.|,|;|\(|\)|:|!|^|~|\n", "", stc)) if part.startswith('#'))

    ret_list = []
    for hashtag in tmp:
        i = dict()
        i['text'] = hashtag[1:]
        ret_list.append(i)

    return ret_list


def extract_mentions(stc):
    return set(part for part in re.split("\.|,| |;|\n", re.sub("\.|,|;|!|^|~|\n", "", stc)) if part.startswith('@'))


def get_or_create(session, model, defaults=None, **kwargs):
    instance = session.query(model).filter_by(**kwargs).first()
    if instance:
        return instance
    else:
        params = dict((k, v) for k, v in kwargs.iteritems() if not isinstance(v, ClauseElement))
        if defaults:
            params.update(defaults)
        instance = model(**params)
        return instance


class Dict2Obj(object):
    def __init__(self, dictionary):
        """Constructor"""
        for key in dictionary:
            setattr(self, key, dictionary[key])