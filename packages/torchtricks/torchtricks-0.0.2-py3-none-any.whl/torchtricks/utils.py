from shutil import copyfile
from torch.autograd import Variable
import numpy as np
import torch


def imagenet_preprocess(batch):
    tensortype = type(batch.data)
    mean = tensortype(batch.data.size())
    std = tensortype(batch.data.size())

    mean[:, 0, :, :] = 0.485
    mean[:, 1, :, :] = 0.456
    mean[:, 2, :, :] = 0.406

    std[:, 0, :, :] = 0.229
    std[:, 1, :, :] = 0.224
    std[:, 2, :, :] = 0.225

    return (batch - Variable(mean)) / Variable(std)


def gram_matrix(img):
    (b, ch, h, w) = img.size()
    features = img.view(b, ch, w * h)
    features_t = features.transpose(1, 2)
    return features @ features_t / (ch * h * w)


class AverageMeter(object):
    """Computes and stores the average and current value"""

    def __init__(self):
        self.reset()

    def reset(self):
        self.val = 0
        self.avg = 0
        self.sum = 0
        self.count = 0

    def update(self, val, n=1):
        self.val = val
        self.sum += val * n
        self.count += n
        self.avg = self.sum / self.count


def save_checkpoint(model_state, optimizer_state, filename, epoch=None, is_best=False):
    state = dict(model_state=model_state,
                 optimizer_state=optimizer_state,
                 epoch=epoch)
    torch.save(state, filename)
    if is_best:
        copyfile(filename, 'model_best.pth.tar')


def clip_softmax(arr, mx):
    clipped = np.clip(arr, (1 - mx) / 1, mx)
    return clipped / clipped.sum(axis=1)[:, np.newaxis]


def recover_image(img):
    img *= np.array([0.229, 0.224, 0.225]).reshape(1, 3, 1, 1)
    img += np.array([0.229, 0.224, 0.225]).reshape(1, 3, 1, 1)
    img *= 225.
    return img.clip(0, 255).astype(np.uint8)


def anneal_lr(optimizer, decay):
    for param_group in optimizer.param_groups:
        param_group['lr'] /= decay
