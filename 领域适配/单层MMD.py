import torch
import torch.nn as nn
import torch.nn.functional as F
import torch.utils.data as Data
from torch import utils
import numpy as np
from scipy.io import loadmat
import random
import matplotlib.pyplot as plt
import math


torch.manual_seed(1)


class Net(nn.Module):
    def __init__(self):
        super(Net, self).__init__()
        self.conv1 = nn.Conv2d(in_channels=1, out_channels=10, kernel_size=(1, 5))
        self.pool1 = nn.MaxPool2d(kernel_size=(1, 2))

        self.conv2 = nn.Conv2d(in_channels=10, out_channels=10, kernel_size=(1, 3))
        self.pool2 = nn.MaxPool2d(kernel_size=(1, 2))

        self.flatten2 = nn.Linear(in_features=2480, out_features=256)

        self.flatten3 = nn.Linear(in_features=256, out_features=5)

    # 前向传播
    def forward(self, source, target):
        bs = source.shape[0]

        source = F.leaky_relu(self.conv1(source))
        target = F.leaky_relu(self.conv1(target))

        source = F.leaky_relu(self.conv2(self.pool1(source)))
        target = F.leaky_relu(self.conv2(self.pool1(target)))

        source = (self.pool2(source)).view(bs, -1)
        target = (self.pool2(target)).view(bs, -1)

        source = F.leaky_relu(self.flatten2(source))
        target = F.leaky_relu(self.flatten2(target))

        transfer_loss = self.MMD(source.squeeze(), target.squeeze())

        source_clf = self.flatten3(source)
        target_clf = self.flatten3(target)

        return source_clf, target_clf, transfer_loss

    # 预测
    def predict(self, source):
        bs = source.shape[0]

        source = F.leaky_relu(self.conv1(source))
        source = F.leaky_relu(self.conv2(self.pool1(source)))
        source = (self.pool2(source)).view(bs, -1)
        source = F.leaky_relu(self.flatten2(source))

        source_clf = self.flatten3(source)

        return source_clf

    def guassian_kernel(self, source, target, kernel_mul=2.0, kernel_num=5):
        """
        将源域和目标域数据转换为核矩阵
        参数：
            source:源域数据（n * 数据长度）
            target:目标域数据（m * 数据长度）
            kernel_mul:不同高斯核sigma值的比例
            kernel_num:取不同高斯核的数量
        返回：
            多个高斯核矩阵之和
        """

        n_samples = source.shape[0] + target.shape[0]  # 矩阵行数， 一般为batch_size的两倍

        total = torch.cat([source, target], dim=0)  # 将source， target按列合并
        total0 = total.unsqueeze(0).expand(total.shape[0], total.shape[0], total.shape[1])  # 将total复制（n+m）份， 第二维是样本维
        total1 = total.unsqueeze(1).expand(total.shape[0], total.shape[0], total.shape[1])  # 将total复制（n+m）份， 第一维是样本维

        L2_distance = ((total0 - total1) ** 2).sum(2)  # 求任意两样本数据的L2距离

        # 创建kernel_num数量个（以kernel_mul为倍数）带宽（sigma）
        bandwidth = torch.sum(L2_distance.data) / (n_samples ** 2 - n_samples)
        bandwidth /= kernel_mul ** (kernel_num // 2)
        bandwidth_list = [bandwidth * (kernel_mul ** i) for i in range(kernel_num)]

        # 创建kernel_num数量个高斯核矩阵
        kernel_val = [torch.exp(-L2_distance / bandwidth_temp) for bandwidth_temp in bandwidth_list]

        del L2_distance, total0, total1, total

        # 返回最终的核矩阵
        return sum(kernel_val) / len(kernel_val)

    def MMD(self, source, target):
        """
        计算源域和目标域数据的MMD距离
        """
        batch_size = source.shape[0]  # 获得批次大小
        kernels = self.guassian_kernel(source, target)  # 获得高斯核矩阵

        # 将核矩阵分为四部分
        XX = kernels[:batch_size, :batch_size]
        YY = kernels[batch_size:, batch_size:]
        XY = kernels[:batch_size, batch_size:]
        YX = kernels[batch_size:, :batch_size]

        MMD = torch.mean(XX + YY - XY - YX)  # 计算MMD距离
        return MMD

    def MMD_fast(self, source, target):
        batch_size = source.shape[0]  # 获得批次大小
        kernels = self.guassian_kernel(source, target)  # 获得高斯核矩阵

        loss = 0
        for i in range(batch_size):
            s1, s2 = i, (i + 1) % batch_size
            t1, t2 = s1 + batch_size, s2 + batch_size
            # print(s1, s2, t1, t2)
            loss += kernels[s1, s2] + kernels[t1, t2]
            loss -= kernels[s1, t2] + kernels[s2, t1]
        return torch.abs(loss / batch_size)


def accuracy_m(net, data_iter):
    net.eval()
    with torch.no_grad():
        num_acc = 0
        num_examples = 0
        matrix = torch.zeros((5, 5))
        for X, y in data_iter:

            predicts = net.predict(X)

            num_acc += (predicts.argmax(dim=1, keepdim=True) == y.view(-1, 1)).float().sum().item()

            num_examples += X.size()[0]

            for i in range(0, X.size(0)):

                matrix[y[i].item(), predicts.argmax(dim=1, keepdim=True)[i].item()] += 1

        return num_acc/num_examples, matrix


def Z_Score(data):
    num_example = len(data)
    length = len(data[0])
    for example in range(num_example):
        total = torch.sum(data[example]).item()
        ave = float(total) / length

        tempsum = torch.sum((data[example] - ave) ** 2).item()
        tempsum = (tempsum / length) ** 0.5

        data[example] = (data[example] - ave) / tempsum

    return data


def weights_init(m):
    classname = m.__class__.__name__
    if classname.find('Conv') != -1:
        n = m.kernel_size[0] * m.kernel_size[1] * m.out_channels
        m.weight.data.normal_(0, math.sqrt(2. / n))
        if m.bias is not None:
            m.bias.data.zero_()
    elif classname.find('BatchNorm') != -1:
        m.weight.data.fill_(1)
        m.bias.data.zero_()
    elif classname.find('Linear') != -1:
        n = m.weight.size(1)
        m.weight.data.normal_(0, 0.01)
        m.bias.data = torch.ones(m.bias.data.size())


"""设置超参数"""
batch_size = 32
lr = 0.001
num_epochs = 10000

momentum = 0.9
l2_decay = 5e-4

lambd = 0.18  # 迁移损失比重

if torch.cuda.is_available():
    device = torch.device("cuda")
    print('GPU数量：', torch.cuda.device_count())
    print('当前GPU索引号:', torch.cuda.current_device())
    print('根据索引号查看GPU名字：', torch.cuda.get_device_name(0))


# 加载源域
path_source = ['S1.npy', 'S2.npy', 'S3.npy', 'S4.npy', 'S5.npy']

for i in [0, 1, 2, 3, 4]:  # 读入数据和标签转换成tensor
    print('-' * 10)
    if i == 0:
        source_data = torch.tensor(np.load(path_source[i]), dtype=torch.float32)
        # source_data = Z_Score(source_data)
        source_data = source_data.view(source_data.shape[0], 1, 1, source_data.shape[1])
        print('source_data_{}.shape'.format(i), source_data.shape)
        source_labels = torch.zeros((source_data.shape[0], 1), dtype=torch.long)
        print('source_labels_{}.shape'.format(i), source_labels.shape)
    else:
        temp_data = torch.tensor(np.load(path_source[i]), dtype=torch.float32)
        # temp_data = Z_Score(temp_data)
        temp_data = temp_data.view(temp_data.shape[0], 1, 1, temp_data.shape[1])
        print('source_data_{}.shape'.format(i), temp_data.shape)
        temp_labels = torch.zeros((temp_data.shape[0], 1), dtype=torch.long) + i
        print('source_labels_{}.shape'.format(i), temp_labels.shape)

        source_data = torch.cat([source_data, temp_data], dim=0)
        source_labels = torch.cat([source_labels, temp_labels], dim=0)
    print('-' * 10)

# 打印读取后source的数据和标签shape
print('-' * 10)
print('source.shape:', source_data.shape)
print('source_labels.shape', source_labels.shape)
print('-' * 10)

# 加载目标域
path_target = ['T1.npy', 'T2.npy', 'T3.npy', 'T4.npy', 'T5.npy']

for i in [0, 1, 2, 3, 4]:  # 读入数据和标签转换成tensor
    print('-' * 10)
    if i == 0:
        target_data = torch.tensor(np.load(path_target[i]), dtype=torch.float32)
        # target_data = Z_Score(target_data)
        target_data = target_data.view(target_data.shape[0], 1, 1, target_data.shape[1])
        print('target_data_{}.shape'.format(i), target_data.shape)
        target_labels = torch.zeros((target_data.shape[0], 1), dtype=torch.long)
        print('target_labels_{}.shape'.format(i), target_labels.shape)
    else:
        temp_data = torch.tensor(np.load(path_target[i]), dtype=torch.float32)
        # temp_data = Z_Score(temp_data)
        temp_data = temp_data.view(temp_data.shape[0], 1, 1, temp_data.shape[1])
        print('target_data_{}.shape'.format(i), temp_data.shape)
        temp_labels = torch.zeros((temp_data.shape[0], 1), dtype=torch.long) + i
        print('target_labels_{}.shape'.format(i), temp_labels.shape)

        target_data = torch.cat([target_data, temp_data], dim=0)
        target_labels = torch.cat([target_labels, temp_labels], dim=0)
    print('-' * 10)

# 打印读取后target的数据和标签shape
print('-' * 10)
print('target.shape:', target_data.shape)
print('target_labels.shape', target_labels.shape)
print('-' * 10)

"""打印网络结构"""
net = Net()
print('-' * 10)
print(net)
print('-' * 10)

# 模型初始化
net.apply(weights_init)

"""创建数据生成器"""
# source_dataset = Data.TensorDataset(source_data, source_labels)
# source_iter = Data.DataLoader(source_dataset, batch_size=batch_size, shuffle=True)
#
# target_dataset = Data.TensorDataset(target_data, target_labels)
# target_iter = Data.DataLoader(target_dataset, batch_size=batch_size, shuffle=True)


source_dataset = Data.TensorDataset(source_data.to(device), source_labels.to(device))
source_iter = Data.DataLoader(source_dataset, batch_size=batch_size, shuffle=True)

target_dataset = Data.TensorDataset(target_data.to(device), target_labels.to(device))
target_iter = Data.DataLoader(target_dataset, batch_size=batch_size, shuffle=True)

net.to(device)

# 清空内存
del source_data, target_data, temp_data, source_labels, target_labels

"""训练"""
len_source_loader = len(source_iter)
len_target_loader = len(target_iter)

# 定义优化器
optimizer = torch.optim.Adam(net.parameters(), lr=lr, weight_decay=l2_decay)

# 定义损失
criterion = nn.CrossEntropyLoss()

# 存储各类损失
total_loss = []  # 总损失
total_source_clf_loss = []  # 源分类损失
total_transfer_loss = []  # 迁移损失

total_acc = []  # 准确率

# 初始化Max_acc
Max_acc = 0

print('len_source_loader=', len_source_loader)
print('len_target_loader=', len_target_loader)
print('n_batch=', min(len_source_loader, len_target_loader))

print('Epoch:{}, target_acc:{}, source_acc:{}'.format(0, accuracy_m(net, target_iter)[0], accuracy_m(net, source_iter)[0]))

for epoch in range(1, num_epochs + 1):
    net.train()

    iter_source, iter_target = iter(source_iter), iter(target_iter)
    n_batch = min(len_source_loader, len_target_loader)

    optimizer.zero_grad()  # 梯度清零
    for batch in range(1, n_batch + 1):

        data_source, label_source = iter_source.next()
        data_target, label_target = iter_target.next()

        if data_source.size(0) != batch_size or data_target.size(0) != batch_size:
            continue

        label_source_pred, label_target_pred, transfer_loss = net(data_source, data_target)

        source_clf_loss = criterion(label_source_pred, label_source.squeeze())

        loss = source_clf_loss + lambd * transfer_loss

        if batch == 1:
            total_loss.append(loss.item())
            total_source_clf_loss.append(source_clf_loss.item())
            total_transfer_loss.append(transfer_loss.item())

        else:
            total_loss[-1] += loss.item()
            total_source_clf_loss[-1] += source_clf_loss.item()
            total_transfer_loss[-1] += transfer_loss.item()

        optimizer.zero_grad()  # 梯度清零
        loss.backward()  # 反向传播
        optimizer.step()  # 优化

    acc, matrix = accuracy_m(net, target_iter)
    total_acc.append(acc)

    if acc >= Max_acc:
        # 保存网络参数
        PATH = 'Max_单层MMD_params.pth'
        torch.save(net.state_dict(), PATH)
        Max_acc = acc

    PATH = 'Last_单层MMD_params.pth'
    torch.save(net.state_dict(), PATH)

    # 保存节点实验数据
    np.save(r'total_acc.npy', np.array(total_acc))

    np.save(r'total_loss.npy', np.array(total_loss))
    np.save(r'source_clf_loss.npy', np.array(total_source_clf_loss))
    np.save(r'transfer_loss.npy', np.array(total_transfer_loss))

    print('-' * 90)
    print('Epoch:{}, target_acc:{}, source_acc:{}, lambd:{}'.format(epoch, total_acc[-1], accuracy_m(net, source_iter)[0], lambd))
    print('loss:{}, source_loss:{}, transfer_loss:{}'.format(
        total_loss[-1], total_source_clf_loss[-1], total_transfer_loss[-1]))
    print(matrix)



