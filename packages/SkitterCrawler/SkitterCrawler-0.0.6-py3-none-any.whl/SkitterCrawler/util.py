from pathlib import Path
import sqlalchemy.orm
import sqlalchemy
import threading
import datetime
import pickle
import time
import json
import os


class Memory:

    def __init__(self, attrs=[], attrs_keep=[],  local=False):
        self.track = dict()
        for i in attrs:
            self.add_attribute(i)
        self.attrs_keep = attrs_keep
        self.dir = os.path.join(str(Path.home()), "SkitterCrawler")
        self.pickled = os.path.join(self.dir, "mem.p")

        if os.path.exists(self.pickled) and not local:
            f = open(self.pickled, "rb")
            other = pickle.load(f)
            f.close()
            self.track = other.track
            self.attrs_keep = other.attrs_keep

    def add_attribute(self, attribute):
        self.track[attribute] = dict()

    def add_val(self, attribute, val, ret):
        self.track[attribute][val] = ret

    def is_attribute(self, attribute):
        return attribute in self.track

    def is_val(self, attribute, val):
        return val in self.track[attribute]

    def get_attribute(self, attribute):
        return self.track[attribute]

    def get_val(self, attribute, val):
        return self.track[attribute][val]

    def is_in_memory(self, attribute, val):
        return self.is_attribute(attribute) and self.is_val(attribute, val)

    def dump(self):
        f = open(self.pickled, "wb")
        pickle.dump(self, f)
        f.close()


class DBHandler:
    """ This handles the operations with the database. It:
        1) Creates SQLAlchemy engine for some database.
        2) Start/closes new sessions for this database.
        3) Creates or drop ORM schemas for the database.
        4) Get values from the file with get_config/get_db_config.
    """

    def __init__(self, base):

        self.auth_handler = AuthHandler()
        self.engine = sqlalchemy.create_engine(self.auth_handler.get_db_config())
        self.sessionmaker = sqlalchemy.orm.sessionmaker(bind=self.engine)
        self.session = None
        self.base = base

    def start_new_session(self):

        self.sessionmaker.close_all()
        self.session = self.sessionmaker()

    def close_session(self):

        self.session.close()
        self.session = None

    def is_section_active(self):

        return self.session is not None

    def create_base(self):

        self.base.metadata.create_all(self.engine)

    def drop_base(self):

        self.base.metadata.drop_base(self.engine)

    def change_db_config(self, config):

        self.auth_handler.change_db_config(config)

    def get_db_config(self):

        return self.auth_handler.get_db_config()

    def commit_session(self):

        self.session.commit()


class AuthHandler:
    """ This handles the authentication with the api/databases, it:
        1) Creates a new file for secrets in __init__, if there isn't.
        2) Attach values to the file with attach_update_config/change_db_config.
        3) Remove values from the file with pop_config.
        4) Get values from the file with get_config/get_db_config.
    """

    def __init__(self):

        self.dir = os.path.join(str(Path.home()), "SkitterCrawler")
        self.json_file = os.path.join(self.dir, "secrets.json")
        self.db_address = os.path.join(self.dir, "db.txt")

        if not os.path.exists(self.dir):
            os.makedirs(self.dir)

        if not os.path.exists(self.json_file):
            f = open(self.json_file, 'w')
            f.write(json.dumps(dict()))
            f.close()

        if not os.path.exists(self.db_address):
            f = open(self.db_address, 'w')
            f.write('')
            f.close()

    def attach_crawler_config(self, key, value, crawler=None):

        f = open(self.json_file, 'r')
        tmp = json.loads(f.read())
        if crawler is None:
            tmp[key] = value
        else:
            if crawler not in tmp:
                tmp[crawler] = dict()
            tmp[crawler][key] = value
        f.close()
        f = open(self.json_file, 'w')
        f.write(json.dumps(tmp))
        f.close()

    def pop_crawler_config(self, key, crawler=None):

        f = open(self.json_file, 'r')
        tmp = json.loads(f.read())
        v = None
        if crawler is None:
            v = tmp.pop(key, None)
        else:
            if crawler not in tmp:
                v = tmp[crawler].pop(key, None)
        f.close()
        f = open(self.json_file, 'w')
        f.write(json.dumps(tmp))
        f.close()
        return v

    def get_crawler_config(self, key=None, crawler=None):

        f = open(self.json_file, 'r')
        tmp = json.loads(f.read())
        f.close()
        if key is None:
            return tmp
        elif crawler is None:
            return tmp[key]
        else:
            return tmp[crawler][key]

    def change_db_config(self, config):

        f = open(self.db_address, 'w')
        f.write(config)
        f.close()

    def get_db_config(self):

        f = open(self.db_address, 'r')
        tmp = f.read()
        f.close()
        return tmp


class FileChecker:
    """ This is the default class for the Checker, it:
        1) Creates a file with a flag 1 on `__init__'.
        2) On `start' sets the flag to 1.
        3) On `check' returns whether the flag is 1.
        4) On `stop' sets the flag to 0.
    """

    def __init__(self):
        self.dir = os.path.join(str(Path.home()), "SkitterCrawler")
        self.txt = os.path.join(self.dir, "._control.txt")
        if not os.path.exists(self.dir):
            os.makedirs(self.dir)
        self.start()

    def start(self):
        f = open(self.txt, 'w')
        f.write("1")
        f.close()

    def check(self):
        f = open(self.txt, 'r')
        tmp = f.read() == "1"
        f.close()
        return tmp

    def stop(self):
        f = open(self.txt, 'w')
        f.write("0")
        f.close()


class TimeWaiter:
    """ This is the default class for the Stopper, it:
        1) Sets a number of seconds in `__init__' or on `start'.
        2) Starts the timer on `start'.
        3) Checks if the timer is over on on `check'
    """

    def __init__(self, default=None):

        self.hammer_time = 0
        self.default = 60 if default is None else default

    def start(self, seconds=None):

        t = self.default if seconds is None else seconds
        self.hammer_time = (datetime.datetime.now() + datetime.timedelta(seconds=int(t))).timestamp()

    def check(self):

        return datetime.datetime.now().timestamp() < self.hammer_time


class Log:
    """ This is the default class for the Logger, it:
        1) Starts a dict() on `__init__'.
        2) `log' creates if key not in dict, creates dict[string] = [], else dict[string].append(list_stuff).
        3) `ret' returns the lists sorted by time
    """

    def __init__(self):
        self.dir = os.path.join(str(Path.home()), "SkitterCrawler")
        self.txt_file = os.path.join(self.dir, "log.txt")
        self.info = dict()
        self.id = "(noid)"

    def set_id(self, id_v):
        self.id = id_v

    def log(self, string, list_stuff):

        if string not in self.info:
            self.info[string] = []
        for stuff in list_stuff:
            self.info[string].append("{0} {1}: {2}".format(self.id,
                                                        time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime()),
                                                        stuff))

    def __add__(self, other):
        for key in self.info:
            if key not in other.info:
                other.info[key] = []
        for key in other.info:
            if key not in self.info:
                self.info[key] = []
        for key in self.info:
            self.info[key] = self.info[key] + other.info[key]
        self.id = "(noid)"

        return self

    def ret(self):

        string = ""

        for key in sorted(self.info.keys()):
            string += key + "\n"
            for stuff in self.info[key]:
                string += "\t" + stuff + "\n"

        return string

    def dump(self, s=None):
        f = open(self.txt_file, 'a+')
        if s is not None:
            f.write(s)
        f.write(self.ret())
        f.close()

    def flush(self):
        self.info = dict()
        self.id = "(noid)"


def run(slaves, identifiers, reduce, check=FileChecker, init_state=lambda: None):
    """ This function coordinates data collection, distributing tasks to several slaves and then merging the results.
    1) Each slave is a runnable function that does something we want. It must contain two arguments to pass on results.
    2) Each slave is assigned a unique identifier.
    3) After all slaves finish their execution, the reduce function process the work of all slaves.
    4) The cycle then continues forever.

    :param slaves: list of runnable functions that take a string, a list and an index as arguments.
    :param identifiers: list of identifiers.
    :param reduce: function that receives list of identifiers and list of results.
    :param check: function that yields true if the cycle is to continue.
    :param init_state: function to initialize shared state.
    :return: number of iterations.
    """

    it = 0
    state = init_state()

    checker = check()
    checker.start()

    while checker.check():

        l = len(slaves)
        results = [None] * l
        threads = [None] * l

        for i, s, idx in zip(identifiers, slaves, range(l)):
            threads[idx] = threading.Thread(name=i, target=s, args=(i, results, idx, state))

        for idx in range(l):
            threads[idx].setDaemon(True)

        for idx in range(l):
            threads[idx].start()

        for idx in range(l):
            threads[idx].join()

        state = reduce(it=it, results=results, state=state)
        it += 1

    return it
