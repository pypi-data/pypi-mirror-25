import unittest
import responses

from pandascore import lol
from tests.base_test import BaseTest


class TestLeagueOfLegends(BaseTest):
    def setUp(self):
        super(TestLeagueOfLegends, self).setUp()
        self.lol = lol.LeagueOfLegends(access_token=self.access_token)

    @responses.activate
    def test_get_champion(self):
        data = self.load_from_file('lol_champion.json')

        url = self.base_url + 'lol/champions/556'
        responses.add(
            responses.GET,
            url,
            body=data,
            status=200,
            content_type='application/json')

        champion = self.lol.get_champion(champion_id=556)

        self.assert_get_url_equal(responses.calls[0].request.url, url)
        self.assertEqual(champion['id'], 556)

    @responses.activate
    def test_get_champions(self):
        data = self.load_from_file('lol_champions.json')

        url = self.base_url + "lol/champions/"
        responses.add(
            responses.GET,
            url,
            body=data,
            status=200,
            content_type='application/json')

        champions = self.lol.get_champions()

        self.assert_get_url_equal(responses.calls[0].request.url, url)
        self.assertEqual(champions[1]['id'], 555)

    @responses.activate
    def test_get_item(self):
        data = self.load_from_file('lol_item.json')

        url = self.base_url + 'lol/items/555'
        responses.add(
            responses.GET,
            url,
            body=data,
            status=200,
            content_type='application/json')

        item = self.lol.get_item(item_id=555)

        self.assert_get_url_equal(responses.calls[0].request.url, url)
        self.assertEqual(item['id'], 555)

    @responses.activate
    def test_get_items(self):
        data = self.load_from_file('lol_items.json')

        url = self.base_url + "lol/items/"
        responses.add(
            responses.GET,
            url,
            body=data,
            status=200,
            content_type='application/json')

        items = self.lol.get_items()

        self.assert_get_url_equal(responses.calls[0].request.url, url)
        self.assertEqual(items[1]['id'], 554)

    @responses.activate
    def test_get_mastery(self):
        data = self.load_from_file('lol_mastery.json')

        url = self.base_url + 'lol/masteries/689'
        responses.add(
            responses.GET,
            url,
            body=data,
            status=200,
            content_type='application/json')

        mastery = self.lol.get_mastery(mastery_id=689)

        self.assert_get_url_equal(responses.calls[0].request.url, url)
        self.assertEqual(mastery['id'], 689)

    @responses.activate
    def test_get_masteries(self):
        data = self.load_from_file('lol_masteries.json')

        url = self.base_url + "lol/masteries/"
        responses.add(
            responses.GET,
            url,
            body=data,
            status=200,
            content_type='application/json')

        masteries = self.lol.get_masteries()

        self.assert_get_url_equal(responses.calls[0].request.url, url)
        self.assertEqual(masteries[1]['id'], 688)

    @responses.activate
    def test_get_rune(self):
        data = self.load_from_file('lol_rune.json')

        url = self.base_url + 'lol/runes/310'
        responses.add(
            responses.GET,
            url,
            body=data,
            status=200,
            content_type='application/json')

        rune = self.lol.get_rune(rune_id=310)

        self.assert_get_url_equal(responses.calls[0].request.url, url)
        self.assertEqual(rune['id'], 310)

    @responses.activate
    def test_get_runes(self):
        data = self.load_from_file('lol_runes.json')

        url = self.base_url + "lol/runes/"
        responses.add(
            responses.GET,
            url,
            body=data,
            status=200,
            content_type='application/json')

        runes = self.lol.get_runes()

        self.assert_get_url_equal(responses.calls[0].request.url, url)
        self.assertEqual(runes[1]['id'], 309)

    @responses.activate
    def test_get_spell(self):
        data = self.load_from_file('lol_spell.json')

        url = self.base_url + 'lol/spells/18'
        responses.add(
            responses.GET,
            url,
            body=data,
            status=200,
            content_type='application/json')

        spell = self.lol.get_spell(spell_id=18)

        self.assert_get_url_equal(responses.calls[0].request.url, url)
        self.assertEqual(spell['id'], 18)

    @responses.activate
    def test_get_spells(self):
        data = self.load_from_file('lol_spells.json')

        url = self.base_url + "lol/spells/"
        responses.add(
            responses.GET,
            url,
            body=data,
            status=200,
            content_type='application/json')

        spells = self.lol.get_spells()

        self.assert_get_url_equal(responses.calls[0].request.url, url)
        self.assertEqual(spells[1]['id'], 17)

    @responses.activate
    def test_get_game(self):
        data = self.load_from_file('lol_game.json')

        url = self.base_url + 'lol/games/165211'
        responses.add(
            responses.GET,
            url,
            body=data,
            status=200,
            content_type='application/json')

        game = self.lol.get_game(game_id=165211)

        self.assert_get_url_equal(responses.calls[0].request.url, url)
        self.assertEqual(game['id'], 165211)

    @responses.activate
    def test_get_games(self):
        data = self.load_from_file('lol_games.json')

        url = self.base_url + "lol/games/"
        responses.add(
            responses.GET,
            url,
            body=data,
            status=200,
            content_type='application/json')

        games = self.lol.get_games()

        self.assert_get_url_equal(responses.calls[0].request.url, url)
        self.assertEqual(games[1]['id'], 165212)

    @responses.activate
    def test_get_player(self):
        data = self.load_from_file('lol_player.json')

        url = self.base_url + 'lol/players/7665'
        responses.add(
            responses.GET,
            url,
            body=data,
            status=200,
            content_type='application/json')

        player = self.lol.get_player(player_id=7665)

        self.assert_get_url_equal(responses.calls[0].request.url, url)
        self.assertEqual(player['id'], 7665)

    @responses.activate
    def test_get_tournament_players(self):
        data = self.load_from_file('lol_tournament_players.json')

        url = self.base_url + 'lol/tournaments/300/players'
        responses.add(
            responses.GET,
            url,
            body=data,
            status=200,
            content_type='application/json')

        players = self.lol.get_tournament_players(tournament_id=300)

        self.assert_get_url_equal(responses.calls[0].request.url, url)
        self.assertEqual(players[1]['id'], 1691)

    @responses.activate
    def test_get_serie_players(self):
        data = self.load_from_file('lol_serie_players.json')

        url = self.base_url + 'lol/series/1306/players'
        responses.add(
            responses.GET,
            url,
            body=data,
            status=200,
            content_type='application/json')

        players = self.lol.get_serie_players(serie_id=1306)

        self.assert_get_url_equal(responses.calls[0].request.url, url)
        self.assertEqual(players[1]['id'], 3546)

    @responses.activate
    def test_get_players(self):
        data = self.load_from_file('lol_players.json')

        url = self.base_url + "lol/players/"
        responses.add(
            responses.GET,
            url,
            body=data,
            status=200,
            content_type='application/json')

        players = self.lol.get_players()

        self.assert_get_url_equal(responses.calls[0].request.url, url)
        self.assertEqual(players[1]['id'], 7664)
