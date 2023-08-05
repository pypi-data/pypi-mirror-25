''' Class to get match description. '''
import dota2api
import pandas as pd

from atod import Hero, Heroes, files
from atod.utils.dota_api import api


class Match(object):
    ''' Representation of the single match.

    Attributes:
        id (int)        : id of the match
        radiant (Heroes): Heroes in radiant team
        dire    (Heroes): Heroes in dire team
    '''

    def __init__(self, match_id: int):
        ''' Calls the API and creates a match representation from result.

        Args:
            match_id: Dota match ID
        '''

        if not isinstance(match_id, int):
            raise TypeError('`match_id` must have type int.')
        else:
            self.id = match_id

        response = api.get_match_details(match_id=match_id)

        # TODO: check supported modes, rewrote this
        if response['game_mode'] != 2 and response['game_mode'] != 16:
            raise NotImplementedError('Sorry, Match currently'
                    + ' does not support {}'.format(response['game_mode_name'])
                    + ' game mode.')

        self.radiant = Heroes()
        self.dire = Heroes()
        self.radiant_win = response['radiant_win']

        # select picks and add heroes to appropriate teams
        for pick in filter(lambda x: x['is_pick'], response['picks_bans']):
            if pick['team'] == 0:
                self.radiant.add(Hero(pick['hero_id']))
            else:
                self.dire.add(Hero(pick['hero_id']))

    def get_description(self, include):
        ''' Returns description of certain match.

        Description consist of 3 parts: radiant description, dire description
        and result. Complete length of description vector is 2n + 1, where
        n is a length of side description (depends on choosen parameters).

        Args:
            include (list): the same with Hero.get_description().

        Returns:
            pd.Series

        '''

        # get descriptions of sides
        radiant_description = self.radiant.get_description(include)
        dire_description    = self.dire.get_description(include)

        len_desc = radiant_description.shape[0]

        # create array for MultiIndex object
        index_arrays = [['radiant'] * len_desc + ['dire'] * len_desc,
                        list(radiant_description.index) * 2]

        # convert array to list of tuples
        index_tuples = list(zip(*index_arrays))
        # add result comlumn
        index_tuples.append(('result', 'radiant_win'))

        index = pd.MultiIndex.from_tuples(index_tuples,
                                          names=['side', 'variables'])

        # unite all the columns
        variables = [*radiant_description, *dire_description, self.radiant_win]
        description = pd.Series(variables, index=index)

        return description

