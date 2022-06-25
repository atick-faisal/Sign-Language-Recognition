import tensorflow as tf


class ConvNet2D(tf.keras.layers.Layer):
    def __init__(
        self,
        base_model: tf.keras.Model
    ):
        super(ConvNet2D, self).__init__()
        self.base_model = base_model
        self.preprocessing = tf.keras.layers.experimental.preprocessing.Rescaling(
            scale=1.0/127.5,
            offset=-1
        )
        self.base_model.trainable = False

    def call(self, inputs):
        x = self.preprocessing(inputs)
        x = self.base_model(x, training=False)
        output = tf.keras.layers.GlobalAveragePooling2D()(x)

        return output
