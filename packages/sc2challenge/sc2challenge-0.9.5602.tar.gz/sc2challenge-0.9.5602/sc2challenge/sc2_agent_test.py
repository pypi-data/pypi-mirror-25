import os
import unittest

from sc2challenge import SC2Agent


class TestSC2Agent(unittest.TestCase):
    def setUp(self):
        self.token = os.getenv('METRICS_TOKEN', None)

    def test_init_with_token(self):
        agent = SC2Agent(token=self.token)
        self.assertIsNotNone(agent)

    def test_init_without_token(self):
        agent = SC2Agent()
        self.assertIsNotNone(agent)

    def test_reset(self):
        agent = SC2Agent(token=self.token)
        agent.setup(None, None)
        self.assertIsNotNone(agent)
        self.assertEqual(agent.episodes, 0)
        agent.reset()
        self.assertEqual(agent.episodes, 1)
        agent.reset()
        self.assertEqual(agent.episodes, 2)

    def test_step(self):
        agent = SC2Agent(token=self.token)
        agent.setup(None, None)
        self.assertIsNotNone(agent)
        obs = DummyObservation()
        agent.step(obs)
        self.assertEqual(agent.reward, 0)
        agent.step(obs)
        self.assertEqual(agent.reward, 0)
        obs.reward = 1
        agent.step(obs)
        self.assertEqual(agent.reward, 1)


class DummyObservation:
    def __init__(self):
        self.reward = 0
