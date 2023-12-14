from torch.utils.data import Dataset, DataLoader
import torchvision.transforms as transforms
from torchvision import datasets
import torch
import torch.nn as nn
import torch.nn.functional as F


def TestModelView() :
    model = MyModel();
    print(list(model.children()))
    
    print(list(model.modules()))


class MyModel(nn.Module) :
	def __init__(self) :
		super(MyModel, self).__init__()
		self.layer1 = nn.Sequential(
			nn.Conv2d(3, 64, 5),
			nn.ReLU(True),
			nn.MaxPool2d(2),
		)
		self.layer2 = nn.Sequential(
			nn.Conv2d(64, 30, 5),
			nn.ReLU(True),
			nn.MaxPool2d(2),
		)
		self.layer3 = nn.Sequential(
			nn.Linear(30 * 5 * 5, 10, True),
			nn.ReLU(True)
		)
	def forwar(self, x) :
		x = self.layer1(x)
		x = self.layer2(x)
		x = x.view(x.shape[0], -1)
		x = self.layer3(x)
		return x