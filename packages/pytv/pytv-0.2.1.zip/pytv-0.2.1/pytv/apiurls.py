"""File that contains all the urls for the tvmaze api located at http://www.tvmaze.com/api"""

BASE_URL = 'http://api.tvmaze.com/'

SCHEDULE = '{}schedule'.format(BASE_URL)
FULL_SCHEDULE = '{}/full'.format(SCHEDULE)

SHOW = '{}shows/'.format(BASE_URL)
EPISODE = '{}/episodes/'.format(BASE_URL)

SEASON = '{}seasons/'.format(BASE_URL)
