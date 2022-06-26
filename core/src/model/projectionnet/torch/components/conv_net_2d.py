import torch.nn as nn
from torchvision.models import mobilenet_v2


class ConvNet2D(nn.Module):
    def __init__(
        self,
        base_model: nn.Module = mobilenet_v2(pretrained=True)
    ):
        super(ConvNet2D, self).__init__()
        base_model.eval()
        self.features = base_model.features
        self.global_pool = nn.AvgPool2d(kernel_size=(7, 7))
        self.flatten = nn.Flatten()

    def forward(self, x):
        x = self.features(x)
        x = self.global_pool(x)

        return self.flatten(x)
