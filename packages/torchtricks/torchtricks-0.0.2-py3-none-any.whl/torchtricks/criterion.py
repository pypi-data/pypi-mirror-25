import torch
import torch.nn.functional as F
from torch import nn

from torchtricks.utils import imagenet_preprocess, gram_matrix


class PerceptualLoss(nn.Module):
    def __init__(self, loss_network, content_weight=1, style_weight=2e5):
        super(PerceptualLoss, self).__init__()
        self.loss_network = loss_network
        self.content_weight = content_weight
        self.style_weight = style_weight
        self.style_criterion = StyleLoss(loss_network)
        self.content_criterion = ContentLoss(loss_network)

    def forward(self, output, original_img, style_image):
        content_loss = self.content_criterion(output, original_img) * self.content_weight
        style_loss = self.style_criterion(output, style_image) * self.style_weight
        return style_loss, content_loss


class StyleLoss(nn.Module):
    """
    Must be initialized with a "loss network"
    Example use  VGG relu2_2 as loss network:
    vgg = vgg16(pretrained=True)
    relu2_2 = nn.Sequential(*list(vgg.features)[:9])
    for param in relu2_2.parameters():
        param.requires_grad = False
    relu2_2.eval
    relu2_2.cuda()
    """

    def __init__(self, loss_network):
        super(StyleLoss, self).__init__()
        self.loss_network = loss_network

    def forward(self, output, style):
        loss = 0
        output = imagenet_preprocess(output)
        style = imagenet_preprocess(style)
        features_output = self.loss_network(output)
        features_style = self.loss_network(style)
        for layer in features_output.keys():
            loss += F.mse_loss(gram_matrix(features_output[layer]),
                               gram_matrix(features_style[layer]))
        return loss


class ContentLoss(nn.Module):
    """
    Must be initialized with a "loss network"
    Example use  VGG relu2_2 as loss network:
    vgg = vgg16(pretrained=True)
    relu2_2 = nn.Sequential(*list(vgg.features)[:9])
    for param in relu2_2.parameters():
        param.requires_grad = False
    relu2_2.eval
    relu2_2.cuda()
    """

    def __init__(self, loss_network):
        super(ContentLoss, self).__init__()
        self.loss_network = loss_network

    def forward(self, input, target):
        input = imagenet_preprocess(input)
        target = imagenet_preprocess(target)
        features_input = self.loss_network(input)
        features_target = self.loss_network(target)
        return F.mse_loss(features_input['relu3_3'],
                          features_target['relu3_3'])


class RelativeDepthLoss(nn.Module):
    def __init__(self):
        super(RelativeDepthLoss, self).__init__()

    def ranking_loss(self, z_A, z_B, target):
        """
        loss for a given set of pixels:
        z_A: predicted absolute depth for pixels A
        z_B: predicted absolute depth for pixels B
        ground_truth: Relative depth between A and B (-1, 0, 1)
        """
        mask = torch.abs(target)
        predicted_depth = z_A - z_B
        log_loss = torch.log(1 + torch.exp((predicted_depth * target) * -1)) * mask
        squared_loss = (predicted_depth ** 2) * (1 - mask)  # if pred depth is not zero adds to loss
        return sum(log_loss + squared_loss)

    def forward(self, output, target):
        total_loss = 0
        for index in range(len(output)):
            # double check index, double check data loader
            x_A = target['x_A'][index].long()
            y_A = target['y_A'][index].long()
            x_B = target['x_B'][index].long()
            y_B = target['y_B'][index].long()

            z_A = output[index][0][x_A, y_A]  # all "A" points
            z_B = output[index][0][x_B, y_B]  # all "B" points

            total_loss += self.ranking_loss(z_A, z_B, target['ordinal_relation'][index])

        return total_loss / len(output)
