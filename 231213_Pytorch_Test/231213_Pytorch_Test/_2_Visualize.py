from torch.utils.data import Dataset, DataLoader
import torchvision.transforms as transforms
from torchvision import datasets
import matplotlib.pyplot as plt
import torch
import torch.nn as nn
import torch.nn.functional as F


def TestSamplesDisplay ():
	mnist_transform = transforms.Compose(
		[transforms.ToTensor(),
		 transforms.Normalize(mean=(0.5,), std=(1.0, ))
	])

	trainset = datasets.MNIST(root = '/content/',
														train = True,
														download = True,
														transform=mnist_transform)

	train_dataloader = DataLoader(trainset , batch_size=8, shuffle = True, num_workers = 2)

	# iterable(��ȸ ������ ��ü)�� ��ȯ���ִ� �۾�
	dataiter = iter(train_dataloader)
	images, labels = next(dataiter)

	print(images.shape) 
	# [��ġ ������, 1, 28, 28] 

	print(labels.shape)
	# [��ġ ������]

	torch_image = torch.squeeze(images[0])
	#[28, 28]



	figure = plt.figure(figsize = (12, 6))
	cols, rows = 4, 2
	for i in range(1, cols * rows + 1) :
		sample_idx = torch.randint(len(trainset), size=(1,)).item()
		img, label = trainset[sample_idx]
		figure.add_subplot(rows, cols, i)
		plt.title(label)
		plt.axis('off')
		plt.imshow(img.squeeze(), cmap = 'gray')
	plt.show()
	print("succeed")

def TestConv2dDisplay() :
	mnist_transform = transforms.Compose(
		[transforms.ToTensor(),
		 transforms.Normalize(mean=(0.5,), std=(1.0, ))
	])

	trainset = datasets.MNIST(root = '/content/',
														train = True,
														download = True,
														transform=mnist_transform)

	train_dataloader = DataLoader(trainset , batch_size=8, shuffle = True, num_workers = 2)

	# iterable(��ȸ ������ ��ü)�� ��ȯ���ִ� �۾�
	dataiter = iter(train_dataloader)
	images, labels = next(dataiter)

	print(images.shape) 
	# [��ġ ������, 1, 28, 28] 

	print(labels.shape)
	# [��ġ ������]

	torch_image = torch.squeeze(images[0])
	#[28, 28]


	layer = nn.Conv2d(in_channels = 1, out_channels = 20, kernel_size=5, stride=1)
	weight = layer.weight.detach().numpy()


	print(images.shape) # 8 1 28 28
	print(images[0].size()) # 1 28 28

	input_image = torch.squeeze(images[0])
	print(input_image.size()) # 28 28


	input_data = torch.unsqueeze(images[0], dim = 0)
	print(input_data.size()) # 1 1 28 28

	output_data = layer(input_data)
	output_arr = output_data.detach().numpy()
	print(output_arr.shape)  # 1 20 28 28


	plt.figure(figsize = (15,30))

	plt.subplot(131)
	plt.title("input")
	plt.imshow(input_image, 'gray')

	plt.subplot(132)
	plt.title("weight")
	plt.imshow(weight[0,0,:, :], 'gray')

	plt.subplot(133)
	plt.title("output")
	plt.imshow(output_arr[0,0,:,:], 'gray')
	
	plt.show()
	
def TestMaxPool2dDisplay() :
	mnist_transform = transforms.Compose(
		[transforms.ToTensor(),
		 transforms.Normalize(mean=(0.5,), std=(1.0, ))
	])
	trainset = datasets.MNIST(root = '/content/',
														train = True,
														download = True,
														transform=mnist_transform)
	train_dataloader = DataLoader(trainset , batch_size=8, shuffle = True, num_workers = 2)

	# iterable(��ȸ ������ ��ü)�� ��ȯ���ִ� �۾�
	dataiter = iter(train_dataloader)
	images, labels = next(dataiter)
	print(images.shape) 
	# [��ġ ������, 1, 28, 28] 
	print(labels.shape)
	# [��ġ ������]
	torch_image = torch.squeeze(images[0])
	#[28, 28]

	input_image = torch.squeeze(images[0])

	input_data = torch.unsqueeze(images[0], dim = 0)
	print(input_data.size()) # 1 1 28 28

	
	pool = F.max_pool2d(images, 2, 2)
	# 2���� �������� max���� ��������...? �� ���Ҹ�
	# �ϴ� 2�� �����ٴ� ���...?
	print(pool.shape) # [1, 20, 2, 2]

	pool_arr = pool.numpy()
	# weight����ġ�� ���� ������ �ٷ� numpy()��ȯ ����
	print(pool_arr.shape) # [1, 20, 2, 2]


	plt.figure(figsize = (10,15))

	plt.subplot(121)
	plt.title("input")
	plt.imshow(input_image, 'gray')

	plt.subplot(122)
	plt.title("output")
	plt.imshow(pool_arr[0,0,:,:], 'gray')
	
	plt.show()
	
