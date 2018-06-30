import tensorflow as tf
import sys
import os
import json

PATH = "../04.seq2seq"
sys.path.insert(0, PATH)

from model import seq2seq
from data_process import sentence_to_char_index

model = None
vocab = dict()
reverse_vocab = dict()

def setup():
    global model, vocab, reverse_vocab

    with open(os.path.join(PATH, 'vocab.json'), 'r') as fp:
        vocab = json.load(fp)
    reverse_vocab = dict()
    for key, value in vocab.items():
        reverse_vocab[value] = key
    vocab_size = len(vocab)

    config = tf.ConfigProto()
    config.gpu_options.allow_growth = True
    sess = tf.Session(config=config)
    model = seq2seq(sess, encoder_vocab_size=vocab_size, decoder_vocab_size=vocab_size, max_step=50)
    saver = tf.train.Saver()
    saver.restore(sess, tf.train.latest_checkpoint(PATH + '/models'))


def get_response(content):
    input = sentence_to_char_index([content], vocab, False)
    result = model.inference([input])
    response = ""
    for index in result[0]:
        if index == 0:
            break
        response += reverse_vocab[index]
    return response
