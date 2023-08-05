import sqlalchemy
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Integer, Boolean, String, Column, DateTime, Enum, Text
from sqlalchemy.orm import sessionmaker

Base = declarative_base()


class bot_comments(Base):
    __tablename__ = 'bot_comments'
    id = Column(Integer, primary_key=True)
    thing_id = Column(String(15), nullable=False)
    source_thing_id = Column(String(15), nullable=False)
    source_microservice_id = Column(String(15), nullable=False)
    content = Column(String(10000), nullable=False)
    submitted = Column(Boolean, nullable=False)
    submitted_id = Column(String(15))

    def __eq__(self, other):
        return self.thing_id == other.thing_id and self.source_thing_id == other.source_thing_id and \
               self.content == other.content and self.submitted == other.submitted and \
               self.submitted_id == other.submitted_id and self.source_microservice_id == other.source_microservice_id

    def __ne__(self, other):
        return not self.thing_id == other.thing_id and self.source_thing_id == other.source_thing_id and \
               self.content == other.content and self.submitted == other.submitted and \
               self.submitted_id == other.submitted_id and self.source_microservice_id == other.source_microservice_id

    @property
    def pure_thing_id(self):
        return self.thing_id[3:]

    @property
    def is_response_to_comment(self):
        return self.thing_id[:2] == 't1'

    @property
    def is_response_to_submission(self):
        return self.thing_id[:2] == 't3'

    @property
    def is_chained_response(self):
        return self.thing_id[:1] == 'i'

    @property
    def pure_chained_id(self):
        return self.thing_id[1:]

    def set_failed_submitted(self):
        self.submitted = True
        self.submitted_id = 'del-1'

    def set_successful_submitted(self, submitted_id=None):
        self.submitted = True
        if submitted_id is not None:
            self.submitted_id = submitted_id

    @property
    def is_failed_chain(self):
        return self.submitted_id == 'del-1'


class bot_submissions(Base):
    __tablename__ = 'bot_submissions'
    id = Column(Integer, primary_key=True)
    title = Column(String(300), nullable=False)
    content = Column(String(15000))
    type = Column(String(10), nullable=False)
    subreddit = Column(String(50), nullable=False)
    submitted = Column(Boolean, nullable=False)
    source_microservice_id = Column(String(15), nullable=False)

    @property
    def is_link(self):
        return self.type == 'link'

    @property
    def is_selfpost(self):
        return self.type == 'self'

    @property
    def stripped_thing_id(self):
        return self.thing_id[3:]

    def set_failed_submitted(self):
        self.submitted = False
        self.submitted_id = 'del-1'

    def set_successful_submitted(self):
        self.submitted = True


class subreddit(Base):
    __tablename__ = 'subreddit'
    website = Column(String(10), primary_key=True)
    last_submission = Column(Integer)
    last_comment = Column(Integer)


class bot_errors(Base):
    __tablename__ = 'bot_errors'
    id = Column(Integer, primary_key=True)
    url = Column(Text())
    exception = Column(Text())
    timestamp = Column(DateTime())
    source_microservice_id = Column(String(15), nullable=False)

    def __eq__(self, other):
        return self.url == other.url and self.exception == other.exception and \
               self.source_microservice_id == other.source_microservice_id

    def __ne__(self, other):
        return not self.url == other.url and self.exception == other.exception and \
               self.source_microservice_id == other.source_microservice_id


class anet_member(Base):
    __tablename__ = 'anet_member'
    username = Column(String(50), primary_key=True)


class bot_comments_anetpool(Base):
    __tablename__ = 'bot_comments_anetpool'
    thread_id = Column(String(15))
    content = Column(String(10000), nullable=False)
    submitted = Column(Boolean, nullable=False)
    submitted_id = Column(String(15))
    edit_id = Column(Integer, primary_key=True, unique=True, nullable=False)
    source_microservice_id = Column(String(15), nullable=False)


def create_session(system, username, password, host, database):
    engine = sqlalchemy.create_engine(f"{system}://{username}:{password}@{host}/{database}")
    Base.metadata.create_all(engine)
    Base.metadata.bind = engine

    Session = sessionmaker(bind=engine, expire_on_commit=False)
    return Session()
