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

	# iterable(순회 가능한 객체)로 변환해주는 작업
	dataiter = iter(train_dataloader)
	images, labels = next(dataiter)

	print(images.shape) 
	# [배치 사이즈, 1, 28, 28] 

	print(labels.shape)
	# [배치 사이즈]

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

	# iterable(순회 가능한 객체)로 변환해주는 작업
	dataiter = iter(train_dataloader)
	images, labels = next(dataiter)

	print(images.shape) 
	# [배치 사이즈, 1, 28, 28] 

	print(labels.shape)
	# [배치 사이즈]

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

	# iterable(순회 가능한 객체)로 변환해주는 작업
	dataiter = iter(train_dataloader)
	images, labels = next(dataiter)
	print(images.shape) 
	# [배치 사이즈, 1, 28, 28] 
	print(labels.shape)
	# [배치 사이즈]
	torch_image = torch.squeeze(images[0])
	#[28, 28]

	input_image = torch.squeeze(images[0])

	input_data = torch.unsqueeze(images[0], dim = 0)
	print(input_data.size()) # 1 1 28 28

	
	pool = F.max_pool2d(images, 2, 2)
	# 2개를 기준으로 max값만 저장해줘...? 뭔 개소리
	# 일단 2로 나눈다는 얘기...?
	print(pool.shape) # [1, 20, 2, 2]

	pool_arr = pool.numpy()
	# weight가중치가 없기 떄문에 바로 numpy()변환 가능
	print(pool_arr.shape) # [1, 20, 2, 2]


	plt.figure(figsize = (10,15))

	plt.subplot(121)
	plt.title("input")
	plt.imshow(input_image, 'gray')

	plt.subplot(122)
	plt.title("output")
	plt.imshow(pool_arr[0,0,:,:], 'gray')
	
	plt.show()
	
