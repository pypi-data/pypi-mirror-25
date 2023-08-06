from collections import defaultdict

import numpy as np
import torch
from torch.autograd import Variable
from torch.utils.data import DataLoader

from torchtricks.metrics import categorical_accuracy
from torchtricks.utils import AverageMeter


class Trainer:

    def __init__(self, model):
        self.model = model
        self.optimizer = None
        self.criterion = None
        self.history = defaultdict(list)
        self.cuda = False
        self.callbacks = []

    def compile(self, optimizer, criterion):
        self.optimizer = optimizer
        self.criterion = criterion

    def fit_epoch(self, loader):
        self.model.train()
        running_loss = AverageMeter()
        running_accuracy = AverageMeter()
        for data, target in loader:
            if self.cuda:
                data, target = Variable(data.cuda()), Variable(target.cuda().squeeze())
            else:
                data, target = Variable(data), Variable(target)
            output = self.model(data)
            loss = self.criterion(output, target)
            accuracy = categorical_accuracy(target.data, output.data)
            running_loss.update(loss.data[0])
            running_accuracy.update(accuracy)
            self.optimizer.zero_grad()
            loss.backward()
            self.optimizer.step()
        return running_loss.avg, running_accuracy.avg

    def validate(self, loader):
        self.model.eval()
        val_loss = AverageMeter()
        val_accuracy = AverageMeter()
        for data, target in loader:
            if self.cuda:
                data, target = Variable(data.cuda()), Variable(target.cuda())
            else:
                data, target = Variable(data), Variable(target)
            output = self.model(data)
            loss = self.criterion(output, target)
            accuracy = categorical_accuracy(target.data, output.data)
            val_loss.update(loss.data[0])
            val_accuracy.update(accuracy)
        return val_loss.avg, val_accuracy.avg

    def fit(self, train_dataset, batch_size=32, shuffle=True,
            nb_epoch=1, validation_dataset=None, cuda=True, num_workers=0, callbacks=[]):
        if cuda:
            self.cuda = cuda
            self.model.cuda()
        if validation_dataset:
            print('Train on {} samples, Validate on {} samples'.format(len(train_dataset),
                                                                       len(validation_dataset)))
        else:
            print('Train on {} samples'.format(len(train_dataset)))

        train_loader = DataLoader(train_dataset, batch_size, shuffle,
                                  pin_memory=True, num_workers=num_workers)
        for epoch in range(nb_epoch):
            loss, accuracy = self.fit_epoch(train_loader)
            self.history['loss'].append(loss)
            self.history['accuracy'].append(accuracy)
            if validation_dataset:
                validation_loader = DataLoader(validation_dataset, batch_size, shuffle,
                                    pin_memory=True, num_workers=num_workers)
                val_loss, val_accuracy = self.validate(validation_loader)
                print("[Epoch {} - loss: {:.4f} - acc: {:.4f} - val_loss: {:.4f} - val_acc: {:.4f}]".format(epoch + 1,
                                                                                                            loss,
                                                                                                            accuracy,
                                                                                                            val_loss,
                                                                                                            val_accuracy))
                self.history['val_loss'].append(val_loss)
                self.history['val_accuracy'].append(val_accuracy)
            else:
                print("[loss: {:.4f} - acc: {:.4f}]".format(loss, accuracy))

    def predict(self, dataset, batch_size, cuda=True):
        self.model.eval()
        self.model.cuda(cuda)
        predictions = []
        loader = DataLoader(dataset, batch_size, shuffle=False)
        for data, _ in loader:
            if cuda:
                data = Variable(data.cuda())
            else:
                data = Variable(data)
            output = self.model(data).data
            for prediction in output:
                predictions.append(prediction.cpu().numpy())
        return np.array(predictions)

    def predict_labels(self, dataset, batch_size, cuda=True):
        self.model.eval()
        self.model.cuda(cuda)
        labels = []
        loader = DataLoader(dataset, batch_size, shuffle=False)
        for data, _ in loader:
            if cuda:
                data = Variable(data.cuda())
            else:
                data = Variable(data)
            data = Variable(data.cuda())
            _, output = torch.max(self.model(data).data, dim=-1)
            for label in output:
                labels.append(label.cpu().numpy())
        return np.array(labels)

    def generate_predictions(self, dataset, batch_size, cuda=True):
        self.model.eval()
        self.model.cuda(cuda)
        loader = DataLoader(dataset, batch_size, shuffle=False)
        for data, _ in loader:
            if cuda:
                data = Variable(data.cuda())
            else:
                data = Variable(data)
            output = self.model(data).data
            for prediction in output:
                yield prediction.cpu().numpy()
