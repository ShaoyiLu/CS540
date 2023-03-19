import numpy as np
import torch
import torch.nn as nn
import torch.nn.functional as F
import torch.optim as optim
from torchvision import datasets, transforms


# Feel free to import other packages, if needed.
# As long as they are supported by CSL machines.


def get_data_loader(training=True):
    custom_transform = transforms.Compose([
        transforms.ToTensor(),
        transforms.Normalize((0.1307,), (0.3081,))
    ])

    if training:
        data_set = datasets.FashionMNIST('./data', train = True, download = True, transform = custom_transform)
    else:
        data_set = datasets.FashionMNIST('./ data', train = False, download=True, transform = custom_transform)

    test_loader = torch.utils.data.DataLoader(data_set, batch_size=64)

    return test_loader

def build_model():
    model = nn.Sequential(
        nn.Flatten(),
        nn.Linear(784, 128),
        nn.ReLU(),
        nn.Linear(128, 64),
        nn.ReLU(),
        nn.Linear(64, 10)
    )
    return model

def train_model(model, train_loader, criterion, T):

    criterion = nn.CrossEntropyLoss()

    opt = optim.SGD(model.parameters(), lr=0.001, momentum=0.9)

    model.train()

    for train_epoch in range(T):
        correct = 0
        running_loss = 0.0
        for i, data in enumerate(train_loader, 0):
            inputs, labels = data

            # zero the parameter gradients
            opt.zero_grad()

            # forward + backward + optimize
            outputs = model(inputs)
            loss = criterion(outputs, labels)
            loss.backward()
            opt.step()

            running_loss += loss.item()

            _, predicted = torch.max(outputs.data, 1)

            correct += (predicted == labels).sum().item()

        percentage = round((correct / 60000) * 100, 2)
        loss = round(running_loss/i, 3)
        print(f"Train Epoch: {train_epoch}  Accuracy: {correct}/60000({percentage}%) Loss: {loss}")

def evaluate_model(model, test_loader, criterion, show_loss=True):
    total = 0
    correct = 0
    running_loss = 0.0
    with torch.no_grad():
        for data in test_loader:
            images, labels = data

            # calculate outputs by running images through the network
            outputs = model(images)
            # the class with the highest energy is what we choose as prediction
            _, predicted = torch.max(outputs.data, 1)
            total += labels.size(0)
            correct += (predicted == labels).sum().item()

            loss = criterion(outputs, labels)
            running_loss += loss.item()

        if show_loss:
            average_loss = round(running_loss / total, 4)
            print(f"Average loss: {average_loss}")

        percentage = round(100 * (correct / total), 2)
        print(f"Accuracy: {percentage}%")


def predict_label(model, test_images, index):
    class_names = ['T-shirt/top', 'Trouser', 'Pullover', 'Dress', 'Coat', 'Sandal', 'Shirt', 'Sneaker', 'Bag', 'Ankle Boot']
    logits = model(test_images[index])
    prob = F.softmax(logits, dim = 1)

    value, index = torch.topk(prob, 3)

    for i in range(3):
        print(f'{class_names[index[0][i]]}: {round(value[0][i].item(), 2)}%')

if __name__ == '__main__':
    criterion = nn.CrossEntropyLoss()