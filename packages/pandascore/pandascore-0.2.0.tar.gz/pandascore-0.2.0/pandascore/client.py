""" Python interface to all PandaScore APIs """

from .api import Api
from .pandascore import PandaScore
from .lol import LeagueOfLegends


class Client(Api):
    """ Python interface to all PandaScore APIs """

    def __init__(self, *args, **kwargs):
        super(Client, self).__init__(*args, **kwargs)
        self.all_games = PandaScore(**kwargs)
        self.lol = LeagueOfLegends(**kwargs)
