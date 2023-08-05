""" This module contains the service definition of the football-data.org api """

import re

SERVICE_DEFINITION = {
    'url': 'http://api.football-data.org/v1',
    'resources': {
        'competitions': {
            'name': 'competitions',
            'standalone': True,
            'subresources': {
                'teams': {
                    'name': 'teams',
                    'filters': {}
                },
                'leagueTable': {
                    'name': 'leagueTable',
                    'filters': { 
                        'matchday': {
                            're': re.compile('^[1-9][\d]*$')
                        }
                    }
                },
                'fixtures': {
                    'name': 'fixtures',
                    'filters': {
                        'timeFrame': {
                            're': re.compile('^(p|n)[1-9][\d]?$')
                        },
                        'matchday': {
                            're': re.compile('^[1-9][\d]*$')
                        }
                    }
                }
            },
            'filters': {
                'season': {
                    're': re.compile('^\d{4}$'),
                    'withId': False
                }
            }
        },
        'fixtures': {
            'name': 'fixtures',
            'standalone': True,
            'subresources': {},
            'filters': {
                'head2head': {
                    'withId': True,
                    're': re.compile('^\d+$')
                },
                'timeFrame': {
                    'withId': False,
                    're': re.compile('^(p|n)[1-9][\d]?$')
                },
                'league': {
                    'withId': False,
                    're': re.compile('^[\w\d]{2,4}(,[\w\d]{2,4})*$')
                }
            }
        },
        'teams': {
            'name': 'teams',
            'standalone': False,
            'subresources': {
                'fixtures': {
                    'name': 'fixtures',
                    'filters': {
                        'season': {
                            're': re.compile('^\d{4}$')
                        },
                        'timeFrame': {
                            're': re.compile('^(p|n)[1-9][\d]?$')
                        },
                        'venue': {
                            're': re.compile('^(home|away)$')
                        }
                    }
                },
                'players': {
                    'name': 'players',
                    'filters': {}
                }
            },
            'filters': {
                'name': {
                    're': re.compile('^...+$')
                }
            }
        }
    }
}