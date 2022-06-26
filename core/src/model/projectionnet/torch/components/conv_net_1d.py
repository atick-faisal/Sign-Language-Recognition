import torch.nn as nn


class ConvNet1D(nn.Module):
    def __init__(self):
        super(ConvNet1D, self).__init__()

        self.features = nn.Sequential(
            nn.Conv1d(in_channels=1, out_channels=8, kernel_size=3),
            nn.BatchNorm1d(8),
            nn.SELU(),
            nn.Conv1d(in_channels=8, out_channels=8, kernel_size=3),
            nn.BatchNorm1d(8),
            nn.SELU(),
            nn.MaxPool1d(kernel_size=2),
            nn.Conv1d(in_channels=8, out_channels=16, kernel_size=3),
            nn.BatchNorm1d(16),
            nn.SELU(),
            nn.Conv1d(in_channels=16, out_channels=16, kernel_size=3),
            nn.BatchNorm1d(16),
            nn.SELU(),
            nn.MaxPool1d(kernel_size=2),
            nn.Flatten(),
            nn.Linear(in_features=34 * 16, out_features=32)
        )

    def forward(self, x):
        return self.features(x)
