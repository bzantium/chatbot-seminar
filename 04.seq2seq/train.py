from model import seq2seq
import tensorflow as tf
import os, re, json
import numpy as np
from data_process import *

if __name__ == "__main__":
    DIR = "models"
    sess = tf.Session()
    data = []
    with open('./data/dialog.txt', encoding='utf-8') as f:
        for line in f:
            data.append(re.sub('\n', '', line))
    vocab, reverse_vocab, vocab_size = build_character(data)
    with open('vocab.json', 'w') as fp:
        json.dump(vocab, fp)
    model = seq2seq(sess, encoder_vocab_size=vocab_size, decoder_vocab_size=vocab_size, max_step=50)
    input, target = make_dataset(data)
    batches = batch_iter(list(zip(input, target)), batch_size=64, num_epochs=3001)

    saver = tf.train.Saver(max_to_keep=5, keep_checkpoint_every_n_hours=0.5)
    avgLoss = []
    for step, batch in enumerate(batches):
        x_train, y_train = zip(*batch)
        x_train = sentence_to_char_index(x_train, vocab, is_target=False)
        y_train = sentence_to_char_index(y_train, vocab, is_target=True)
        l, _ = model.train(x_train, y_train)
        avgLoss.append(l)
        if step % 500 == 0:
            print('batch:', '%04d' % step, 'loss:', '%05f' % np.mean(avgLoss))
            saver.save(sess, os.path.join(DIR, "model"), global_step=step)
            avgLoss = []