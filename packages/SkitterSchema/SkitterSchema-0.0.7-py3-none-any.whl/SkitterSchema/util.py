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


def remove_mentions(text):
    for mention in extract_mentions(text):
        text = text.replace(mention, "")
    return re.sub("( |\n)+", " ", text).strip()


class Dict2Obj(object):
    def __init__(self, dictionary):
        """Constructor"""
        for key in dictionary:
            setattr(self, key, dictionary[key])


def get_edges(id_v, edges, criteria):
    matching_edges = set()
    for edge in edges:
        if criteria(edge, id_v):
            matching_edges.add(edge)
    return list(matching_edges)
