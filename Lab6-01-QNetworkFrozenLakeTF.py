import gym
import numpy as np
import tensorflow as tf
import matplotlib.pyplot as plt


def one_hot(hot, n):
    return np.identity(n)[hot:hot + 1]


env = gym.make('FrozenLake-v0')

input_size = env.observation_space.n
output_size = env.action_space.n
learning_rate = 0.1

X = tf.placeholder(shape=[1, input_size], dtype=tf.float32)
W = tf.Variable(tf.random_uniform(shape=[input_size, output_size], minval=0, maxval=0.01))

Q_pred = tf.matmul(X, W)
Y = tf.placeholder(shape=[1, output_size], dtype=tf.float32)

loss = tf.reduce_sum(tf.square(Y - Q_pred))

train = tf.train.GradientDescentOptimizer(learning_rate=learning_rate).minimize(loss)

gamma = 0.99
num_episodes = 2000

rList = []

init = tf.global_variables_initializer()
with tf.Session() as sess:
    sess.run(init)
    for i in range(num_episodes):
        s = env.reset()
        e = 1.0 / ((i / 50) + 10)
        rAll = 0
        done = False

        while not done:
            Qs = sess.run(Q_pred, feed_dict={X: one_hot(s, input_size)})
            if np.random.rand(1) < e:
                a = env.action_space.sample()
            else:
                a = np.argmax(Qs)

            s1, reward, done, _ = env.step(a)
            if done:
                Qs[0, a] = reward
            else:
                Qs1 = sess.run(Q_pred, feed_dict={X: one_hot(s1, input_size)})
                Qs[0, a] = reward + gamma * np.max(Qs1)

            sess.run(train, feed_dict={X: one_hot(s, input_size), Y: Qs})

            rAll += reward
            s = s1

        rList.append(rAll)

print("Success Rate : {}".format(str(sum(rList) / num_episodes)))
plt.bar(range(len(rList)), rList, color="blue")
plt.show()
