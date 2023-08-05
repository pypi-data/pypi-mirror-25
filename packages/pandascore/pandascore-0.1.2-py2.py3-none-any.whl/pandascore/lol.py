""" Python interface to PandaScore League of Legends API """

try:
    from urlparse import urlparse, parse_qs
except ImportError:
    from urllib.parse import urlparse, parse_qs

from .api import Api
from .util import format_params


class LeagueOfLegends(Api):
    """ Python interface to PandaScore League of Legends API """

    def __init__(self, *args, **kwargs):
        super(LeagueOfLegends, self).__init__(*args, **kwargs)

    def get_champions(self, **params):
        """
            This function returns a list of champion dicts. All parameters
            are optional. Sort, filter, and range can only use: id, champion_lol_id,
            image, name, armor, armorperlevel, attackdamage, attackdamageperlevel,
            attackrange, attackspeedoffset, attackspeedperlevel, crit, critperlevel,
            hp, hpperlevel, hpregen, hpregenperlevel, movespeed, mp, mpperlevel,
            mpregen, mpregenperlevel, spellblock, spellblockperlevel, created_at,
            updated_at, big_image.

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
        champions = self.get_data("lol/champions/", params=params)

        return champions

    def get_champion(self, champion_id):
        """
            This function returns a single champion dict by champion_id

            :param champion_id: The unique identifier for a champion
        """
        champion = self.get_data("lol/champions/" + str(champion_id))

        return champion

    def get_items(self, **params):
        """
            This function returns a list of items dicts. All parameters
            are optional. Sort, filter, and range can only use: id, item_lol_id,
            name, image, gold_total, gold_base, gold_sell, gold_purchasable,
            consumed, in_store, flat_magic_damage_mod, flat_crit_chance_mod,
            percent_attack_speed_mod, percent_movement_speed_mod, flat_hp_pool_mod,
            flat_movement_speed_mod, flat_armor_mod, flat_spell_block_mod,
            flat_physical_damage_mod, percent_life_steal_mod, flat_hp_regen_mod,
            flat_mp_regen_mod, flat_mp_pool_mod, created_at, updated_at.

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
        items = self.get_data("lol/items/", params=params)

        return items

    def get_item(self, item_id):
        """
            This function returns a single item dict by item_id

            :param item_id: The unique identifier for a item
        """
        item = self.get_data("lol/items/" + str(item_id))

        return item

    def get_masteries(self, **params):
        """
            This function returns a list of masteries dicts. All parameters
            are optional. Sort, filter, and range can only use: id, mastery_lol_id,
            name, image, created_at, updated_at.

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
        masteries = self.get_data("lol/masteries/", params=params)

        return masteries

    def get_mastery(self, mastery_id):
        """
            This function returns a single mastery dict by mastery_id

            :param mastery_id: The unique identifier for a mastery
        """
        mastery = self.get_data("lol/masteries/" + str(mastery_id))

        return mastery

    def get_runes(self, **params):
        """
            This function returns a list of runes dicts. All parameters
            are optional. Sort, filter, and range can only use: id, rune_lol_id,
            name, image, created_at, updated_at.

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
        runes = self.get_data("lol/runes/", params=params)

        return runes

    def get_rune(self, rune_id):
        """
            This function returns a single rune dict by rune_id

            :param rune_id: The unique identifier for a rune
        """
        rune = self.get_data("lol/runes/" + str(rune_id))

        return rune

    def get_spells(self, **params):
        """
            This function returns a list of spells dicts. All parameters
            are optional. Sort, filter, and range can only use: id, spell_lol_id,
            name, image, created_at, updated_at.

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
        spells = self.get_data("lol/spells/", params=params)

        return spells

    def get_spell(self, spell_id):
        """
            This function returns a single spell dict by spell_id

            :param spell_id: The unique identifier for a spell
        """
        spell = self.get_data("lol/spells/" + str(spell_id))

        return spell

    def get_games(self, **params):
        """
            This function returns a list of games dicts. All parameters
            are optional. Sort, filter, and range can only use: id, match_id,
            position, length, game_lol_id, winner_id, begin_at, get_detailed_info,
            created_at, updated_at, get_detailed_advance, updated, finished,
            winner_type.

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
        games = self.get_data("lol/games/", params=params)

        return games

    def get_game(self, game_id):
        """
            This function returns a single game dict by game_id

            :param game_id: The unique identifier for a game
        """
        game = self.get_data("lol/games/" + str(game_id))

        return game

    def get_players(self, **params):
        """
            This function returns a list of players dicts. All parameters
            are optional. Sort, filter, and range can only use: id, hometown,
            name, first_name, last_name, role, bio, image, created_at,
            updated_at, slug.

            :param serie_id: The unique identifier for a series
            :param tournament_id: The unique identifier for a tournament
            :param sort: The sort order. Sorted by id desc by default
            :param filter: Allows for filtering on one or more fields
                ex: filter='name=VCSA,Challenge France;created_at=2017-01-01'
            :param range: A hash allowing filtering for a field, as a key,
                on two comma-separated bounds. Only the fields between
                the given bounds will be returned. The bounds are inclusives.
                ex: range='created_at=2017-01-01,2017-02-01'
        """
        valid_params = ['sort', 'filter', 'range', 'serie_id', 'tournament_id']
        params = format_params(valid_params, **params)
        players = self.get_data("lol/players/", params=params)

        return players

    def get_tournament_players(self, tournament_id):
        """
            This function returns a list of players dicts for a specific tournament

            :param tournament_id: The unique identifier for a tournament
        """
        players = self.get_data("lol/tournaments/" + str(tournament_id) +
                                "/players")

        return players

    def get_serie_players(self, serie_id):
        """
            This function returns a list of players dicts for a specific serie

            :param serie_id: The unique identifier for a series
        """
        players = self.get_data("lol/series/" + str(serie_id) + "/players")

        return players

    def get_player(self, player_id):
        """
            This function returns a single player dict by player_id

            :param player_id: The unique identifier for a player
        """
        player = self.get_data("lol/players/" + str(player_id))

        return player
