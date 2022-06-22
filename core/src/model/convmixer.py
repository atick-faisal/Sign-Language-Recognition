import tensorflow as tf


class ConvMixer(tf.keras.Model):
    def __init__(
        self,
        img_size: int,
        in_channels: int,
        n_classes: int,
        n_filters: int,
        depth: int,
        kernel_size: int,
        patch_size: int
    ):
        super(ConvMixer, self).__init__()
        self.img_size = img_size
        self.in_channels = in_channels
        self.n_filters = n_filters
        self.kernel_size = kernel_size
        self.n_classes = n_classes
        self.depth = depth
        self.patch_size = patch_size

    @staticmethod
    def activation_block(x):
        x = tf.keras.layers.Activation("gelu")(x)
        return tf.keras.layers.BatchNormalization()(x)

    def conv_stem(self, x, filters: int, patch_size: int):
        x = tf.keras.layers.Conv2D(
            filters,
            kernel_size=patch_size,
            strides=patch_size
        )(x)
        return self.activation_block(x)

    def conv_mixer_block(self, x, filters: int, kernel_size: int):
        # Depthwise convolution.
        x0 = x
        x = tf.keras.layers.DepthwiseConv2D(
            kernel_size=kernel_size, padding="same")(x)
        x = tf.keras.layers.Add()([self.activation_block(x), x0])  # Residual.

        # Pointwise convolution.
        x = tf.keras.layers.Conv2D(filters, kernel_size=1)(x)
        x = self.activation_block(x)

        return x

    def call(self, inputs):
        x = tf.keras.layers.Rescaling(scale=1.0 / 255)(inputs)

        # Extract patch embeddings.
        x = self.conv_stem(x, self.n_filters, self.patch_size)

        # ConvMixer blocks.
        for _ in range(self.depth):
            x = self.conv_mixer_block(x, self.n_filters, self.kernel_size)

        # Classification block.
        x = tf.keras.layers.GlobalAvgPool2D()(x)
        outputs = tf.keras.layers.Dense(self.n_classes)(x)

        return outputs

    def model(self):
        inputs = tf.keras.Input(
            (self.img_size, self.img_size, self.in_channels))
        return tf.keras.Model(inputs=inputs, outputs=self.call(inputs))
