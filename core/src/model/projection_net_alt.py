import tensorflow as tf


class ConvNet1D(tf.keras.Layer):
    pass


class ProjectionNet(tf.keras.Model):
    def __init__(
        self,
        n_classes: int,
        feature_vector_length: int = 150,
        projection_img_size: int = 224,
        n_feature_vectors: int = 5,
        n_projections: int = 3

    ):
        super(ProjectionNet, self).__init__()
        self.n_classes = n_classes
        self.feature_vector_length = feature_vector_length
        self.projection_img_size = projection_img_size
        self.n_feature_vectors = n_feature_vectors
        self.n_projections = n_projections

    def call(self, inputs):
        features = []
        for i in range(self.n_img_channels):
            features.append()
