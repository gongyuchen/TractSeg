import os, sys, inspect

parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe()))))
if not parent_dir in sys.path: sys.path.insert(0, parent_dir)

import glob
from os.path import join
from models.BaseModel import BaseModel
import numpy as np
import torch
import torch.nn as nn
import torch.nn.functional as F
import torch.optim as optim
from torch.autograd import Variable

from libs.PytorchUtils import PytorchUtils


def conv2d(in_channels, out_channels, kernel_size=3, stride=1, padding=1, bias=True, batchnorm=False):
    if batchnorm:
        layer = nn.Sequential(
            nn.Conv2d(in_channels, out_channels, kernel_size, stride=stride, padding=padding, bias=bias),
            nn.BatchNorm2d(out_channels),
            nn.ReLU())
    else:
        layer = nn.Sequential(
            nn.Conv2d(in_channels, out_channels, kernel_size, stride=stride, padding=padding, bias=bias),
            nn.ReLU())
    return layer


def deconv2d(in_channels, out_channels, kernel_size=3, stride=1, padding=0, output_padding=0, bias=True):
    layer = nn.Sequential(
        nn.ConvTranspose2d(in_channels, out_channels, kernel_size, stride=stride,
                           padding=padding, output_padding=output_padding, bias=bias),
        nn.ReLU())
    return layer


class UNet(torch.nn.Module):
    def __init__(self, n_input_channels=3, n_classes=7, n_filt=64):
        super(UNet, self).__init__()
        self.in_channel = n_input_channels
        self.n_classes = n_classes

        # todo:
        # - besser ohne Bias?
        # - besser mit Conv statt MaxPooling?
        # - Add Dropout

        self.contr_1_1 = conv2d(n_input_channels, n_filt, bias=True)
        self.contr_1_2 = conv2d(n_filt, n_filt, bias=True)
        self.pool_1 = nn.MaxPool2d((2, 2))

        self.contr_2_1 = conv2d(n_filt, n_filt * 2, bias=True)
        self.contr_2_2 = conv2d(n_filt * 2, n_filt * 2, bias=True)
        self.pool_2 = nn.MaxPool2d((2, 2))

        self.contr_3_1 = conv2d(n_filt * 2, n_filt * 4, bias=True)
        self.contr_3_2 = conv2d(n_filt * 4, n_filt * 4, bias=True)
        self.pool_3 = nn.MaxPool2d((2, 2))

        self.contr_4_1 = conv2d(n_filt * 4, n_filt * 8, bias=True)
        self.contr_4_2 = conv2d(n_filt * 8, n_filt * 8, bias=True)
        self.pool_4 = nn.MaxPool2d((2, 2))

        self.dropout = nn.Dropout(p=0.4)

        self.encode_1 = conv2d(n_filt * 8, n_filt * 16, bias=True)
        self.encode_2 = conv2d(n_filt * 16, n_filt * 16, bias=True)
        self.deconv_1 = deconv2d(n_filt * 16, n_filt * 16, kernel_size=2, stride=2, bias=True)
        # nn.Upsample(scale_factor=(2, 2, 1))

        self.expand_1_1 = conv2d(n_filt * 8 + n_filt * 16, n_filt * 8, bias=True)
        self.expand_1_2 = conv2d(n_filt * 8, n_filt * 8, bias=True)
        self.deconv_2 = deconv2d(n_filt * 8, n_filt * 8, kernel_size=2, stride=2, bias=True)

        self.expand_2_1 = conv2d(n_filt * 4 + n_filt * 8, n_filt * 4, stride=1, bias=True)
        self.expand_2_2 = conv2d(n_filt * 4, n_filt * 4, stride=1, bias=True)
        self.deconv_3 = deconv2d(n_filt * 4, n_filt * 4, kernel_size=2, stride=2, bias=True)

        self.expand_3_1 = conv2d(n_filt * 2 + n_filt * 4, n_filt * 2, stride=1, bias=True)
        self.expand_3_2 = conv2d(n_filt * 2, n_filt * 2, stride=1, bias=True)
        self.deconv_4 = deconv2d(n_filt * 2, n_filt * 2, kernel_size=2, stride=2, bias=True)

        self.expand_4_1 = conv2d(n_filt + n_filt * 2, n_filt, stride=1, bias=True)
        self.expand_4_2 = conv2d(n_filt, n_filt, stride=1, bias=True)

        self.conv_5 = nn.Conv2d(n_filt, n_classes, kernel_size=1, stride=1, padding=0,
                                bias=True)  # no activation function, because is in LossFunction (...WithLogits)

    def forward(self, inpt):
        contr_1_1 = self.contr_1_1(inpt)
        contr_1_2 = self.contr_1_2(contr_1_1)
        pool_1 = self.pool_1(contr_1_2)

        contr_2_1 = self.contr_2_1(pool_1)
        contr_2_2 = self.contr_2_2(contr_2_1)
        pool_2 = self.pool_2(contr_2_2)

        contr_3_1 = self.contr_3_1(pool_2)
        contr_3_2 = self.contr_3_2(contr_3_1)
        pool_3 = self.pool_3(contr_3_2)

        contr_4_1 = self.contr_4_1(pool_3)
        contr_4_2 = self.contr_4_2(contr_4_1)
        pool_4 = self.pool_4(contr_4_2)

        dropout = self.dropout(pool_4)

        encode_1 = self.encode_1(dropout)
        encode_2 = self.encode_2(encode_1)
        deconv_1 = self.deconv_1(encode_2)

        concat1 = torch.cat([deconv_1, contr_4_2], 1)
        expand_1_1 = self.expand_1_1(concat1)
        expand_1_2 = self.expand_1_2(expand_1_1)
        deconv_2 = self.deconv_2(expand_1_2)

        concat2 = torch.cat([deconv_2, contr_3_2], 1)
        expand_2_1 = self.expand_2_1(concat2)
        expand_2_2 = self.expand_2_2(expand_2_1)
        deconv_3 = self.deconv_3(expand_2_2)

        concat3 = torch.cat([deconv_3, contr_2_2], 1)
        expand_3_1 = self.expand_3_1(concat3)
        expand_3_2 = self.expand_3_2(expand_3_1)
        deconv_4 = self.deconv_4(expand_3_2)

        concat4 = torch.cat([deconv_4, contr_1_2], 1)
        expand_4_1 = self.expand_4_1(concat4)
        expand_4_2 = self.expand_4_2(expand_4_1)

        conv_5 = self.conv_5(expand_4_2)
        return conv_5


class UNet_Pytorch(BaseModel):
    def create_network(self):

        def train(X, y):
            X = torch.from_numpy(X.astype(np.float32))
            y = torch.from_numpy(y.astype(np.float32))
            X, y = Variable(X.cuda()), Variable(y.cuda())  # X: (bs, features, x, y)   y: (bs, classes, x, y)
            optimizer.zero_grad()
            net.train()
            outputs = net(X)  # forward     # outputs: (bs, classes, x, y)
            loss = criterion(outputs, y)
            loss.backward()  # backward
            optimizer.step()  # optimise
            f1 = PytorchUtils.f1_score_macro(y.data, outputs.data)
            return loss.data[0], outputs, f1

        def test(X, y):
            X = torch.from_numpy(X.astype(np.float32))
            y = torch.from_numpy(y.astype(np.float32))
            X, y = Variable(X.cuda(), volatile=True), Variable(y.cuda(), volatile=True)
            net.train(False)
            outputs = net(X)  # forward
            loss = criterion(outputs, y)
            f1 = PytorchUtils.f1_score_macro(y.data, outputs.data)
            return loss.data[0], outputs, f1

        def predict(X):
            X = torch.from_numpy(X.astype(np.float32), volatile=True)
            X = Variable(X.cuda())
            net.train(False)
            outputs = net(X)  # forward
            return outputs

        def save_model(metrics, epoch_nr):
            max_f1_idx = np.argmax(metrics["f1_macro_validate"])
            max_f1 = np.max(metrics["f1_macro_validate"])
            if epoch_nr == max_f1_idx and max_f1 > 0.01:  # saving to network drives takes 5s (to local only 0.5s) -> do not save so often
                print("  Saving weights...")
                for fl in glob.glob(join(self.HP.EXP_PATH, "best_weights_ep*")):  # remove weights from previous epochs
                    os.remove(fl)
                try:
                    #Actually is a pkl not a npz
                    PytorchUtils.save_checkpoint(join(self.HP.EXP_PATH, "best_weights_ep" + str(epoch_nr) + ".npz"), unet=net)
                except IOError:
                    print("\nERROR: Could not save weights because of IO Error\n")
                self.HP.BEST_EPOCH = epoch_nr

        def load_model(path):
            PytorchUtils.load_checkpoint(path, unet=net)


        if self.HP.SEG_INPUT == "Peaks" and self.HP.TYPE == "single_direction":
            NR_OF_GRADIENTS = 9
        elif self.HP.SEG_INPUT == "Peaks" and self.HP.TYPE == "combined":
            NR_OF_GRADIENTS = 3*self.HP.NR_OF_CLASSES
        else:
            NR_OF_GRADIENTS = 33

        net = UNet(n_input_channels=NR_OF_GRADIENTS, n_classes=self.HP.NR_OF_CLASSES, n_filt=self.HP.UNET_NR_FILT).cuda()
        criterion = nn.BCEWithLogitsLoss()  # todo: use BCEWithLogitsLoss and remove sigmoid further up
        optimizer = optim.Adamax(net.parameters(), lr=self.HP.LEARNING_RATE)

        if self.HP.LOAD_WEIGHTS:
            print("Loading weights ... ({})".format(join(self.HP.EXP_PATH, self.HP.WEIGHTS_PATH)))
            load_model(join(self.HP.EXP_PATH, self.HP.WEIGHTS_PATH))

        self.train = train
        self.predict = test
        self.get_probs = predict
        self.get_probs_flat = -1
        self.save_model = save_model
        self.load_model = load_model