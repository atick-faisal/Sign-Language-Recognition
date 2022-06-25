import tensorflow as tf


class ConvNet1D(tf.keras.layers.Layer):
    def __init__(
        self,
        n_filters: int = 8,
        n_layers: int = 4,
        kernel_size: int = 3,
        pool_size: int = 2,
        feature_size: int = 32
    ):
        super(ConvNet1D, self).__init__()
        self.n_filters = n_filters
        self.n_layers = n_layers
        self.kernel_size = kernel_size
        self.pool_size = pool_size
        self.feature_size = feature_size

        self.conv_layers = []
        self.bn_layers = []

        multiplier = 1
        for i in range(1, self.n_layers + 1):
            self.conv_layers.append(tf.keras.layers.Conv1D(
                filters=self.n_filters * multiplier,
                kernel_size=self.kernel_size
            ))

            if i != 0 and i % 2 == 0:
                multiplier += 1

            self.bn_layers.append(tf.keras.layers.BatchNormalization())

        self.pool = tf.keras.layers.MaxPool1D(self.pool_size)
        self.mlp = tf.keras.layers.Dense(self.feature_size)

    def call(self, inputs, training=None):
        x = inputs
        multiplier = 1
        for i in range(1, self.n_layers + 1):
            x = self.conv_layers[i - 1](x)
            x = self.bn_layers[i - 1](x)
            x = tf.keras.activations.selu(x)

            if i % 2 == 0:
                x = self.pool(x)
                multiplier += 1

        x = tf.keras.layers.Flatten()(x)
        output = self.mlp(x)

        return output
