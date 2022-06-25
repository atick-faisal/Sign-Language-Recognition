import tensorflow as tf
from .layers import ConvNet1D, ConvNet2D


class ProjectionNet(tf.keras.Model):
    def __init__(
        self,
        n_classes: int,
        base_model: tf.keras.Model,
        feature_vector_shape: tuple = (150, 1),
        projection_img_shape: tuple = (160, 160, 3),
        n_feature_vectors: int = 5,
        n_projections: int = 3
    ):
        super(ProjectionNet, self).__init__()
        self.n_classes = n_classes
        self.base_model = base_model
        self.feature_vector_shape = feature_vector_shape
        self.projection_img_shape = projection_img_shape
        self.n_feature_vectors = n_feature_vectors
        self.n_projections = n_projections

        self.base_model.trainable = False
        self.dropout = tf.keras.layers.Dropout(0.5)

        self.conv_net_layers = []

        for _ in range(self.n_feature_vectors):
            self.conv_net_layers.append(
                ConvNet1D(
                    n_filters=8,
                    n_layers=4,
                    kernel_size=3,
                    pool_size=2,
                    feature_size=32
                )
            )

        for _ in range(self.n_projections):
            self.conv_net_layers.append(
                ConvNet2D(
                    base_model=self.base_model
                )
            )

        self.mlp1 = tf.keras.layers.Dense(
            units=128,
            activation="relu"
        )

        self.mlp2 = tf.keras.layers.Dense(
            units=n_classes,
            activation="softmax"
        )

    def call(self, inputs, training=None):
        features = []
        for i in range(len(inputs)):
            features.append(
                self.conv_net_layers[i](inputs[i])
            )

        x = tf.keras.layers.concatenate(features, axis=-1)
        x = self.dropout(x)

        # if training:
        #     x = self.dropout(x)

        # x = self.mlp1(x)

        # if training:
        #     x = self.dropout(x)

        x = self.dropout(x)
        output = self.mlp2(x)

        return output

    def model(self) -> tf.keras.Model:
        inputs = []
        for _ in range(self.n_feature_vectors):
            inputs.append(tf.keras.layers.Input(
                shape=self.feature_vector_shape))

        for _ in range(self.n_projections):
            inputs.append(tf.keras.layers.Input(
                shape=self.projection_img_shape))

        return tf.keras.Model(inputs=inputs, outputs=self.call(inputs))
