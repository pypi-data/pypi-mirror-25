import torch


def binary_accuracy(y_true, y_pred):
    y_pred = y_pred.float()
    y_true = y_true.float()
    return (y_true == torch.round(y_pred)).float().mean()


def categorical_accuracy(y_true, y_pred):
    y_true = y_true.float()
    _, y_pred = torch.max(y_pred, dim=-1)
    return (y_pred.float() == y_true).float().mean()
