from SkitterSchema.tweepy2schema import ProcessedOutcome, process_timeline, process_user, process_followers
from SkitterSchema.tweepy2schema import process_followees, process_favourites
from SkitterCrawler.util import Memory, Log, DBHandler
from SkitterSchema.twitter_schema import UUEdge
from SkitterSchema.twitter_schema import Base
import random
import tweepy


class TwitterCrawler:
    def __init__(self, auth_dict, stopper, logger):
        """ Initialization method for the generic crawler.
        :param auth_dict: dictionary with consumer_key, consumer_secret, access_token and access_secret for twitter api.
        :param logger: logger class with log.log(key, values)
        :param stopper: stopper class with stopper.start() and stopper.check()
        """

        # gets secrets
        self.consumer_key, self.consumer_secret = auth_dict['consumer_key'], auth_dict['consumer_secret']
        self.access_token, self.access_secret = auth_dict['access_token'], auth_dict['access_secret']

        # initializes logger and stopper
        self.log, self.stop = logger(), stopper()

        # gets api object from Tweepy
        auth = tweepy.OAuthHandler(self.consumer_key, self.consumer_secret)
        auth.set_access_token(self.access_token, self.access_secret)
        self.api = tweepy.API(auth)

        self.log.log("Initializing API", ["API initialization was successful"])

    def _run(self, identifier, result, idx, state, **kwargs):
        raise Exception("_run function not implemented!")

    def run(self, identifier, result, idx, state, **kwargs):
        """ This function is a generic slave.
        :param identifier: identifier for the slave.
        :param result: array with results.
        :param idx: position of the array that can be modified.
        :param state: state of the current iteration.
        :param kwargs: arguments for filtering/searching.
        :return: Nothing
        """
        self._run(identifier, result, idx, state, **kwargs)

    @staticmethod
    def reducer(it, results, state):
        raise Exception("reducer function not implemented!")


class RandomWalkerTwitterCrawler(TwitterCrawler):
    def __init__(self, auth_dict, stopper, logger, seed, prob_types=(0.7, 0.3), prob_seed=0.3):
        """ This initializes a RandomWalkerTwitterCrawler.
        :param auth_dict: dictionary with consumer_key, consumer_secret, access_token and access_secret for twitter api.
        :param logger: logger class with log.log(key, values).
        :param stopper: stopper class with stopper.start() and stopper.check().
        :param seed: seed or list of seeds from which the rw will start and eventually return.
        :param prob_types: P of next u_retweeted_by_me, u_replied_by_me.
        :param prob_seed: probability at each hop that rw will return to the seed.
        """
        self.seed, self.pointer = seed, None  # Initializes seed(s), pointer
        self.prob, self.prob_seed = [sum(prob_types[:i + 1]) for  # Initializes probabilities
                                     i, x in enumerate(prob_types)], prob_seed
        self.excd, self.count, self.got, self.mem = dict(), dict(), dict(), None  # Bookkeeping
        super().__init__(auth_dict, stopper, logger)

    def point_to_seed(self):
        """ This makes the pointer points to the seed. If the seed is unique, it will always point to the same seed,
        however if the seed is a list of tweet IDs, we return a seed randomly.
        :return: Nothing
        """
        self.pointer = random.choice(self.seed) if isinstance(self.seed, list) else self.seed

    def chooses_next(self, retweets, replies):
        """ Chooses next from retweets, replies or the existing seed.
        :param retweets: list of user ids of whom the user retweeted.
        :param replies: list of user ids of whom the user replied.
        :return: Nothing.
        """
        joint = [retweets, replies]

        rv = random.random()
        if rv <= self.prob_seed:
            self.point_to_seed()
            return

        rv = random.random()
        tmp = [rv <= i for i in self.prob].index(True)
        order = list(range(tmp, len(joint))) + list(range(0, tmp))

        for i in order:
            if len(joint[i]) == 0:
                continue
            self.pointer = random.choice(joint[i])
            return

        self.point_to_seed()

    def get_user(self):
        """ This makes an api call to get the user and then processes it. """
        return process_user(self.api.get_user(self.pointer))

    def get_timeline(self):
        """ This makes an api call to get the timeline and then processes it. """
        retweets, replies, timeline_outcome = [], [], ProcessedOutcome()
        tl = self.api.user_timeline(include_rts=True, count=200, trim_user=False, exclude_replies=False,
                                    user_id=self.pointer)
        timeline_outcome += process_timeline(tl)
        retweets = set(timeline_outcome.get_filtered_edges(UUEdge, "retweet", lambda x: x.dst_id))
        retweets = list(filter(lambda x: x != self.pointer, retweets))
        replies = set(timeline_outcome.get_filtered_edges(UUEdge, "reply", lambda x: x.dst_id))
        replies = list(list(filter(lambda x: x != self.pointer, replies)))
        return retweets, replies, timeline_outcome

    def get_followers_ees(self):
        """ This makes an api call to get the followers/ees and then processes it. """
        followees = self.api.friends_ids(user_id=self.pointer, count=5000)
        followers = self.api.followers_ids(user_id=self.pointer, count=5000)
        followers_ees_outcome = process_followers(followers, self.pointer)
        followers_ees_outcome += process_followees(followees, self.pointer)
        return followers_ees_outcome

    def get_favs(self):
        """ This makes an api call to get the favorites and then processes it. """
        favs = self.api.favorites(user_id=self.pointer, count=200, include_entities=True)
        favs_outcome = process_favourites(favs, self.pointer)
        return favs_outcome

    def double_mem_check(self, state, attribute, val, func):
        """This executes the given func only if the val is not in self.memory[attribute]"""
        outcome = ProcessedOutcome()
        # Gets user if not in memory, may raise tweepy.RateLimitError
        if not self.mem.is_in_memory(attribute, val) and not state.is_in_memory(attribute, val):
            outcome = func()
            self.count[attribute] += 1

            if self.mem.is_attribute(attribute):
                self.mem.add_val(attribute, val, True)
        self.got[attribute] = True
        return outcome

    def handle_got(self, e, attribute):
        if not self.got[attribute]:
            self.log.log("Error Retrieving {0}".format(attribute), [e.reason])
            if type(e) is tweepy.RateLimitError:
                self.excd[attribute] = True
                return True
        return False

    def _run(self, identifier, result, idx, state, **kwargs):
        """ Internal function for doing the streaming processing. """

        self.stop.start()
        self.point_to_seed()
        self.log.flush()
        self.log.set_id(identifier)
        outcome = ProcessedOutcome()
        retweets, replies = [], []
        self.mem = Memory(['user', 'tl', 'flwer', 'favs'], ['flwer', 'favs'], local=True)
        self.count = dict({"user": 0, "tl": 0, "flwer": 0, "favs": 0})
        self.excd = dict({"user": False, "tl": False, "flwer": False, "favs": False})

        while self.stop.check() and self.excd['tl'] is False:

            self.got = dict({"user": False, "tl": False, "flwer": False, "favs": False})

            try:
                # Gets timeline if not in memory, may raise tweepy.RateLimitError
                if self.mem.is_in_memory('tl', self.pointer):
                    retweets, replies = self.mem.get_val('tl', self.pointer)
                elif state.is_in_memory('tl', self.pointer):
                    retweets, replies = state.get_val('tl', self.pointer)
                else:
                    retweets, replies, timeline_outcome = self.get_timeline()
                    outcome += timeline_outcome
                    self.count['tl'] += 1
                    if self.mem.is_attribute('tl'):
                        self.mem.add_val('tl', self.pointer, [retweets, replies])
                self.got['tl'] = True

                # Gets user if not in memory, may raise tweepy.RateLimitError
                if not self.excd["user"]:
                    outcome += self.double_mem_check(state, 'user', self.pointer, self.get_user)

                # Gets followers if not in memory, may raise tweepy.RateLimitError
                if not self.excd["flwer"]:
                    outcome += self.double_mem_check(state, 'flwer', self.pointer, self.get_followers_ees)

                # Gets followers if not in memory, may raise tweepy.RateLimitError
                if not self.excd["favs"]:
                    outcome += self.double_mem_check(state, 'favs', self.pointer, self.get_favs)

            except tweepy.TweepError as e:

                if self.handle_got(e, 'tl'):
                    continue

                if self.handle_got(e, 'user'):
                    continue

                if self.handle_got(e, 'flwer'):
                    continue

                if self.handle_got(e, 'favs'):
                    continue

            previous_pointer = self.pointer
            self.chooses_next(retweets, replies)
            print("({0}) {1} > {2} : user={3}/{7}/{11} tl={4}/{8}/{12} flwer={5}/{9}/{13} favs={6}/{10}/{14}".format(
                identifier, previous_pointer, self.pointer,
                self.count["user"], self.count["tl"], self.count["flwer"], self.count["favs"],
                len(self.mem.track["user"]), len(self.mem.track["tl"]),
                len(self.mem.track["flwer"]), len(self.mem.track["favs"]),
                len(state.track["user"]), len(state.track["tl"]),
                len(state.track["flwer"]), len(state.track["favs"])))

            retweets, replies = [], []

        self.log.log("Retrieved", ["users: {0}, statuses: {1}, entities: {2}, edges: {3}"
                     .format(len(outcome.schema_users), len(outcome.schema_tweets),
                             len(outcome.schema_entities), len(outcome.schema_edges))])

        self.log.log("Requests", ["user: {0}, tl: {1}, flwer: {2}, favs: {3}"
                     .format(self.count["user"], self.count["tl"], self.count["flwer"], self.count["flwer"])])

        self.log.log("Memory", ["Local user: {0}, tl: {1}, flwer: {2}, favs: {3}"
                     .format(len(self.mem.track["user"]), len(self.mem.track["tl"]),
                             len(self.mem.track["flwer"]), len(self.mem.track["favs"]))])

        self.log.log("Memory", ["Global user: {0}, tl: {1}, flwer: {2}, favs: {3}"
                     .format(len(state.track["user"]), len(state.track["tl"]),
                             len(state.track["flwer"]), len(state.track["favs"]))])

        result[idx] = (identifier, outcome, self.mem, self.log)

    @staticmethod
    def reducer(it, results, state):

        nlog = Log()
        dbhandler = DBHandler(base=Base)
        dbhandler.create_base()
        dbhandler.start_new_session()
        final_outcome = ProcessedOutcome()

        state.dump()

        for identifier, outcome, state_update, log in results:
            final_outcome += outcome
            for attr in state_update.attrs_keep:
                for val in state_update.get_attribute(attr).keys():
                    state.add_val(attr, val, True)
            nlog += log

        final_outcome.add_to_session(dbhandler.session)
        dbhandler.commit_session()
        dbhandler.close_session()
        nlog.dump(s="Iteration {0}:\n".format(it))

        return state

    @staticmethod
    def init_external_state():
        return Memory(['user', 'tl', 'flwer', 'favs'], ['flwer', 'favs'])
