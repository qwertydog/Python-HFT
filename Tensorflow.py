import Database as Database
import tensorflow as tf
import numpy as np


class Tensorflow(object):
    def __init__(self, db: Database):
        self._db = db

        self.x = tf.placeholder(tf.float32, [None, 9])  # input
        self.y_ = tf.placeholder(tf.float32, [None, 2])  # output

        self.m = tf.Variable(tf.zeros([9, 2]))  # weight
        self.c = tf.Variable(tf.zeros([2]))  # bias

        self.y = tf.matmul(self.x, self.m) + self.c    # y = mx + c (y = Wx + b) (predicted output using linear model)

        self.cross_entropy = tf.reduce_mean(tf.nn.softmax_cross_entropy_with_logits(self.y, self.y_))

        self.train_step = tf.train.GradientDescentOptimizer(0.5).minimize(self.cross_entropy)

        init = tf.global_variables_initializer()

        self.sess = tf.Session()
        self.sess.run(init)

    def run(self, currencies):
        data = self._db.execute("""SELECT last, lowestAsk, highestBid, percentChange, baseVolume, quoteVolume, last24hrHigh, last24hrLow
                                   FROM exchangeCurrencyLog
                                   WHERE currency1Id = ? AND currency2Id = ?
                                   ORDER BY timestamp DESC
                                   LIMIT 2;""", (currencies[0], currencies[1]))

        rows = data.fetchall()
        if not rows or rows[0] is None or rows[1] is None:
            return

        tf_input = [rows[0]['time'] - rows[1]['time'],
                    rows[0]['last'] - rows[1]['last'],
                    rows[0]['lowestAsk'] - rows[1]['lowestAsk'],
                    rows[0]['highestBid'] - rows[1]['highestBid'],
                    rows[0]['percentChange'] - rows[1]['percentChange'],
                    rows[0]['baseVolume'] - rows[1]['baseVolume'],
                    rows[0]['quoteVolume'] - rows[1]['quoteVolume'],
                    rows[0]['last24hrHigh'] - rows[1]['last24hrHigh'],
                    rows[0]['last24hrLow'] - rows[1]['last24hrLow']]

        self.sess.run(self.train_step, feed_dict={self.x: tf_input})

        #correct_prediction = tf.equal(tf.argmax(y, 1), tf.argmax(y_, 1))

        #accuracy = tf.reduce_mean(tf.cast(correct_prediction, tf.float32))

        #print(self.sess.run(accuracy, feed_dict={x: mnist.test.images, y_: mnist.test.labels}))

