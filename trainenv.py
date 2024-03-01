import numpy as np
from tf_agents.environments import py_environment
from tf_agents.specs import array_spec
from tf_agents.trajectories import time_step as ts
from simulatorenv import SXSimulator


class SXExtractionSimulatorEnv(py_environment.PyEnvironment):
    def __init__(self):
        self._action_spec = array_spec.BoundedArraySpec(
            shape=(6,),
            dtype=np.float32,
            minimum=[4, 5, 1, 1.5, 0.005, 0.008],
            maximum=[4, 5, 2, 3.5, 0.1, 0.8],
            name="action",
        )
        self._observation_spec = array_spec.ArraySpec(
            shape=(), dtype=np.float32, name="observation"
        )
        self._episode_ended = False

    def action_spec(self):
        return self._action_spec

    def observation_spec(self):
        return self._observation_spec

    def _reset(self):
        self._episode_ended = False
        # Return a dummy observation
        return ts.restart(np.array(0, dtype=np.float32))

    def _step(self, action):
        if self._episode_ended:
            return self.reset()

        (
            num_stage_extract,
            num_stage_strip,
            OA_extract,
            OA_strip,
            tentative_BO,
            tentative_DR,
        ) = action
        reward = SXSimulator(
            int(num_stage_extract),
            int(num_stage_strip),
            OA_extract,
            OA_strip,
            tentative_BO,
            tentative_DR,
        )
        self._episode_ended = True

        return ts.termination(np.array(0, dtype=np.float32), reward)
