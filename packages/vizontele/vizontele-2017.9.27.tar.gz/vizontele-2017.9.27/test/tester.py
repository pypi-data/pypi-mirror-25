from pprint import pprint

from vizontele.crawler import DiziCrawler

#episode = DiziCrawler('dizimag', 'supernatural', 12, 22).get_sources()
#assert len(episode['video_links']) > 0
#pprint('Dizimag test successful')

episode = DiziCrawler('dizipub', 'the office', 1, 2).get_sources()
assert len(episode['video_links']) > 0
pprint('Dizipub test successful')

episode = DiziCrawler('dizilab', 'rick-and-morty', 3, 6).get_sources()
assert len(episode['video_links']) > 0
pprint('Dizilab test successful')

episode = DiziCrawler('sezonlukdizi', 'the-big-bang-theory', 11, 1).get_sources()
assert len(episode['video_links']) > 0
pprint('Sezonlukdizi test successful')

episode = DiziCrawler('dizibox', 'doctor-who', 10, 8).get_sources()
assert len(episode['video_links']) > 0
pprint('Dizibox test successful')

episode = DiziCrawler('dizimek', 'how i met your mother', 1, 1).get_sources()
assert len(episode['video_links']) > 0
pprint('Dizimek test successful')

episode = DiziCrawler('dizist', 'family-guy', 1, 1).get_sources()
assert len(episode['video_links']) > 0
pprint('Dizist test successful')

episode = DiziCrawler('diziay', 'family guy', 1, 1).get_sources()
assert len(episode['video_links']) > 0
pprint('Diziay test successful')