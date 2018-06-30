import tensorflow as tf
import sys
import os
import json

PATH = "../04.seq2seq"
sys.path.insert(0, PATH)

from model import seq2seq
from data_process import sentence_to_char_index

model = dict()
vocab = None
reverse_vocab = dict()


def setup():
    global model, vocab, reverse_vocab

    sess = tf.Session()
    with open(os.path.join(PATH, 'vocab.json'), 'r') as fp:
        vocab = json.load(fp)
    reverse_vocab = dict()
    for key, value in vocab.items():
        reverse_vocab[value] = key
    vocab_size = len(vocab)
    model = seq2seq(sess, encoder_vocab_size=vocab_size, decoder_vocab_size=vocab_size, max_step=50)
    saver = tf.train.Saver()
    saver.restore(sess, tf.train.latest_checkpoint(PATH + '/models'))


def get_response(content):
    input = sentence_to_char_index([content], vocab, False)
    result = model.inference([input])

    for sentence in result:
        response = ""
        for index in sentence:
            if index == 0:
                break
            response += reverse_vocab[index]

    return response
