""" Entry point for football-data.org api wrapper """
import logging
from footballdataorg.request_handler import RequestHandler
from footballdataorg.exceptions import APIErrorException, IncorrectParametersException, IncorrectFilterException, IncorrectMethodCallException

class FD(object):
    """ Please register on football-data.org (http://api.football-data.org/client/register)
    to get an API key. """
    def __init__(self, apikey=None):
        self.logger = logging.getLogger(__name__)
        headers = {}
        if apikey is not None:
            self.logger.info(f'Initializing with API key {apikey}')
            headers['X-Auth-Token'] = apikey
        self.logger.info('Creating RequestHandler')
        self.rh = RequestHandler(headers)
        self.competitions = {}

    def _request(self, main, main_id=None, sub=None, filters=None):
        try:
            return self.rh.get_json(main, main_id, sub, filters)
        except (APIErrorException, IncorrectParametersException, IncorrectFilterException) as e:
            self.__handleException(e)

    def get_competitions(self,season=None):
        try:
            if season is not None:
                self.logger.debug(f'Get competitions of season {season}')
                seasonFilter = {
                    'name': 'season',
                    'value': season
                }
                filters = [seasonFilter]
            else:
                self.logger.debug(f'Get competitions of current season')
                filters = []
                season = 'default'

            if season not in self.competitions or self.competitions[season] is None:
                self.competitions[season] = self._request('competitions', filters=filters)
                
            return self.competitions[season]
        except Exception as ex:
            self.__handleException(ex)

    def get_competition(self, league_id=None, league_code=None, season=None):
        self.logger.debug(f'Get a competition with the following parameters: {locals()}')
        if league_id is not None:
            return self._request('competitions', league_id)
        elif league_code is not None:
            competitions = self.get_competitions(season)
            for competition in competitions:
                if competition['league'] == league_code:
                    return competition

    def get_team(self, team_id):
        self.logger.debug(f'Get a single team with id {team_id}')
        return self._request('teams', team_id)

    def get_teams(self, competition):
        self.logger.debug(f'Geting list of teams')
        competition_id = self.__get_competition_id(competition)
        self.logger.debug(f'Competition id is {competition_id}')
        return self._request('competitions', competition_id, 'teams')

    def search_teams(self, query):
        self.logger.debug(f'Searching for teams with query "{query}"')
        return self._request('teams', filters=[self.__createFilter('name', query)])

    def get_league_table(self, competition, matchday=None):
        if matchday is not None:
            self.logger.debug(f'Getting league table of competition {competition["caption"]} on matchday {str(matchday)}')
            matchday_filter = {
                'name': 'matchday',
                'value': str(matchday)
            }
            filters = [matchday_filter]
        else:
            self.logger.debug(f'Getting the current league table of competition {competition["caption"]}')
            filters = []

        competition_id = self.__get_competition_id(competition)
        return self._request('competitions', competition['id'], 'leagueTable', filters=filters)

    def get_fixtures(self, competition=None, team=None, timeFrame=None, matchday=None, season=None, venue=None, league=None):    
        """ This method gets a set of fixtures. There are several possibilities to load them. The following three main resources are available: 
            * competitions
            * teams
            * fixtures

            Args:
               * competition (:obj: json, optional): a competition in json format obtained from the service.
               * team (:obj: json, optional): a team in json format obtained from the service.
               * timeFrame (str, optional): a timeFrame string.
               * matchday (int, optional): the matchday in integer format.
               * season (str, optional): the year of the season.
               * venue (str, optional): 'home' or 'away'.

            Returns:
               * :obj: list of :obj: json: a list of fixtures

            #### Competitions
            To load the fixtures of a competition you have to provide a competition-json that you obtained from the service.
            You can provide the following filters:
            * timeFrame (str): a timeFrame string (e.g. n14 for fixtures in the next 14 days)
            * matchday (int): the matchday

            Note that the filters can not be combined. 
            
            #### Teams
            To load the fixtures of a team you have to provide a team-json that you obtained from the service.
            You can provide the following filters:
            * timeFrame (str): a timeFrame string (e.g. n14 for fixtures in the next 14 days)
            * season (str): the year of the season (e.g. 2017)
            * venue: (str): either 'home' or 'away'

            Note that timeFrame and season can not be combined. 

            #### Fixtures
            To load a list of upcoming or passed fixtures you do not need to provide a json. You can provide the following filters:
            * league: a leagueCode. Please refer to the documentation to get a list of league codes.
            * timeFrame: a timeFrame string (e.g. n14 for fixtures in the next 14 days)
        """
        self.logger.debug(f'Getting fixtures with the following parameters: {locals()}')
        filters = []
        if competition is not None:
            if timeFrame is not None and matchday is not None:
                raise IncorrectMethodCallException("Please filter by either timeFrame or matchday.")
            elif timeFrame is not None and matchday is None:
                filters.append(self.__createFilter('timeFrame', timeFrame))
            elif timeFrame is None and matchday is not None:
                filters.append(self.__createFilter('matchday', matchday))

            competition_id = self.__get_competition_id(competition)
            fixtures = self._request('competitions', competition_id, 'fixtures', filters=filters)
            if team is not None:
                fixtures['fixtures'] = list(filter(lambda fixture: fixture['_links']['homeTeam']['href'] == team['_links']['self']['href'] or fixture['_links']['awayTeam']['href'] == team['_links']['self']['href'], fixtures['fixtures']))
                fixtures['count'] = len(fixtures['fixtures']) 
        elif team is not None:
            if venue is not None:
                filters.append(self.__createFilter('venue', venue))
            if season is not None and timeFrame is not None:
                raise IncorrectMethodCallException("Please filter by either timeFrame or season.")
            elif season is not None:
                filters.append(self.__createFilter('season', season))
            elif timeFrame is not None:
                filters.append(self.__createFilter('timeFrame', timeFrame))

            team_id = self.__get_team_id(team)
            fixtures = self._request('teams', team_id, 'fixtures', filters=filters)
        else:
            if league is not None:
                filters.append(self.__createFilter('league', league))
            if timeFrame is not None:
                filters.append(self.__createFilter('timeFrame', timeFrame))
            
            fixtures = self._request('fixtures', filters=filters)
        return fixtures

    def get_fixture(self, fixture_id, head2head=None):
        """
        Loads a single fixture.

        Args:
            * fixture_id (str): the id of the fixture
            * head2head (int, optional): load the previous n fixture of the two teams

        Returns:
            * :obj: json: the fixture-json
        """
        filters = []
        if head2head is not None and int(head2head) > 0:
            self.logger.debug(f'Getting fixture {fixture_id}. head2head is {head2head}.')
            filters.append(self.__createFilter('head2head', head2head))
        else:
            self.logger.debug(f'Getting fixture {fixture_id}.')

        return self._request('fixtures', fixture_id, filters=filters)

    def get_players(self, team):
        """
        Loads the players of a team.

        Args:
            * team (:obj: json): a team in json format obtained from the service.

        Returns:
            * :obj: json: the players of the team
        """
        team_id = self.__get_team_id(team)
        self.logger.debug(f'Getting players of team {team_id}.')
        return self._request('teams', team_id, 'players')

    def __createFilter(self, name, value):
        """
        Creates a filter. A filter is a simple dictionary with the keys 'name' and 'value'.

        Args:
            * name (str): the name of the filter
            * value (str): the value of the filter

        Returns:
            * :obj: dict: the filter dictionary
        """
        return {'name': name, 'value': str(value)}

    def __get_competition_id(self, competition):
        try:
            return competition['_links']['self']['href'].split('/')[5]
        except TypeError as ex:
            self.__handleException(ex)

    def __get_team_id(self, team):
        try:
            return team['_links']['self']['href'].split('/')[5]
        except TypeError as ex:
            self.__handleException(ex)

    def __handleException(self, ex):
        template = "An exception of type {0} occurred. Arguments:\n{1!r}"
        message = template.format(type(ex).__name__, ex.args)
        self.logger.error(message)
