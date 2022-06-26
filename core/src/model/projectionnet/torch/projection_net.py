import torch
import torch.nn as nn

from components import ConvNet1D, ConvNet2D


class ProjectionNet(nn.Module):
    def __init__(
        self,
        n_classes: int,
        n_feature_vectors: int,
        n_projections: int
    ):
        super(ProjectionNet, self).__init__()
        self.n_classes = n_classes
        self.n_feature_vectors = n_feature_vectors
        self.n_projections = n_projections

        self.features = nn.ModuleList()

        for i in range(self.n_feature_vectors):
            self.features.append(ConvNet1D())

        for i in range(self.n_projections):
            self.features.append(ConvNet2D())

        feature_size = 1280 * n_projections + 32 * n_feature_vectors

        self.mlp1 = nn.Linear(in_features=feature_size, out_features=128)
        self.mlp2 = nn.Linear(in_features=128, out_features=n_classes)

        self.dropout1 = nn.Dropout(0.5)
        self.dropout2 = nn.Dropout(0.5)

    def forward(self, inputs):
        features = []
        for i, feature in enumerate(self.features):
            features.append(feature(inputs[i]))

        x = torch.cat(features, dim=1)

        x = self.dropout1(x)
        x = self.mlp1(x)
        x = self.dropout2(x)

        return self.mlp2(x)
