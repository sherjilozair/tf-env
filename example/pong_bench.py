"""
Measure the speed of the Pong environment.
"""

import time

import tensorflow as tf

from tf_env import Pong


BATCH_SIZE = 16
NUM_STEPS = 512


def main():
    env = Pong()
    init_state = env.reset(BATCH_SIZE)
    states = tf.placeholder(init_state.dtype, shape=init_state.get_shape())
    actions = tf.random_uniform([BATCH_SIZE], minval=0, maxval=env.num_actions, dtype=tf.int32)
    new_states, rews, dones = env.step(states, actions)
    image = env.observe(states)
    with tf.Session() as sess:
        for render in [False, True]:
            cur_states = sess.run(init_state)
            start_time = time.time()
            for _ in range(NUM_STEPS):
                cur_states, cur_rews, cur_dones = sess.run([new_states, rews, dones],
                                                           feed_dict={states: cur_states})
                if render:
                    sess.run(image, feed_dict={states: cur_states})
            fps = NUM_STEPS * BATCH_SIZE / (time.time() - start_time)
            print('fps is %f with render=%s' % (fps, render))


if __name__ == '__main__':
    main()
