""" Python interface to PandaScore core API """

try:
    from urlparse import urlparse, parse_qs
except ImportError:
    from urllib.parse import urlparse, parse_qs

from .api import Api
from .util import format_params


class PandaScore(Api):
    """ Python interface to PandaScore core API """

    def __init__(self, *args, **kwargs):
        super(PandaScore, self).__init__(*args, **kwargs)

    def get_videogames(self, **params):
        """
            This function returns a list of videogame dicts. All parameters
            are optional. Sort, filter, and range can only use: id, created_at,
            updated_at, name, slug, instance, prefix.

            :param sort: The sort order. Sorted by id desc by default
            :param filter: Allows for filtering on one or more fields
                ex: filter='name=VCSA,Challenge France;created_at=2017-01-01'
            :param range: A hash allowing filtering for a field, as a key,
                on two comma-separated bounds. Only the fields between
                the given bounds will be returned. The bounds are inclusives.
                ex: range='created_at=2017-01-01,2017-02-01'
        """
        valid_params = ['sort', 'filter', 'range']
        params = format_params(valid_params, **params)
        videogames = self.get_data("videogames/", params=params)

        return videogames

    def get_leagues(self, **params):
        """
            This function returns a list of league dicts. All parameters
            are optional. Sort, filter, and range can only use: id, image,
            url, name, videogame_id, created_at, updated_at, slug.

            :param videogame_id: The unique identifier for a video game
            :param sort: The sort order. Sorted by id desc by default
            :param filter: Allows for filtering on one or more fields
                ex: filter='name=VCSA,Challenge France;created_at=2017-01-01'
            :param range: A hash allowing filtering for a field, as a key,
                on two comma-separated bounds. Only the fields between
                the given bounds will be returned. The bounds are inclusives.
                ex: range='created_at=2017-01-01,2017-02-01'
        """
        valid_params = ['videogame_id', 'sort', 'filter', 'range']
        params = format_params(valid_params, **params)
        leagues = self.get_data("leagues/", params=params)

        return leagues

    def get_league(self, league_id):
        """
            This function returns a single league dict by league_id

            :param league_id: The unique identifier for a league
        """
        league = self.get_data("leagues/" + str(league_id))

        return league

    def get_series(self, **params):
        """
            This function returns a list of series dicts. All parameters
            are optional. Sort, filter, and range can only use: id, name,
            season, url, league_id, created_at, updated_at, prizepool,
            description, begin_at, winner_id, winner_type, slug, year, end_at.

            :param videogame_id: The unique identifier for a video game
            :param league_id: The unique identifier for a league
            :param sort: The sort order. Sorted by id desc by default
            :param filter: Allows for filtering on one or more fields
                ex: filter='name=VCSA,Challenge France;created_at=2017-01-01'
            :param range: A hash allowing filtering for a field, as a key,
                on two comma-separated bounds. Only the fields between
                the given bounds will be returned. The bounds are inclusives.
                ex: range='created_at=2017-01-01,2017-02-01'
        """
        valid_params = ['videogame_id', 'league_id', 'sort', 'filter', 'range']
        params = format_params(valid_params, **params)
        series = self.get_data("series/", params=params)

        return series

    def get_serie(self, series_id):
        """
            This function returns a single series dict by series_id

            :param series_id: The unique identifier for a series
        """
        series = self.get_data("series/" + str(series_id))

        return series

    def get_tournaments(self, **params):
        """
            This function returns a list of tournament dicts. All parameters
            are optional. Sort, filter, and range can only use: id, name,
            begin_at, end_at, winner_id, serie_id, created_at, updated_at,
            updated, winner_type, slug, parent_id, videogame_id.

            :param videogame_id: The unique identifier for a video game
            :param league_id: The unique identifier for a league
            :param serie_id: The unique identifier for a series
            :param sort: The sort order. Sorted by id desc by default
            :param filter: Allows for filtering on one or more fields
                ex: filter='name=VCSA,Challenge France;created_at=2017-01-01'
            :param range: A hash allowing filtering for a field, as a key,
                on two comma-separated bounds. Only the fields between
                the given bounds will be returned. The bounds are inclusives.
                ex: range='created_at=2017-01-01,2017-02-01'
        """
        valid_params = [
            'videogame_id', 'league_id', 'serie_id', 'sort', 'filter', 'range'
        ]
        params = format_params(valid_params, **params)
        tournaments = self.get_data("tournaments/", params=params)

        return tournaments

    def get_tournament(self, tournament_id):
        """
            This function returns a single tournament dict by tournament_id

            :param tournament_id: The unique identifier for a tournament
        """
        tournament = self.get_data("tournaments/" + str(tournament_id))

        return tournament

    def get_matches(self, **params):
        """
            This function returns a list of match dicts. All parameters
            are optional. Sort, filter, and range can only use: id, slug,
            name, tournament_id, winner_id, occurrence_id, status, begin_at,
            created_at, updated_at, updated, winner_type, end_at, position.

            :param tournament_id: The unique identifier for a tournament
            :param team_id: The unique identifier for a team
            :param sort: The sort order. Sorted by id desc by default
            :param filter: Allows for filtering on one or more fields
                ex: filter='name=VCSA,Challenge France;created_at=2017-01-01'
            :param range: A hash allowing filtering for a field, as a key,
                on two comma-separated bounds. Only the fields between
                the given bounds will be returned. The bounds are inclusives.
                ex: range='created_at=2017-01-01,2017-02-01'
        """
        valid_params = ['tournament_id', 'team_id', 'sort', 'filter', 'range']
        params = format_params(valid_params, **params)
        matches = self.get_data("matches/", params=params)

        return matches

    def get_match(self, match_id):
        """
            This function returns a single match dict by match_id

            :param match_id: The unique identifier for a match
        """
        match = self.get_data("matches/" + str(match_id))

        return match

    def get_players(self, **params):
        """
            This function returns a list of player dicts. All parameters
            are optional. Sort, filter, and range can only use: id, slug,
            name, tournament_id, winner_id, occurrence_id, status, begin_at,
            created_at, updated_at, updated, winner_type, end_at, position.

            :param match_id: The unique identifier for a match
            :param sort: The sort order. Sorted by id desc by default
            :param filter: Allows for filtering on one or more fields
                ex: filter='name=VCSA,Challenge France;created_at=2017-01-01'
            :param range: A hash allowing filtering for a field, as a key,
                on two comma-separated bounds. Only the fields between
                the given bounds will be returned. The bounds are inclusives.
                ex: range='created_at=2017-01-01,2017-02-01'
        """
        valid_params = ['match_id', 'sort', 'filter', 'range']
        params = format_params(valid_params, **params)
        players = self.get_data("players/", params=params)

        return players

    def get_player(self, player_id):
        """
            This function returns a single match dict by player_id

            :param player_id: The unique identifier for a player
        """
        player = self.get_data("players/" + str(player_id))

        return player
