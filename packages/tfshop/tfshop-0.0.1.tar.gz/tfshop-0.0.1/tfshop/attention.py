import tensorflow as tf


def soft_attention(encoder_seq, decoder_state, encdim, attdim, decdim):
    """
    expects all in batch major format  [batch, time, dim]

    encoder_seq     : the sequence of encoder states/etc
    decoder_state   : current state of the decoder
    encdim          : dim of encoder state
    attdim          : dim of attention representation
    decdim          : dim of decoder

    returns
        attention   : [batch, time]
    """
    # [batch, time, dim] -> time x [batch, dim]
    eseq = tf.unstack(encoder_seq, axis=1)
    rui = tf.random_uniform_initializer(0., 1.)
    with tf.variable_scope('soft_attention'):
        attention_vals = []
        v = tf.get_variable('v', shape=(attdim, 1), initializer=rui)
        wd = tf.get_variable('wd', shape=(decdim, attdim), initializer=rui)
        bd = tf.get_variable('bd', shape=(attdim, ), initializer=rui)
        ud = tf.matmul(decoder_state, wd) + bd
        for index, e in enumerate(eseq):
            if index > 0:
                tf.get_variable_scope().reuse_variables()
            we = tf.get_variable('we', shape=(encdim, attdim), initializer=rui)
            be = tf.get_variable('be', shape=(attdim, ), initializer=rui)
            ue = tf.matmul(e, we) + be
            u = tf.squeeze(tf.matmul(tf.nn.tanh(ue + ud), v))
            attention_vals.append(u)
        attention = tf.nn.softmax(tf.stack(attention_vals, axis=1), axis=-1)
    return attention
