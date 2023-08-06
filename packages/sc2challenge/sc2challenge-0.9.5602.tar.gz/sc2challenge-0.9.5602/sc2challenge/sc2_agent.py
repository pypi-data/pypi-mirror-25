import os

from mixpanel import Mixpanel
from pysc2.agents.base_agent import BaseAgent


class SC2Agent(BaseAgent):
    def __init__(self, token=None):
        super(SC2Agent, self).__init__()

        self._analytics = None
        if token is not None:
            self._analytics = Mixpanel(token)

        self.team_id = os.getenv('TEAM_ID', None)

        if self._analytics is not None:
            self._analytics.track(self.team_id, 'Sent Message')

    def reset(self):
        super(SC2Agent, self).reset()
        if self._analytics is not None:
            self._analytics.track(self.team_id, 'reset', {
                'episodes': self.episodes,
                'steps': self.steps,
                'reward': self.reward
            })

    def step(self, obs):
        ret = super(SC2Agent, self).step(obs)
        if self._analytics is not None:
            self._analytics.track(self.team_id, 'step', {
                'episodes': self.episodes,
                'steps': self.steps,
                'reward': self.reward
            })
        return ret
