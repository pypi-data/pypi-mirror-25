from torch import nn
from torchvision.models import vgg16


class LossNetwork(nn.Module):
    def __init__(self):
        super(LossNetwork, self).__init__()
        vgg = vgg16(pretrained=True)
        features = list(vgg.features)
        self.relu1_2 = nn.Sequential(*features[:4])
        self.relu2_2 = nn.Sequential(*features[4:9])
        self.relu3_3 = nn.Sequential(*features[9:16])
        self.relu4_3 = nn.Sequential(*features[16:23])

    def forward(self, x):
        relu1_2 = self.relu1_2(x)
        relu2_2 = self.relu2_2(relu1_2)
        relu3_3 = self.relu3_3(relu2_2)
        relu4_3 = self.relu4_3(relu3_3)
        return dict(relu1_2=relu1_2,
                    relu2_2=relu2_2,
                    relu3_3=relu3_3,
                    relu4_3=relu4_3)
