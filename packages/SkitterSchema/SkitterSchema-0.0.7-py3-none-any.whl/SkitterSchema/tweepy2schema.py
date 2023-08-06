from SkitterSchema.twitter_schema import User, Entity, Status, UUEdge, USEdge, SSEdge, ESEdge, EUEdge
from SkitterSchema.util import extract_hashtags, Dict2Obj, remove_mentions, get_edges
from urllib.parse import urlparse


def process_url(url):
    outcome = ProcessedOutcome()
    url = "".join(urlparse(url['expanded_url'])[1:])
    schema_entity_url = Entity.get_new_url(url="".join(url[:255]))
    outcome.add_entity(schema_entity_url)
    return outcome, schema_entity_url


def process_domain(url):
    outcome = ProcessedOutcome()
    url = urlparse(url['expanded_url']).netloc
    schema_entity_domain = Entity.get_new_domain(domain=url[:255])
    outcome.add_entity(schema_entity_domain)
    return outcome, schema_entity_domain


def process_hashtag(hashtag):
    outcome = ProcessedOutcome()
    schema_entity_hashtag = Entity.get_new_hashtag(hashtag="#" + hashtag['text'])
    outcome.add_entity(schema_entity_hashtag)
    return outcome, schema_entity_hashtag


def process_media(media):
    outcome = ProcessedOutcome()
    media = "".join(urlparse(media['expanded_url'])[1:])
    schema_entity_media = Entity.get_new_media(media="".join(media[:255]))
    outcome.add_entity(schema_entity_media)
    return outcome, schema_entity_media


def process_timeline(timeline, user_id, extended=True):
    outcome = ProcessedOutcome()
    for status in timeline:
        _outcome, _, _ = process_status(status, extended, flag='tl')
        outcome += _outcome
    return outcome


def process_favourites(favorites, user_id, extended=True):
    outcome = ProcessedOutcome()
    for status in favorites:
        _outcome, schema_status, schema_user = process_status(status, extended, flag='fv')
        outcome += _outcome
        outcome += UUEdge.get_favorite_uuedge(user_id, schema_user.id)
        outcome += USEdge.get_favorite_usedge(user_id, schema_status.id)
    return outcome


def process_followers(followers, user_id):
    outcome = ProcessedOutcome()
    for follower in followers:
        outcome += UUEdge.get_follow_uuedge(follower, user_id)
    return outcome


def process_followees(followees, user_id):
    outcome = ProcessedOutcome()
    for followee in followees:
        outcome += UUEdge.get_follow_uuedge(user_id, followee)
    return outcome


def process_user(user, flag="nil"):

    if type(user) is dict:
        user = Dict2Obj(user)

    outcome = ProcessedOutcome()

    # > < > < > < > < > < > < > < > < > < > < > < > < > < > < > < > < > < > < > < > < > < > < > < > < > < > < > < > < >
    # > > > > > > > > > > > > > > > > > > > > > > > > > > Gets User < < < < < < < < < < < < < < < < < < < < < < < < < <
    # > < > < > < > < > < > < > < > < > < > < > < > < > < > < > < > < > < > < > < > < > < > < > < > < > < > < > < > < >

    # Adds : - user
    this_user = User(id=user.id, statuses_count=user.statuses_count, followers_count=user.followers_count,
                     followees_count=user.friends_count, favorites_count=user.favourites_count,
                     listed_count=user.listed_count, screen_name=user.screen_name, name=user.name,
                     description=user.description, location=user.location, profile_image_url=user.profile_image_url,
                     time_zone=user.time_zone, lang=user.lang, default_profile=user.default_profile,
                     default_profile_image=user.default_profile_image, geo_enabled=user.geo_enabled,
                     verified=user.verified, created_at=user.created_at, flag=flag)
    outcome.add_user(this_user)

    # Adds: - url_entity*/domain_entity*
    #       - user   <--> url_entity/domain_entity
    if 'url' in user.entities and 'urls' in user.entities['url']:
        for url in user.entities['url']['urls']:
            if 'expanded_url' in url and url['expanded_url'] is not None:
                if urlparse(url['expanded_url']).netloc == "twitter.com":
                    continue
                _outcome, schema_entity_url = process_url(url)
                outcome += _outcome
                outcome += EUEdge.get_ueedge(schema_entity_url.content, this_user.id, schema_entity_url.kind)

                _outcome, schema_entity_domain = process_domain(url)
                outcome += _outcome
                outcome += EUEdge.get_ueedge(schema_entity_domain.content, this_user.id, schema_entity_domain.kind)

    # Adds: - hashtag_entity*
    #       - user   <--> hashtag_entity
    hashtags = extract_hashtags(user.description)
    for hashtag in hashtags:
        _outcome, schema_entity_hashtag = process_hashtag(hashtag)
        outcome += _outcome
        outcome += EUEdge.get_ueedge(schema_entity_hashtag.content, this_user.id, schema_entity_hashtag.kind)

    return outcome, this_user


def process_status(status, extended=True, flag="nil"):
    if type(status) is dict:
        status = Dict2Obj(status)

    outcome = ProcessedOutcome()

    # Adds: - tweeting_user
    _outcome, this_user = process_user(status.user)
    outcome += _outcome

    # Adds : - tweeted_status (PARTIAL)
    text = status.full_text if extended else status.text
    text = remove_mentions(text)[:350]
    this_status = Status(id=status.id, favorite_count=status.favorite_count, retweet_count=status.retweet_count,
                         text=text if extended else status.text, lang=status.lang,
                         coordinates=str(status.coordinates), source=status.source, created_at=status.created_at,
                         flag=flag)

    # > < > < > < > < > < > < > < > < > < > < > < > < > < > < > < > < > < > < > < > < > < > < > < > < > < > < > < > < >
    # > > > > > > > > > > > > > > > > > > > > > Gets Retweet (AND TERMINATES) < < < < < < < < < < < < < < < < < < < < <
    # > < > < > < > < > < > < > < > < > < > < > < > < > < > < > < > < > < > < > < > < > < > < > < > < > < > < > < > < >

    # Adds: - retweeted_status/user/entities/edges
    #       - tweeting_user --rt--> retweeted_status
    #       - tweeting_user --rt--> retweeted_user
    if hasattr(status, 'retweeted_status'):
        # Add status
        _outcome, schema_status, schema_user = process_status(status.retweeted_status, extended, flag="rt")
        outcome += _outcome
        # Add edges
        outcome.add_edge(UUEdge.get_retweet_uuedge(this_user.id, schema_user.id))  # User to user
        outcome.add_edge(USEdge.get_retweet_usedge(this_user.id, schema_status.id))  # User to status

        return outcome, schema_status, schema_user

    # > < > < > < > < > < > < > < > < > < > < > < > < > < > < > < > < > < > < > < > < > < > < > < > < > < > < > < > < >
    # > > > > > > > > > > > > > > > > > > > > > > > Gets Quoted Status  < < < < < < < < < < < < < < < < < < < < < < < <
    # > < > < > < > < > < > < > < > < > < > < > < > < > < > < > < > < > < > < > < > < > < > < > < > < > < > < > < > < >

    # Adds: - quoted_status/user/entities/edges
    #       - tweeting_user  --qt--> quoted_status
    #       - tweeting_user  --qt--> quoted_user
    #       - tweeted_status --qt--> quoted_status
    if hasattr(status, 'quoted_status'):
        _outcome, schema_status, schema_user = process_status(status.quoted_status, extended, flag="qt")
        outcome += _outcome

        outcome += USEdge.get_quote_usedge(this_user.id, schema_status.id)
        outcome += UUEdge.get_quote_uuedge(this_user.id, schema_user.id)
        outcome += SSEdge.get_quote_ssedge(this_status.id, schema_status.id)

    # > < > < > < > < > < > < > < > < > < > < > < > < > < > < > < > < > < > < > < > < > < > < > < > < > < > < > < > < >
    # > > > > > > > > > > > > > > > > > > > > > > > Gets Normal Status  < < < < < < < < < < < < < < < < < < < < < < < <
    # > < > < > < > < > < > < > < > < > < > < > < > < > < > < > < > < > < > < > < > < > < > < > < > < > < > < > < > < >

    # Gets Normal Tweets, Quotes and Replies
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
                _outcome, schema_entity_url = process_url(url)
                outcome += _outcome
                outcome += EUEdge.get_ueedge(schema_entity_url.content, this_user.id, schema_entity_url.kind)
                outcome += ESEdge.get_esedge(schema_entity_url.content, this_status.id, schema_entity_url.kind)

                _outcome, schema_entity_domain = process_domain(url)
                outcome += _outcome
                outcome += EUEdge.get_ueedge(schema_entity_domain.content, this_user.id, schema_entity_domain.kind)
                outcome += ESEdge.get_esedge(schema_entity_domain.content, this_status.id, schema_entity_domain.kind)

    # Adds: - hashtag_entity*
    #       - this_user   <--> hashtag_entity
    #       - this_status <--> hashtag_entity
    if 'hashtags' in status.entities:
        for hashtag in status.entities['hashtags']:
            _outcome, schema_entity_hashtag = process_hashtag(hashtag)
            outcome += _outcome
            outcome += EUEdge.get_ueedge(schema_entity_hashtag.content, this_user.id, schema_entity_hashtag.kind)
            outcome += ESEdge.get_esedge(schema_entity_hashtag.content, this_status.id, schema_entity_hashtag.kind)

    # Adds: - media_entity*
    #       - this_user   <--> media_entity
    #       - this_status <--> media_entity
    if 'media' in status.entities:
        for media in status.entities['media']:
            _outcome, schema_entity_media = process_media(media)
            outcome += _outcome
            outcome += EUEdge.get_ueedge(schema_entity_media.content, this_user.id, schema_entity_media.kind)
            outcome += ESEdge.get_esedge(schema_entity_media.content, this_status.id, schema_entity_media.kind)

    # Adds: - this_status -mt-> mentioned_user
    #       - this_user   -mt-> mentioned_user
    if 'user_mentions' in status.entities:
        for user_mention in status.entities['user_mentions']:
            outcome += UUEdge.get_mention_uuedge(this_user.id, user_mention['id'])
            outcome += USEdge.get_mention_usedge(user_mention['id'], this_status.id)

    # Adds: - this_user -mt-> replied_user
    #       - this_status   -mt-> replied_status
    if hasattr(status, 'in_reply_to_user_id') and \
                    status.in_reply_to_user_id is not None and \
                    status.in_reply_to_status_id is not None:
        outcome += UUEdge.get_reply_uuedge(this_user.id, status.in_reply_to_user_id)
        outcome += USEdge.get_reply_usedge(this_user.id,  status.in_reply_to_status_id)
        outcome += SSEdge.get_reply_ssedge(this_status.id, status.in_reply_to_status_id)

    return outcome, this_status, this_user


class ProcessedOutcome:
    def __init__(self):
        self.schema_users = []
        self.schema_tweets = []
        self.schema_entities = []
        self.schema_edges = []

    def __repr__(self):
        return "{0}\n{1}\n{2}\n{3}\n".format(self.schema_users,  self.schema_tweets,
                                             self.schema_entities, self.schema_edges)

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

    def add_user(self, user):
        self.schema_users.append(user)

    def add_status(self, tweet):
        self.schema_tweets.append(tweet)

    def add_entity(self, entity):
        self.schema_entities.append(entity)

    def add_edge(self, edge):
        self.schema_edges.append(edge)

    def add_to_session(self, session):
        for i in self.schema_users + self.schema_tweets + self.schema_edges + self.schema_entities:
            try:
                session.merge(i)
            except Exception as e:
                print(e)
                session.rollback()

    def exist_user(self, user_id):
        for user in self.schema_users:
            if user.id == user_id:
                return True
        return False

    def exist_status(self, status_id):
        for tweet in self.schema_tweets:
            if tweet.id == status_id:
                return True
        return False

    def get_filtered_edges(self, type_edge, kind, func=lambda x: x):
        edges = []
        for edge in self.schema_edges:
            if type(edge) == type_edge and edge.kind == kind:
                edges.append(func(edge))
        return edges


def assert_processed_outcome(outcome, user_id):

    # Nothing to see here, seed will restart
    if len(outcome.schema_tweets) == 0:
        return

    tweet_us_edges = outcome.get_filtered_edges(USEdge, 'tweet', lambda x: (x.user, x.status))
    retweet_us_edges = outcome.get_filtered_edges(USEdge, 'retweet', lambda x: (x.user, x.status))
    retweet_uu_edges = outcome.get_filtered_edges(UUEdge, 'retweet', lambda x: (x.src_id, x.dst_id))
    quote_uu_edges = outcome.get_filtered_edges(UUEdge, 'quote', lambda x: (x.src_id, x.dst_id))
    quote_us_edges = outcome.get_filtered_edges(USEdge, 'quote', lambda x: (x.user, x.status))
    quote_ss_edges = outcome.get_filtered_edges(SSEdge, 'quote', lambda x: (x.src_id, x.dst_id))
    favorite_us_edges = outcome.get_filtered_edges(USEdge, 'favorite', lambda x: (x.user, x.status))
    favorite_uu_edges = outcome.get_filtered_edges(UUEdge, 'favorite', lambda x: (x.src_id, x.dst_id))

    assert outcome.exist_user(user_id), "checks user tl"

    # for each status
    for status in outcome.schema_tweets:

        if status.flag == 'tl':
            assert (user_id, status.id) in tweet_us_edges, "missing user_tl -tweet-> status edge \n {0}".format(status.id)

        if status.flag == 'fav':
            assert (user_id, status.id) in favorite_us_edges, "missing user_tl -fav-> status edge\n {0}".format(status.id)
            us_edge = get_edges(status.id, tweet_us_edges, lambda edge, id_v: edge[1] == id_v)
            assert len(us_edge) != 0, "single tweet yet zero other users who tweeted them\n {0}".format(status.id)
            assert len(us_edge) <= 1, "single tweet yet multiple other users who tweeted them\n {0}".format(status.id)

            other_user_id = us_edge[0][0]
            assert outcome.exist_user(other_user_id), "other user doest not exist in the outcome\n {0}".format(status.id)
            assert (user_id, other_user_id) in favorite_uu_edges, "missing user_tl -fav-> user_other edge\n {0}".format(status.id)

        if status.flag == 'rt':
            assert (user_id, status.id) in retweet_us_edges, "missing user_tl -retweet-> status edge\n {0}".format(status.id)

            us_edge = get_edges(status.id, tweet_us_edges, lambda edge, id_v: edge[1] == id_v)
            assert len(us_edge) != 0, "single tweet yet zero other users who tweeted them\n {0}".format(status.id)
            assert len(us_edge) <= 1, "single tweet yet multiple other users who tweeted them\n {0}".format(status.id)

            other_user_id = us_edge[0][0]

            assert outcome.exist_user(other_user_id), "other user doest not exist in the outcome\n {0}".format(status.id)
            assert (user_id, other_user_id) in retweet_uu_edges, "missing user_tl -retweet-> user_other edge\n {0}".format(status.id)

        if status.flag == 'qt':
            direct_quote, retweet_quote = (user_id, status.id) in quote_us_edges, False
            us_edge = get_edges(status.id, tweet_us_edges, lambda edge, id_v: edge[1] == id_v)
            other_user_id = us_edge[0][0]
            assert len(us_edge) != 0, "single tweet yet zero other users who tweeted them\n {0}".format(status.id)
            assert len(us_edge) <= 1, "single tweet yet multiple other users who tweeted them\n {0}".format(status.id)
            assert outcome.exist_user(other_user_id), "other user don't exist in the outcome\n {0}".format(status.id)

            ss_edges = get_edges(status.id, quote_ss_edges, lambda edge, id_v: edge[1] == id_v)
            assert len(ss_edges) != 0, "single tweet yet zero other users who tweeted them\n {0}".format(status.id)
            for ss_edge in ss_edges:
                assert outcome.exist_status(ss_edge[0]), "statuses user don't exist in the outcome\n {0}".format(status.id)

            if direct_quote:
                assert (user_id, other_user_id) in quote_uu_edges, "missing user -quote-> other user edge\n {0}".format(status.id)
                assert (user_id, status.id) in quote_us_edges, "missing user -quote-> other tweet\n {0}".format(status.id)

                user_check = False
                for ss_edge in ss_edges:
                    us_edge = get_edges(ss_edge[0], tweet_us_edges, lambda edge, id_v: edge[1] == id_v)
                    other_user_id = us_edge[0][0]
                    assert len(us_edge) != 0, "single tweet yet zero other users who tweeted them\n {0}".format(status.id)
                    assert len(us_edge) <= 1, "single tweet yet multiple other users who tweeted them\n {0}".format(status.id)
                    assert outcome.exist_user(other_user_id), "other user don't exist in the outcome\n {0}".format(status.id)

                    if other_user_id == user_id:
                        user_check = True

                assert user_check, "missing very complicated stuff\n {0}".format(status.id)

            if direct_quote is False:

                user_check_rt = False
                for ss_edge in ss_edges:

                    us_edge = get_edges(ss_edge[0], tweet_us_edges, lambda edge, id_v: edge[1] == id_v)
                    other_user_id = us_edge[0][0]
                    assert len(us_edge) != 0, "single tweet yet zero other users who tweeted them\n {0}".format(status.id)
                    assert len(us_edge) <= 1, "single tweet yet multiple other users who tweeted them\n {0}".format(status.id)
                    assert outcome.exist_user(other_user_id), "other user don't exist in the outcome\n {0}".format(status.id)

                    if (other_user_id, status.id) in quote_us_edges:

                        uu_edges = get_edges(other_user_id, retweet_uu_edges,
                                             lambda edge, id_v: edge[1] == other_user_id)

                        for uu_edge in uu_edges:
                            assert outcome.exist_user(uu_edge[0]), "other user don't exist in the outcome\n {0}".format(status.id)

                            if (uu_edge[0], ss_edge[0]) in retweet_us_edges:
                                user_check_rt = True

                user_check_fv = False
                for ss_edge in ss_edges:

                    us_edge = get_edges(ss_edge[0], tweet_us_edges, lambda edge, id_v: edge[1] == id_v)
                    other_user_id = us_edge[0][0]
                    assert len(us_edge) != 0, "single tweet yet zero other users who tweeted them\n {0}".format(status.id)
                    assert len(us_edge) <= 1, "single tweet yet multiple other users who tweeted them\n {0}".format(status.id)
                    assert outcome.exist_user(other_user_id), "other user don't exist in the outcome\n {0}".format(status.id)

                    if (other_user_id, status.id) in quote_us_edges:

                        uu_edges = get_edges(other_user_id, favorite_uu_edges,
                                             lambda edge, id_v: edge[1] == other_user_id)

                        for uu_edge in uu_edges:
                            assert outcome.exist_user(uu_edge[0]), "other user don't exist in the outcome\n {0}".format(status.id)

                            if (uu_edge[0], ss_edge[0]) in favorite_us_edges:
                                user_check_fv = True

                assert user_check_rt or user_check_fv, "missing very complicated stuff\n {0}".format(status.id)
