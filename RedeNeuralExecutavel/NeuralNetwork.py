import torch
import torch.nn as nn
import numpy as np
import sys

class MyCNN(nn.Module):
    def __init__(self):
        super().__init__()
        self.conv1 = nn.Conv2d(1,3,3,padding=1)
        self.pool = nn.MaxPool2d(2,2)
        self.conv2 = nn.Conv2d(3,9,3)
        self.fc1 = nn.Linear(9*6*6,25)
        self.fc2 = nn.Linear(25,25)
        self.fc3 = nn.Linear(25,6)
        self.R = nn.ReLU()
    def forward(self,x):
        x = self.pool(self.R(self.conv1(x)))
        x = self.pool(self.R(self.conv2(x)))
        x = x.view(-1,9*6*6)
        x = self.R(self.fc1(x))
        x = self.R(self.fc2(x))
        x = self.fc3(x)
        return x.squeeze()

def main():
    args = sys.argv

    image = args[1]
    print(image)

    # NeuralNetwork = MyCNN()
    # NeuralNetwork.load_state_dict(torch.load('CNN6.pth'))

    # with torch.no_grad():
    #     SoftMax = nn.Softmax(dim=0)
    #     prediction = NeuralNetwork((torch.from_numpy(np.asarray(image))/255).view(1,28,28))
    #     prediction_answer = prediction.argmax()
    #     prediction_prob = SoftMax(prediction)

    #     prediction_value = prediction[prediction_answer]

    #     print(prediction_answer,prediction_value)
    #     return prediction_answer,prediction_value

if __name__ == "__main__":
    main()