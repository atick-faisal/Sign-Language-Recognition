from numpy import outer
from tensorflow.keras import layers, models


class ProjectionNet():
    def __init__(
        self,
        img_size: int,
        segment_len: int,
        n_classes: int,
        base_model: models.Model
    ):
        self.img_size = img_size
        self.segment_len = segment_len
        self.base_model = base_model
        self.base_model.trainable = False

        self.dropout = layers.Dropout(0.5)

        self.mlp1 = layers.Dense(
            units=128,
            activation="relu"
        )

        self.mlp2 = layers.Dense(
            units=n_classes,
            activation="softmax"
        )

    def conv_block_1d(self):
        inputs = layers.Input(shape=(self.segment_len, 1))
        x = layers.BatchNormalization()(inputs)
        x = layers.Conv1D(8, 3, activation="selu")(x)
        x = layers.Conv1D(8, 3, activation="selu")(x)
        x = layers.MaxPool1D(2)(x)
        x = layers.Conv1D(16, 3, activation="selu")(x)
        x = layers.Conv1D(16, 3, activation="selu")(x)
        x = layers.MaxPool1D(2)(x)
        x = layers.Flatten()(x)
        output = layers.Dense(32)(x)

        return inputs, output

    def conv_block_2d(self):
        preprocess = layers.experimental.preprocessing.Rescaling(
            scale=1.0/127.5,
            offset=-1
        )
        inputs = layers.Input(shape=(self.img_size, self.img_size, 3))
        x = preprocess(inputs)
        x = self.base_model(x, training=False)
        output = layers.GlobalAveragePooling2D()(x)

        # inputs = layers.Input(shape=(self.img_size, self.img_size, 3))
        # x = layers.Conv2D(16, (3, 3), activation="relu")(inputs)
        # x = layers.MaxPool2D((2, 2))(x)
        # x = layers.Conv2D(16, (3, 3), activation="relu")(inputs)
        # x = layers.MaxPool2D((2, 2))(x)
        # x = layers.Conv2D(32, (3, 3), activation="relu")(inputs)
        # x = layers.MaxPool2D((2, 2))(x)
        # x = layers.Conv2D(32, (3, 3), activation="relu")(inputs)
        # x = layers.MaxPool2D((2, 2))(x)
        # x = layers.Dropout(0.2)(x)
        # x = layers.Flatten()(x)
        # output = layers.Dense(128, activation="relu")(x)

        return inputs, output

    def get_model(
        self,
        n_projections: int = 3,
        n_channels: int = 5
    ):

        inputs = []
        features = []

        for _ in range(n_channels):
            input_1d, features_1d = self.conv_block_1d()
            inputs.append(input_1d)
            features.append(features_1d)

        for _ in range(n_projections):
            input_2d, features_2d = self.conv_block_2d()
            inputs.append(input_2d)
            features.append(features_2d)

        x = layers.concatenate(features, axis=-1)
        x = self.dropout(x)
        x = self.mlp1(x)
        x = self.dropout(x)
        output = self.mlp2(x)

        return models.Model(inputs, output)
