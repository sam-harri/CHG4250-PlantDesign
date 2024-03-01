import tensorflow as tf
from tf_agents.networks import actor_distribution_network
from tf_agents.agents.sac import sac_agent
from tf_agents.environments import tf_py_environment
from tf_agents.agents.ddpg import critic_network
from tf_agents.replay_buffers import tf_uniform_replay_buffer
from tf_agents.trajectories import trajectory
import numpy as np
from trainenv import SXExtractionSimulatorEnv
import simulatorenv

train_env = tf_py_environment.TFPyEnvironment(SXExtractionSimulatorEnv())


actor_net = actor_distribution_network.ActorDistributionNetwork(
    train_env.observation_spec(),
    train_env.action_spec(),
    fc_layer_params=(32, 64, 64, 32),
)

critic_net_input_specs = (train_env.observation_spec(), train_env.action_spec())
critic_net = critic_network.CriticNetwork(
    critic_net_input_specs, joint_fc_layer_params=(32, 64, 64, 32)
)

tf_agent = sac_agent.SacAgent(
    train_env.time_step_spec(),
    train_env.action_spec(),
    actor_network=actor_net,
    critic_network=critic_net,
    actor_optimizer=tf.keras.optimizers.Adam(learning_rate=0.0001),
    critic_optimizer=tf.keras.optimizers.Adam(learning_rate=0.0001),
    alpha_optimizer=tf.keras.optimizers.Adam(learning_rate=0.0001),
    target_update_tau=0.005,
    target_update_period=1,
    td_errors_loss_fn=tf.math.squared_difference,
    gamma=0.99,
    reward_scale_factor=1.0,
    train_step_counter=tf.Variable(0),
)

tf_agent.initialize()

replay_buffer = tf_uniform_replay_buffer.TFUniformReplayBuffer(
    data_spec=tf_agent.collect_data_spec,
    batch_size=train_env.batch_size,
    max_length=100,
)


def collect_step(environment, policy, buffer):
    time_step = environment.current_time_step()
    action_step = policy.action(time_step)
    next_time_step = environment.step(action_step.action)
    traj = trajectory.from_transition(time_step, action_step, next_time_step)
    buffer.add_batch(traj)


for _ in range(64):
    collect_step(train_env, tf_agent.collect_policy, replay_buffer)

num_iterations = 10000
collect_steps_per_iteration = 1
batch_size = 64
dataset = replay_buffer.as_dataset(
    num_parallel_calls=3, sample_batch_size=batch_size, num_steps=2
).prefetch(3)

iterator = iter(dataset)

best_reward = -np.inf
best_action = None

for i in range(num_iterations):
    print(f"Iterations {i}")

    for _ in range(collect_steps_per_iteration):
        collect_step(train_env, tf_agent.collect_policy, replay_buffer)

    if replay_buffer._num_frames() >= batch_size:
        experience, unused_info = next(iterator)
        train_loss = tf_agent.train(experience).loss

        time_step = train_env.current_time_step()
        action_step = tf_agent.policy.action(time_step)
        action = action_step.action.numpy()
        next_time_step = train_env.step(action)
        reward = next_time_step.reward.numpy()


print(simulatorenv.BEST_PARAMS)
print(simulatorenv.BEST_REWARD)
