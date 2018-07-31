import loss
from keras.models import Model
from keras.layers import *
from keras.utils import plot_model


def get_model(utils, parameters):
    if parameters["keras"] == "convolutional":
        model = convolutional(parameters)
    plot_model(model, utils["save_model_path"])
    return model


def convolutional(parameters):
    input = Input(shape=(parameters["shape_x"], parameters["shape_y"]) + (1,))

    conv_1 = Conv2D(10,
                    (parameters["filter_size"], parameters["filter_size"]),
                    activation='relu'
                    )(input)

    mp1 = MaxPooling2D(pool_size=(2, 2))(conv_1)

    dp1 = Dropout(0.25)(mp1)

    conv_2 = Conv2D(10,
                    (parameters["filter_size"], parameters["filter_size"]),
                    activation='relu'
                    )(dp1)

    mp2 = MaxPooling2D(pool_size=(2, 2))(conv_2)

    dp2 = Dropout(0.25)(mp2)

    flatten = Flatten()(dp2)

    dropout = Dropout(0.5)(flatten)

    out = Dense(10, activation=parameters["activation"])(dropout)

    model = Model(input, out)

    model.summary()

    # compile keras
    print 'compile keras...'
    if parameters["loss"] == 'bin_cross':
        model.compile(optimizer='adadelta', metrics=['accuracy'], loss='binary_crossentropy')
    elif parameters["loss"] == 'mean_squared_error':
        model.compile(optimizer='adadelta', metrics=['accuracy'], loss='mean_squared_error')
    elif parameters["loss"] == 'cat_cross':
        model.compile(optimizer='adadelta', metrics=['accuracy'], loss='categorical_crossentropy')

    return model