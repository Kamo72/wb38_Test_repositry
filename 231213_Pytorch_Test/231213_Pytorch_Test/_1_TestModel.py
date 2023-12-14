from asyncio.windows_events import NULL
from os import read
from typing import Sequence
import torch
from torch import nn
from torch.utils.data import DataLoader, Dataset
from torchvision import datasets
from torchvision.transforms import ToTensor

def TestWhole():
    class SimpleModel(nn.Module):
        def __init__(self):
            super().__init__()
            self.layerList = nn.Sequential(
                    nn.Linear(1,  1),
                )
            self.loss_fn = nn.MSELoss()
            self.optimizer = torch.optim.SGD(self.parameters(), lr=1e-3) #lr = 0.001
            pass
        def forward(self, x) :
            x = torch.transpose(x, 0, -1)
            x = self.layerList(x)
            return x
    model  = SimpleModel();
    def train(dataloader, model, loss_fn, optimizer):
        # 학습에 사용할 CPU나 GPU, MPS 장치를 얻습니다.
        device = (
            "cuda"
            if torch.cuda.is_available()
            else "mps"
            if torch.backends.mps.is_available()
            else "cpu"
        )
        print(f"Using {device} device")
        model.to(device)
        
        #크기 포문
        size = len(dataloader.dataset)
        for batch, data in enumerate(dataloader):
            X = data["source"];
            y = data["label"];
            X, y = X.to(device), y.to(device)   
            # 예측 오류 계산
            pred = model(X)
            loss = loss_fn(pred, y)

            # 역전파
            optimizer.zero_grad()
            loss.backward()
            optimizer.step()

            if batch % 100 == 0:
                loss, current = loss.item(), (batch + 1) * len(X)
                print(f"loss: {loss:>7f}  [{current:>5d}/{size:>5d}]")  
    def test(dataloader, model, loss_fn):
        pass

    def TestTry(inputValue) :
        try :
            device = (
                "cuda"
                if torch.cuda.is_available()
                else "mps"
                if torch.backends.mps.is_available()
                else "cpu"
            )
            print(f"Using {device} device")            

            inputValue = float(inputValue)
            inputValue = torch.full((1,1), inputValue)
            while(inputValue.is_cpu) :
               inputValue.to(device)
               print(f"plz tensor, go to Fucking GPU!!!!")
            result = model(inputValue)
            print ("result : " + str(result.item()))
        except :
            print ("insert is not number!") 
    def TestTrain():
        # 데이터 셋 준비
        training_data = CustomDataset(list(range(-2000, 2000, 1)))

        # 데이터로더를 생성합니다.
        batch_size = 1;
        train_dataloader = DataLoader(training_data, batch_size=batch_size,shuffle=True)
        
        train(train_dataloader, model, model.loss_fn, model.optimizer)
        
        return
    def TestSave():
        if(model == NULL) : return "[Save Failure]"
        torch.save(model.state_dict(), 'model_weights.pth')
        return "[Save Succeed]"
    def TestLoad():
        try:
            model.load_state_dict(torch.load('model_weights.pth'))
            return "[Load Succeed]"
        except :
            return "[Load Failure]"
            
    def TestLoop():
        insert = ""        
        while(True) :
            print("Please insert number('/' to Exit, 's' to save, 'l' to load, 'm' to more learning)")
            insert = input("Input : ")
            match (insert) :
                case "/" : break
                case "s" : print(TestSave());
                case "l" : print(TestLoad());
                case "m" : TestTrain();
                case _ : TestTry(insert);
        pass
    
    
    TestLoop()
    


class CustomDataset(Dataset):
    def __init__(self, data):
        self.data = data

    def __len__(self):
        return len(self.data)

    def __getitem__(self, index):
        sample = self.data[index]
        input_data = torch.tensor(float(sample), dtype=torch.float32)
        label = torch.tensor(float(sample + 1), dtype=torch.float32)
        data = {"source": input_data, "label": label}
        return data
   

