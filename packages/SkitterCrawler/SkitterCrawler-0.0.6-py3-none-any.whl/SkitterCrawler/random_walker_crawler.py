from SkitterCrawler.util import AuthHandler, FileChecker, TimeWaiter, Log, run
from SkitterCrawler.twitter_crawlers import RandomWalkerTwitterCrawler
from pathlib import Path
from functools import partial
import json
import os


def _random_walk_crawler(config_m=None):
    if config_m is None:
        skittercrawler = os.path.join(str(Path.home()), "SkitterCrawler")
        f = open(os.path.join(skittercrawler, "rwc_config.json"), 'r')
        config = json.load(f)
        f.close()
    elif type(config_m) is not dict:
        f = open(config_m, 'r')
        config = json.load(f)
        f.close()
    else:
        config = config_m

    crawlers, crawlers_names = [], list(config.keys())
    for crawler_name in crawlers_names:
        auth_handler = AuthHandler()
        auth_dict = auth_handler.get_crawler_config(crawler_name)
        crawler = RandomWalkerTwitterCrawler(auth_dict=auth_dict,
                                             stopper=partial(TimeWaiter, config[crawler_name]['time_wait']),
                                             logger=Log,
                                             seed=config[crawler_name]['seed'])
        crawlers.append(crawler.run)

    state = RandomWalkerTwitterCrawler.init_external_state
    reducer = RandomWalkerTwitterCrawler.reducer

    run(slaves=crawlers, identifiers=crawlers_names, reduce=reducer, check=FileChecker,  init_state=state)


if __name__ == "__main__":
    _random_walk_crawler()
