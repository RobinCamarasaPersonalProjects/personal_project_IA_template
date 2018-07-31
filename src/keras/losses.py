from keras import backend as K


def dice_loss(y_true, y_pred):
    intersection = K.sum(K.abs(y_true * y_pred), axis=-1)
    sum_ = K.sum(K.abs(y_true) + K.abs(y_pred), axis=-1)
    dice = 2 * intersection / (sum_ + K.epsilon())
    return (1. - dice)