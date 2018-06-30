import tensorflow as tf
import sys
import re
import json

PATH = "../03.sentiment"
sys.path.insert(0, PATH)

from model import CNN
from data_process import sentence_to_index_morphs

model = dict()
vocab = None
max_length = None


def setup():
    global model, vocab, max_length
    # load vocab, vocab_size, max_length
    with open(os.path.join(PATH, 'vocab.json') as fp:
        vocab = json.load(fp)

    with open(os.path.join(PATH, 'vocab.json') as f:
        vocab_size = int(re.sub('\n', '', f.readline()))
        max_length = int(f.readline())

    config = tf.ConfigProto()
    config.gpu_options.allow_growth = True
    sess = tf.Session(config=config)
    model = CNN(sess=sess, vocab_size=vocab_size, sequence_length=max_length, trainable=True)
    saver = tf.train.Saver()
    saver.restore(sess, tf.train.latest_checkpoint(PATH))


def get_response(content):
    speak = sentence_to_index_morphs([content], vocab, max_length)
    label, prob = model.predict(speak)

    if prob[0] < 0.6:
        response = '차분해 보이시네요 :)'
    else:
        if label[0] == 0:
            response = '기분이 좋지 않아 보여요 :('
        else:
            response = '기분이 좋아 보이시네요!'

    return response
