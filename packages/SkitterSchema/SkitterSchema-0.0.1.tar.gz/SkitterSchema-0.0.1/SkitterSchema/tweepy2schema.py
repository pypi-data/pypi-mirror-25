from SkitterSchema.twitter_schema import User, Entity, Status, UUEdge, USEdge, SSEdge, ESEdge, EUEdge
from SkitterSchema.util import extract_hashtags, Dict2Obj
from urllib.parse import urlparse


class ProcessedOutcome:
    def __init__(self):
        self.schema_users = []
        self.schema_tweets = []
        self.schema_entities = []
        self.schema_edges = []

    def __repr__(self):
        return "{0}\n{1}\n{2}\n{3}\n".format(self.schema_users,
                                             self.schema_tweets,
                                             self.schema_entities,
                                             self.schema_edges)

    def __add__(self, other):

        if type(other) == User:
            self.schema_users += [other]

        if type(other) == Status:
            self.schema_tweets += [other]

        if type(other) == Entity:
            self.schema_entities += [other]

        if type(other) in [UUEdge, USEdge, SSEdge, ESEdge, EUEdge]:
            self.schema_edges += [other]

        if type(other) == ProcessedOutcome:
            self.schema_users += other.schema_users
            self.schema_tweets += other.schema_tweets
            self.schema_entities += other.schema_entities
            self.schema_edges += other.schema_edges

        return self

    def last_user(self):
        return self.schema_users[-1]

    def add_user(self, user):
        self.schema_users.append(user)

    def last_status(self):
        return self.schema_tweets[-1]

    def add_status(self, tweet):
        self.schema_tweets.append(tweet)

    def last_entity(self):
        return self.schema_entities[-1]

    def add_entity(self, entity):
        self.schema_entities.append(entity)

    def last_edge(self):
        return self.schema_edges[-1]

    def add_edge(self, edge):
        self.schema_edges.append(edge)

    def add_to_session(self, session):
        for i in self.schema_users + self.schema_tweets + self.schema_edges + self.schema_entities:
            session.merge(i)


def compare_user(schema_user, tweepy_user):
    """ Compares a schema User, defined in twitter_schema.py with a tweepy User.
    :param schema_user: TwitterSchema User.
    :param tweepy_user: tweepy User.
    :return: whether all the attributes are the same.
    """

    return \
        schema_user.id == tweepy_user.id and schema_user.statuses_count == tweepy_user.statuses_count and \
        schema_user.followers_count == tweepy_user.followers_count and \
        schema_user.followees_count == tweepy_user.friends_count and \
        schema_user.favorites_count == tweepy_user.favourites_count and \
        schema_user.listed_count == tweepy_user.listed_count and \
        schema_user.screen_name == tweepy_user.screen_name and \
        schema_user.name == tweepy_user.name and \
        schema_user.description == tweepy_user.description and \
        schema_user.lang == tweepy_user.lang and \
        schema_user.time_zone == tweepy_user.time_zone and \
        schema_user.location == tweepy_user.location and \
        schema_user.profile_image_url == tweepy_user.profile_image_url and \
        schema_user.default_profile == tweepy_user.default_profile and \
        schema_user.default_profile_image == tweepy_user.default_profile_image and \
        schema_user.geo_enabled == tweepy_user.geo_enabled and \
        schema_user.verified == tweepy_user.verified


def process_url(url):
    outcome = ProcessedOutcome()
    schema_entity_url = Entity.get_new_url(url="".join(urlparse(url['expanded_url'])[1:]))
    outcome.add_entity(schema_entity_url)
    return outcome


def process_domain(url):
    outcome = ProcessedOutcome()

    schema_entity_domain = Entity.get_new_domain(domain=urlparse(url['expanded_url']).netloc)
    outcome.add_entity(schema_entity_domain)
    return outcome


def process_hashtag(hashtag):
    outcome = ProcessedOutcome()
    schema_entity_hashtag = Entity.get_new_hashtag(hashtag="#" + hashtag['text'])
    outcome.add_entity(schema_entity_hashtag)
    return outcome


def process_media(media):
    outcome = ProcessedOutcome()
    schema_entity_media = Entity.get_new_media(media="".join(urlparse(media['media_url'])[1:]))
    outcome.add_entity(schema_entity_media)
    return outcome


def process_user(user):
    """ This function receives a twitter user and creates a User object that can be stored, as well as its mentions and
    hashtags. Currently, it does not store any of the mentions in the description, as this would require another call
    from the api, but it is something to think about.
    :param user: tweepy User object.
    :return: ProcessedOutcome user object.
    """

    if type(user) is dict:
        user = Dict2Obj(user)

    outcome = ProcessedOutcome()

    # Gets User
    this_user = User(id=user.id, statuses_count=user.statuses_count, followers_count=user.followers_count,
                     followees_count=user.friends_count, favorites_count=user.favourites_count,
                     listed_count=user.listed_count, screen_name=user.screen_name, name=user.name,
                     description=user.description, location=user.location, profile_image_url=user.profile_image_url,
                     time_zone=user.time_zone, lang=user.lang, default_profile=user.default_profile,
                     default_profile_image=user.default_profile_image, geo_enabled=user.geo_enabled,
                     verified=user.verified, created_at=user.created_at)

    outcome.add_user(this_user)

    if 'url' in user.entities and 'urls' in user.entities['url']:
        for url in user.entities['url']['urls']:
            if 'expanded_url' in url and url['expanded_url'] is not None:
                if urlparse(url['expanded_url']).netloc == "twitter.com":
                    continue
                outcome += process_url(url)
                outcome += EUEdge.get_ueedge(outcome.last_entity().content, this_user.id, outcome.last_entity().kind)

                outcome += process_domain(url)
                outcome += EUEdge.get_ueedge(outcome.last_entity().content, this_user.id, outcome.last_entity().kind)

    # Gets Hashtags
    hashtags = extract_hashtags(user.description)
    for hashtag in hashtags:
        outcome += process_hashtag(hashtag)
        outcome += EUEdge.get_ueedge(outcome.last_entity().content, this_user.id, outcome.last_entity().kind)

    return outcome


def process_status(status):
    if type(status) is dict:
        status = Dict2Obj(status)

    outcome = ProcessedOutcome()

    # Initialization - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
    # Adds: - tweeting_user
    tmp = process_user(status.user)
    this_user = tmp.schema_users[0]
    outcome += tmp

    # Adds : - tweeted_status (PARTIAL)
    this_status = Status(id=status.id, favorite_count=status.favorite_count, retweet_count=status.retweet_count,
                         text=status.text, lang=status.lang, coordinates=str(status.coordinates),
                         source=status.source, created_at=status.created_at)

    # Gets Retweet (AND TERMINATES) - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
    # Adds: - retweeted_status/user/entities/edges
    #       - tweeting_user --rt--> retweeted_status
    #       - tweeting_user --rt--> retweeted_user
    if hasattr(status, 'retweeted_status'):
        # Add status
        outcome += process_status(status.retweeted_status)

        # Add edges
        outcome.add_edge(UUEdge.get_retweet_uuedge(this_user.id, outcome.last_user().id))  # User to user
        outcome.add_edge(USEdge.get_retweet_usedge(this_user.id, outcome.last_status().id))  # User to status

        return outcome

    # Gets Quoted Status - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
    # Adds: - quoted_status/user/entities/edges
    #       - tweeting_user  --qt--> quoted_status
    #       - tweeting_user  --qt--> quoted_user
    #       - tweeted_status --qt--> quoted_status
    if hasattr(status, 'quoted_status'):
        outcome += process_status(status.quoted_status)
        outcome += USEdge.get_quote_usedge(this_user.id, outcome.last_status().id)
        outcome += UUEdge.get_quote_uuedge(this_user.id, outcome.last_user().id)
        outcome += SSEdge.get_quote_ssedge(this_status.id, outcome.last_status().id)

    # Gets Normal Tweets, Quotes and Replies - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
    # Adds: - tweeted_status (COMPLETES)
    outcome += this_status
    outcome += USEdge.get_tweet_usedge(this_user.id, this_status.id)

    # Adds: - url_entity*/domain_entity*
    #       - this_user   <--> url_entity/domain_entity
    #       - this_status <--> url_entity/domain_entity
    if 'urls' in status.entities:
        for url in status.entities['urls']:
            if 'expanded_url' in url and url['expanded_url'] is not None:
                if urlparse(url['expanded_url']).netloc == "twitter.com":
                    continue
                outcome += process_url(url)
                outcome += EUEdge.get_ueedge(outcome.last_entity().content, this_user.id, outcome.last_entity().kind)
                outcome += ESEdge.get_esedge(outcome.last_entity().content, this_status.id, outcome.last_entity().kind)
                outcome += process_domain(url)
                outcome += EUEdge.get_ueedge(outcome.last_entity().content, this_user.id, outcome.last_entity().kind)
                outcome += ESEdge.get_esedge(outcome.last_entity().content, this_status.id, outcome.last_entity().kind)

    # Adds: - hashtag_entity*
    #       - this_user   <--> hashtag_entity
    #       - this_status <--> hashtag_entity
    if 'hashtags' in status.entities:
        for hashtag in status.entities['hashtags']:
            outcome += process_hashtag(hashtag)
            outcome += EUEdge.get_ueedge(outcome.last_entity().content, this_user.id, outcome.last_entity().kind)
            outcome += ESEdge.get_esedge(outcome.last_entity().content, this_status.id, outcome.last_entity().kind)

    # Adds: - media_entity*
    #       - this_user   <--> media_entity
    #       - this_status <--> media_entity
    if 'media' in status.entities:
        for media in status.entities['media']:
            outcome += process_media(media)
            outcome += EUEdge.get_ueedge(outcome.last_entity().content, this_user.id, outcome.last_entity().kind)
            outcome += ESEdge.get_esedge(outcome.last_entity().content, this_status.id, outcome.last_entity().kind)

    # Adds: - this_status -mt-> mentioned_user
    #       - this_user   -mt-> mentioned_user
    if 'user_mentions' in status.entities:
        for user_mention in status.entities['user_mentions']:
            outcome += UUEdge.get_mention_uuedge(this_user.id, user_mention['id'])
            outcome += USEdge.get_mention_usedge(user_mention['id'], this_status.id)

    # Adds: - this_user -mt-> replied_user
    #       - this_status   -mt-> replied_status
    if hasattr(status, 'in_reply_to_user_id') and status.in_reply_to_user_id is not None:
        outcome += UUEdge.get_reply_uuedge(this_user.id, status.in_reply_to_user_id)
        outcome += SSEdge.get_reply_ssedge(this_status.id, status.in_reply_to_status_id)

    return outcome


def process_timeline(timeline):
    outcome = ProcessedOutcome()

    for status in timeline:
        outcome += process_status(status)

    return outcome


def process_favourites(favorites, user):
    outcome = ProcessedOutcome()

    for status in favorites:
        outcome += process_status(status)
        outcome += UUEdge.get_favorite_uuedge(user.id, outcome.last_user().id)
        outcome += USEdge.get_favorite_usedge(user.id, outcome.last_status().id)

    return outcome


def process_followers(followers, user):
    outcome = ProcessedOutcome()

    for follower in followers:
        outcome += UUEdge.get_follow_uuedge(follower, user.id)

    return outcome


def process_followees(followees, user):
    outcome = ProcessedOutcome()

    for followee in followees:
        outcome += UUEdge.get_follow_uuedge(user.id, followee)

    return outcome
