import unittest
import responses

from pandascore import pandascore
from tests.base_test import BaseTest


class TestPandaScore(BaseTest):
    def setUp(self):
        super(TestPandaScore, self).setUp()
        self.pandascore = pandascore.PandaScore(access_token=self.access_token)

    @responses.activate
    def test_get_league(self):
        data = self.load_from_file('league.json')

        url = self.base_url + 'leagues/1'
        responses.add(
            responses.GET,
            url,
            body=data,
            status=200,
            content_type='application/json')

        league = self.pandascore.get_league(league_id=1)

        self.assert_get_url_equal(responses.calls[0].request.url, url)
        self.assertEqual(self.pandascore.access_token, self.access_token)
        self.assertEqual(league['id'], 1)

    @responses.activate
    def test_get_leagues(self):
        data = self.load_from_file('leagues.json')

        url = self.base_url + "leagues/"
        responses.add(
            responses.GET,
            url,
            body=data,
            status=200,
            content_type='application/json')

        leagues = self.pandascore.get_leagues()

        self.assert_get_url_equal(responses.calls[0].request.url, url)
        self.assertEqual(leagues[1]['id'], 2)

    @responses.activate
    def test_get_serie(self):
        data = self.load_from_file('serie.json')

        url = self.base_url + 'series/1299'
        responses.add(
            responses.GET,
            url,
            body=data,
            status=200,
            content_type='application/json')

        serie = self.pandascore.get_serie(series_id=1299)

        self.assert_get_url_equal(responses.calls[0].request.url, url)
        self.assertEqual(serie['id'], 1299)

    @responses.activate
    def test_get_series(self):
        data = self.load_from_file('series.json')

        url = self.base_url + "series/"
        responses.add(
            responses.GET,
            url,
            body=data,
            status=200,
            content_type='application/json')

        series = self.pandascore.get_series()

        self.assert_get_url_equal(responses.calls[0].request.url, url)
        self.assertEqual(series[1]['id'], 1298)

    @responses.activate
    def test_get_tournament(self):
        data = self.load_from_file('tournament.json')

        url = self.base_url + 'tournaments/530'
        responses.add(
            responses.GET,
            url,
            body=data,
            status=200,
            content_type='application/json')

        tournament = self.pandascore.get_tournament(tournament_id=530)

        self.assert_get_url_equal(responses.calls[0].request.url, url)
        self.assertEqual(tournament['id'], 530)

    @responses.activate
    def test_get_tournaments(self):
        data = self.load_from_file('tournaments.json')

        url = self.base_url + "tournaments/"
        responses.add(
            responses.GET,
            url,
            body=data,
            status=200,
            content_type='application/json')

        tournaments = self.pandascore.get_tournaments()

        self.assert_get_url_equal(responses.calls[0].request.url, url)
        self.assertEqual(tournaments[1]['id'], 532)

    @responses.activate
    def test_get_match(self):
        data = self.load_from_file('match.json')

        url = self.base_url + 'matches/18163'
        responses.add(
            responses.GET,
            url,
            body=data,
            status=200,
            content_type='application/json')

        match = self.pandascore.get_match(match_id=18163)

        self.assert_get_url_equal(responses.calls[0].request.url, url)
        self.assertEqual(match['id'], 18163)

    @responses.activate
    def test_get_matches(self):
        data = self.load_from_file('matches.json')

        url = self.base_url + "matches/"
        responses.add(
            responses.GET,
            url,
            body=data,
            status=200,
            content_type='application/json')

        matches = self.pandascore.get_matches()

        self.assert_get_url_equal(responses.calls[0].request.url, url)
        self.assertEqual(matches[1]['id'], 18165)

    @responses.activate
    def test_get_player(self):
        data = self.load_from_file('player.json')

        url = self.base_url + 'players/7614'
        responses.add(
            responses.GET,
            url,
            body=data,
            status=200,
            content_type='application/json')

        player = self.pandascore.get_player(player_id=7614)

        self.assert_get_url_equal(responses.calls[0].request.url, url)
        self.assertEqual(player['id'], 7614)

    @responses.activate
    def test_get_players(self):
        data = self.load_from_file('players.json')

        url = self.base_url + "players/"
        responses.add(
            responses.GET,
            url,
            body=data,
            status=200,
            content_type='application/json')

        players = self.pandascore.get_players()

        self.assert_get_url_equal(responses.calls[0].request.url, url)
        self.assertEqual(players[1]['id'], 7654)
