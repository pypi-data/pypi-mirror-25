from sqlalchemy import Column, Integer, String, DateTime, BigInteger, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()


class ESEdge(Base):
    __tablename__ = 'esedges'
    entity = Column(String(256), primary_key=True)
    kind = Column(String(16), primary_key=True)
    status = Column(BigInteger, primary_key=True)

    def __repr__(self):
        return "<entity:{0}, status:{1}, kind:{2}>".format(self.entity,
                                                           self.status,
                                                           self.kind)

    @staticmethod
    def get_esedge(entity_content,
                   status_id,
                   entity_kind):
        return ESEdge(entity=entity_content,
                      status=status_id,
                      kind=entity_kind)

    @staticmethod
    def build_rel(src, kind):
        if src == "Status":
            return relationship("Entity", secondary='esedges',
                                primaryjoin="and_(Status.id==ESEdge.status, ESEdge.kind=='{0}')".format(kind),
                                secondaryjoin="and_(Entity.content==ESEdge.entity, ESEdge.kind==ESEdge.kind)".format(kind))
        elif src == "Entity":
            return relationship("Status",
                                secondary='esedges',
                                primaryjoin="and_(Entity.content==ESEdge.entity, ESEdge.kind=='{0}')".format(kind),
                                secondaryjoin="and_(Status.id==ESEdge.status, ESEdge.kind==ESEdge.kind)")


class EUEdge(Base):
    __tablename__ = 'euedges'

    entity = Column(String(256), primary_key=True)
    kind = Column(String(16), primary_key=True)
    user = Column(BigInteger, primary_key=True)

    def __repr__(self):
        return "<entity:{0}, user:{1}, kind:{2}>".format(self.entity,
                                                         self.user,
                                                         self.kind)

    @staticmethod
    def get_ueedge(entity_content,
                   user_id,
                   entity_kind):
        return EUEdge(entity=entity_content,
                      user=user_id,
                      kind=entity_kind)

    @staticmethod
    def build_rel(src, kind):
        if src == "User":
            return relationship("Entity", secondary='euedges',
                                primaryjoin="and_(User.id==EUEdge.user, EUEdge.kind=='{0}')".format(kind),
                                secondaryjoin="and_(Entity.content==EUEdge.entity, Entity.kind==EUEdge.kind)")
        elif src == "Entity":
            return relationship("User", secondary='euedges',
                                primaryjoin="and_(Entity.content==EUEdge.entity, EUEdge.kind=='{0}')".format(kind),
                                secondaryjoin="and_(User.id==EUEdge.user, EUEdge.kind==EUEdge.kind)".format(kind))


class SSEdge(Base):
    __tablename__ = 'ssedges'

    src_id = Column(BigInteger, primary_key=True)
    dst_id = Column(BigInteger, primary_key=True)
    kind = Column(String(16), primary_key=True)

    def __repr__(self):
        return "<src:{0}, dst:{1}, kind:{2}>".format(self.src_id,
                                                     self.dst_id,
                                                     self.kind)

    @staticmethod
    def get_reply_ssedge(src_id,
                         dst_id):
        return SSEdge(src_id=src_id,
                      dst_id=dst_id,
                      kind="reply")

    @staticmethod
    def get_quote_ssedge(src_id,
                         dst_id):
        return SSEdge(src_id=src_id,
                      dst_id=dst_id,
                      kind="quote")

    @staticmethod
    def j_me(condition, kind):
        tmp = "Status.id==SSEdge.dst_id" if condition == 'primary' else "Status.id==SSEdge.src_id"
        return "and_({0}, SSEdge.kind=='{1}')".format(tmp, kind)

    @staticmethod
    def j_by_me(condition, kind):
        tmp = "Status.id==SSEdge.dst_id" if condition == 'secondary' else "Status.id==SSEdge.src_id"
        return "and_({0}, SSEdge.kind=='{1}')".format(tmp, kind)

    @staticmethod
    def build_rel(condition, kind):
        if condition == "me":
            return relationship("Status", secondary='ssedges', primaryjoin=SSEdge.j_me('primary', kind),
                                secondaryjoin=SSEdge.j_me('secondary', kind))
        elif condition == "by_me":
            return relationship("Status", secondary='ssedges', primaryjoin=SSEdge.j_by_me('primary', kind),
                                secondaryjoin=SSEdge.j_by_me('secondary', kind))


class USEdge(Base):
    __tablename__ = 'usedges'

    user = Column(BigInteger, primary_key=True)
    status = Column(BigInteger, primary_key=True)
    kind = Column(String(16), primary_key=True)

    def __repr__(self):
        return "<user:{0}, status:{1}, kind:{2}>".format(self.user,
                                                         self.status,
                                                         self.kind)

    @staticmethod
    def get_tweet_usedge(user,
                         status):
        return USEdge(user=user,
                      status=status,
                      kind="tweet")

    @staticmethod
    def get_retweet_usedge(user,
                           status):
        return USEdge(user=user,
                      status=status,
                      kind="retweet")

    @staticmethod
    def get_quote_usedge(user,
                         status):
        return USEdge(user=user,
                      status=status,
                      kind="quote")

    @staticmethod
    def get_reply_usedge(user,
                         status):
        return USEdge(user=user,
                      status=status,
                      kind="reply")

    @staticmethod
    def get_favorite_usedge(user,
                            status):
        return USEdge(user=user,
                      status=status,
                      kind="favorite")

    @staticmethod
    def get_mention_usedge(user,
                           status):
        return USEdge(user=user,
                      status=status,
                      kind="mention")

    @staticmethod
    def build_rel(src, kind):
        if src == "User":
            return relationship("Status", secondary='usedges',
                                primaryjoin="and_(User.id==USEdge.user, USEdge.kind=='{0}')".format(kind),
                                secondaryjoin="and_(Status.id==USEdge.status, USEdge.kind=='{0}')".format(kind))
        elif src == "Status":
            return relationship("User", secondary='usedges',
                                primaryjoin="and_(Status.id==USEdge.status, USEdge.kind=='{0}')".format(kind),
                                secondaryjoin="and_(User.id==USEdge.user, USEdge.kind=='{0}')".format(kind))


class UUEdge(Base):
    __tablename__ = 'uuedges'

    src_id = Column(BigInteger, primary_key=True)
    dst_id = Column(BigInteger, primary_key=True)
    kind = Column(String(16), primary_key=True)

    def __repr__(self):
        return "<src:{0}, dst:{1}, kind:{2}>".format(self.src_id,
                                                     self.dst_id,
                                                     self.kind)

    @staticmethod
    def get_follow_uuedge(src_user,
                          dst_user):
        return UUEdge(src_id=src_user,
                      dst_id=dst_user,
                      kind="follow")

    @staticmethod
    def get_favorite_uuedge(src_user,
                            dst_user):
        return UUEdge(src_id=src_user,
                      dst_id=dst_user,
                      kind="favorite")

    @staticmethod
    def get_reply_uuedge(src_user,
                         dst_user):
        return UUEdge(src_id=src_user,
                      dst_id=dst_user,
                      kind="reply")

    @staticmethod
    def get_retweet_uuedge(src_user,
                           dst_user):
        return UUEdge(src_id=src_user,
                      dst_id=dst_user,
                      kind="retweet")

    @staticmethod
    def get_quote_uuedge(src_user,
                         dst_user):
        return UUEdge(src_id=src_user,
                      dst_id=dst_user,
                      kind="quote")

    @staticmethod
    def get_mention_uuedge(src_user,
                           dst_user):
        return UUEdge(src_id=src_user,
                      dst_id=dst_user,
                      kind="mention")

    @staticmethod
    def j_me(condition, kind):
        tmp = "User.id==UUEdge.dst_id" if condition == 'primary' else "User.id==UUEdge.src_id"
        return "and_({0}, UUEdge.kind=='{1}')".format(tmp, kind)

    @staticmethod
    def j_by_me(condition, kind):
        tmp = "User.id==UUEdge.dst_id" if condition == 'secondary' else "User.id==UUEdge.src_id"
        return "and_({0}, UUEdge.kind=='{1}')".format(tmp, kind)

    @staticmethod
    def build_rel(condition, kind):
        if condition == "me":
            return relationship("User", secondary='uuedges',
                                primaryjoin=UUEdge.j_me("primary", kind),
                                secondaryjoin=UUEdge.j_me("secondary", kind))
        elif condition == "by_me":
            return relationship("User", secondary='uuedges',
                                primaryjoin=UUEdge.j_by_me("primary", kind),
                                secondaryjoin=UUEdge.j_by_me("secondary", kind))


class Entity(Base):
    __tablename__ = 'entities'

    content = Column(String(256), primary_key=True)
    kind = Column(String(16), primary_key=True)

    @staticmethod
    def get_new_url(url):
        return Entity(content=url, kind="url")

    @staticmethod
    def get_new_domain(domain):
        return Entity(content=domain, kind="domain")

    @staticmethod
    def get_new_hashtag(hashtag):
        return Entity(content=hashtag, kind="hashtag")

    @staticmethod
    def get_new_media(media):
        return Entity(content=media, kind="media")

    @staticmethod
    def get_new_regex(regex_match):  # this is just in case some day I find it useful
        return Entity(content=regex_match, kind="regex")

    def __repr__(self):
        return "<kind:{0}, content:{1}>".format(self.kind, self.content)

    # >> EUEdge
    u_url_me = EUEdge.build_rel("Entity", "url")
    u_domain_me = EUEdge.build_rel("Entity", "domain")
    u_hashtag_me = EUEdge.build_rel("Entity", "hashtag")
    u_media_me = EUEdge.build_rel("Entity", "media")
    u_regex_me = EUEdge.build_rel("Entity", "regex")

    # >> ESEdge
    s_url_me = ESEdge.build_rel("Entity", "url")
    s_domain_me = ESEdge.build_rel("Entity", "domain")
    s_hashtag_me = ESEdge.build_rel("Entity", "hashtag")
    s_media_me = ESEdge.build_rel("Entity", "media")
    s_regex_me = ESEdge.build_rel("Entity", "regex")


class User(Base):
    __tablename__ = 'users'

    id = Column(BigInteger, primary_key=True)  # Integer   |
    statuses_count = Column(Integer)
    followers_count = Column(Integer)
    followees_count = Column(Integer)  # originally "friends_count"
    favorites_count = Column(Integer)  # originally "favourites_count"
    listed_count = Column(Integer)
    screen_name = Column(String(20))  # String
    name = Column(String(20))
    description = Column(String(256))
    lang = Column(String(8))
    time_zone = Column(String(32))
    location = Column(String(64))
    profile_image_url = Column(String(256))
    default_profile = Column(Boolean)  # Boolean
    default_profile_image = Column(Boolean)
    geo_enabled = Column(Boolean)
    verified = Column(Boolean)
    created_at = Column(DateTime)  # Date Time

    def __repr__(self):
        return "<id:{0}, screen_name:{1}, name:{2}, flwr:{3}, flwe:{4}, lang:{5} desc:{6}, member_since:{7}>".format(
            self.id, self.screen_name, self.name, self.followers_count, self.followees_count, self.lang,
            self.description.replace('\n', ' '), self.created_at)

    # >> UUEdge
    u_followed_me = UUEdge.build_rel("me", "follow")
    u_favorited_me = UUEdge.build_rel("me", "favorite")
    u_replied_me = UUEdge.build_rel("me", "reply")
    u_retweeted_me = UUEdge.build_rel("me", "retweet")
    u_mentioned_me = UUEdge.build_rel("me", "mention")
    u_quoted_me = UUEdge.build_rel("me", "quote")
    u_followed_by_me = UUEdge.build_rel("by_me", "follow")
    u_favorited_by_me = UUEdge.build_rel("by_me", "favorite")
    u_replied_by_me = UUEdge.build_rel("by_me", "reply")
    u_retweeted_by_me = UUEdge.build_rel("by_me", "retweet")
    u_mentioned_by_me = UUEdge.build_rel("by_me", "mention")
    u_quoted_by_me = UUEdge.build_rel("by_me", "quote")

    # >> USEdge
    s_tweeted_by_me = USEdge.build_rel("User", "tweet")
    s_retweeted_by_me = USEdge.build_rel("User", "retweet")
    s_replied_by_me = USEdge.build_rel("User", "reply")
    s_favorited_by_me = USEdge.build_rel("User", "favorite")
    s_quoted_by_me = USEdge.build_rel("User", "quote")
    s_mentioned_me = USEdge.build_rel("User", "mention")

    # >> EUEdge
    e_url_by_me = EUEdge.build_rel("User", "url")
    e_domain_by_me = EUEdge.build_rel("User", "domain")
    e_hashtag_by_me = EUEdge.build_rel("User", "hashtag")
    e_media_by_me = EUEdge.build_rel("User", "media")
    e_regex_by_me = EUEdge.build_rel("User", "regex")


class Status(Base):
    __tablename__ = 'statuses'

    id = Column(BigInteger, primary_key=True)  # Integer
    favorite_count = Column(Integer)  # originally "favourite_count"
    retweet_count = Column(Integer)
    text = Column(String(200))  # String
    lang = Column(String(5))
    coordinates = Column(String(128))
    source = Column(String(128))
    created_at = Column(DateTime)  # DateTime

    def __repr__(self):
        return "<id:{0}, lang:{1}, created_at:{2}, date:{3}>".format(self.id, self.lang, self.text.replace('\n', ' '),
                                                                     self.created_at)

    # >> USEdge
    u_tweeted_me = USEdge.build_rel("Status", "tweet")
    u_retweeted_me = USEdge.build_rel("Status", "retweet")
    u_replied_me = USEdge.build_rel("Status", "reply")
    u_favorited_me = USEdge.build_rel("Status", "favorite")
    u_mentioned_by_me = USEdge.build_rel("Status", "mention")

    # >> SSEdge
    s_replied_me = SSEdge.build_rel("me", 'reply')
    s_replied_by_me = SSEdge.build_rel("by_me", 'reply')
    s_quoted_me = SSEdge.build_rel("me", 'quote')
    s_quoted_by_me = SSEdge.build_rel("by_me", 'quote')

    # >> ESEdge
    e_url_by_me = ESEdge.build_rel("Status", "url")
    e_domain_by_me = ESEdge.build_rel("Status", "domain")
    e_hashtag_by_me = ESEdge.build_rel("Status", "hashtag")
    e_media_by_me = ESEdge.build_rel("Status", "media")
    e_regex = ESEdge.build_rel("Status", "regex")
