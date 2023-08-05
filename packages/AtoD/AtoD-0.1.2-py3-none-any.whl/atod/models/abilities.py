import pandas as pd
from sqlalchemy.orm import sessionmaker, scoped_session

from atod import Ability
from atod.db import engine
from atod.db_models.ability import AbilityModel
from atod.db_models.ability_texts import AbilityTextsModel
from atod.models.interfaces import Group

session = scoped_session(sessionmaker(bind=engine))


class Abilities(Group):
    ''' Any amount of abilities as one substance. '''

    member_type = Ability

    # TODO: write version with levels arguments
    @classmethod
    def from_hero_id(cls, hero_id, patch=''):
        ''' Adds to members all abilities of the hero with `hero_id`. '''
        response = session.query(AbilityModel.ID)
        response = response.filter(AbilityModel.HeroID == hero_id).all()

        if len(response) == 0:
            report = 'No abilities for this HeroID == {}'.format(hero_id)
            raise ValueError(report)

        members_ = [cls.member_type(a[0], patch=patch) for a in response]

        return cls(members_)

    # TODO: this can be generalized with `member_type.model.ID`
    @classmethod
    def all(cls):
        ''' Creates Abilities object with all heroes' abilities in the game.'''
        ids = [x[0] for x in session.query(AbilityModel.ID).all()]
        # XXX: would be nice to create members only if they are needed
        members_ = [Ability(id_) for id_ in ids]

        return cls(members_)

    def get_description(self):
        ''' Returns sum of abilities labels. 
        
        Function takes all the descriptions of abilities (by labels) and sums
        them up field by field.

        Results:
            pd.Series: where value in every labels is sum between all the
                abilities in object.
        '''
        # add all labels to one DataFrame
        labels = pd.DataFrame([m.get_description(['labels'])
                               for m in self.members])

        # sum columns in the DataFrame
        labels_summary = pd.Series([sum(labels[c])
                                    for c in labels.columns])

        return labels_summary
