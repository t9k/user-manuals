import os
import shutil

import torch
import torch.nn as nn
import torch.nn.functional as F
import torch.optim as optim
from torch.utils.tensorboard import SummaryWriter
from torchvision import datasets, transforms


class Net(nn.Module):

    def __init__(self):
        super().__init__()
        self.conv1 = nn.Conv2d(1, 32, 3, 1)
        self.conv2 = nn.Conv2d(32, 64, 3, 1)
        self.conv3 = nn.Conv2d(64, 64, 3, 1)
        self.pool = nn.MaxPool2d(2, 2)
        self.dense1 = nn.Linear(576, 64)
        self.dense2 = nn.Linear(64, 10)

    def forward(self, x):
        x = self.pool(F.relu(self.conv1(x)))
        x = self.pool(F.relu(self.conv2(x)))
        x = F.relu(self.conv3(x))
        x = torch.flatten(x, 1)
        x = F.relu(self.dense1(x))
        output = F.softmax(self.dense2(x), dim=1)
        return output


def train():
    global global_step
    for epoch in range(1, epochs + 1):
        model.train()
        for step, (data, target) in enumerate(train_loader, 1):
            data, target = data.to(device), target.to(device)
            optimizer.zero_grad()
            output = model(data)
            loss = criterion(output, target)
            loss.backward()
            optimizer.step()

            if step % 500 == 0:
                train_loss = loss.item()
                print('epoch {:d}/{:d}, batch {:5d}/{:d} with loss: {:.4f}'.
                      format(epoch, epochs, step, steps_per_epoch, train_loss))
                global_step = (epoch - 1) * steps_per_epoch + step

                writer.add_scalar('train/loss', train_loss, global_step)

        scheduler.step()
        global_step = epoch * steps_per_epoch
        test(val=True, epoch=epoch)


def test(val=False, epoch=None):
    label = 'val' if val else 'test'
    model.eval()
    running_loss = 0.0
    correct = 0

    with torch.no_grad():
        loader = val_loader if val else test_loader
        for data, target in loader:
            data, target = data.to(device), target.to(device)
            output = model(data)
            loss = criterion(output, target)
            running_loss += loss.item()
            prediction = output.max(1)[1]
            correct += (prediction == target).sum().item()

    test_loss = running_loss / len(loader)
    test_accuracy = correct / len(loader.dataset)
    msg = '{:s} loss: {:.4f}, {:s} accuracy: {:.4f}'.format(
        label, test_loss, label, test_accuracy)
    if val:
        msg = 'epoch {:d}/{:d} with '.format(epoch, epochs) + msg
    print(msg)

    writer.add_scalar('{:s}/loss'.format(label), test_loss, global_step)
    writer.add_scalar('{:s}/accuracy'.format(label), test_accuracy,
                      global_step)


device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
kwargs = {
    'num_workers': 1,
    'pin_memory': True
} if torch.cuda.is_available() else {}

torch.manual_seed(1)

model = Net().to(device)
criterion = nn.CrossEntropyLoss()
optimizer = optim.Adam(model.parameters(), lr=0.001)
scheduler = optim.lr_scheduler.StepLR(optimizer, step_size=1, gamma=0.7)

dataset_path = './data'
transform = transforms.Compose(
    [transforms.ToTensor(),
     transforms.Normalize((0.5), (0.5))])
train_dataset = datasets.MNIST(root=dataset_path,
                               train=True,
                               download=True,
                               transform=transform)
train_dataset, val_dataset = torch.utils.data.random_split(
    train_dataset, [48000, 12000])
test_dataset = datasets.MNIST(root=dataset_path,
                              train=False,
                              download=True,
                              transform=transform)
train_loader = torch.utils.data.DataLoader(train_dataset,
                                           batch_size=32,
                                           shuffle=True,
                                           **kwargs)
val_loader = torch.utils.data.DataLoader(val_dataset,
                                         batch_size=400,
                                         shuffle=False,
                                         **kwargs)
test_loader = torch.utils.data.DataLoader(test_dataset,
                                          batch_size=1000,
                                          shuffle=False,
                                          **kwargs)

log_dir = './log'
if os.path.exists(log_dir):
    shutil.rmtree(log_dir, ignore_errors=True)
writer = SummaryWriter(log_dir)

global_step = 0
epochs = 10
steps_per_epoch = len(train_loader)
train()
test()

torch.save(model.state_dict(), 'model_state_dict.pt')
