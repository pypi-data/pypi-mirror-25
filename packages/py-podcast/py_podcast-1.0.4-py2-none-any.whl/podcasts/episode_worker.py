import os
import pdb
import threading
from copy import deepcopy
import feedparser
import podcasts.log as log
from podcasts.models.episode import Episode

class EpisodeWorker(threading.Thread):
  def __init__(self, storer, series):
    """
    Constructor for thread that will request the RSS of a
    particular podcast series, parse the series details
    and episode information, and save the information
    w/`storer`
    """
    super(EpisodeWorker, self).__init__()
    self.logger = log.logger
    self.storer = storer
    self.series = series # All series

  def request_rss(self, url):
    return feedparser.parse(url)

  def run(self):
    """
    Run the task - compose full series + add to our results
    """
    empty = False
    while not empty:
      try:
        s = self.series.get()
        rss = self.request_rss(s.feed_url)
        ep_dicts = []
        for entry in rss['entries']:
          ep_dicts.append(Episode(s, entry).__dict__)
        result_dict = dict()
        result_dict['series'] = deepcopy(s.__dict__)
        result_dict['series']['genres'] = \
          result_dict['series']['genres'].split(';')
        result_dict['series']['type'] = 'series'
        result_dict['episodes'] = ep_dicts
        self.storer.store(result_dict)
        self.logger.info('Retrieved and stored %s', str(s.id))
      except Exception as e: # pylint: disable=W0703
        print e
      finally:
        self.series.task_done()
        empty = self.series.empty()
