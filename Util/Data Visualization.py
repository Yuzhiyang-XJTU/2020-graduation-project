import torch
import torch.nn as nn
import torch.nn.functional as F
import torch.utils.data as Data
import numpy as np
from scipy.io import loadmat
import random
import matplotlib.pyplot as plt


"""参数迁移"""
""" 1.
# source_clf_loss和两个正确率
source_clf_loss = np.load(r'A:\我的交大\Transfer Learning\Deep Transfer Learning\参数迁移\source_clf_loss.npy')
acc_s = np.load(r'A:\我的交大\Transfer Learning\Deep Transfer Learning\参数迁移\total_acc_s.npy')
acc_t = np.load(r'A:\我的交大\Transfer Learning\Deep Transfer Learning\参数迁移\total_acc_t.npy')

print('数据长度：', acc_t.shape)
print('最大准确率：', np.max(acc_t))
print('此时位置：', np.argmax(acc_t))
print('后100次的平均准确率：', np.mean(acc_t[-100:]))

fig, ax1 = plt.subplots(figsize=(10, 5), dpi=125)
ax2 = ax1.twinx()

lns1 = ax1.plot(np.arange(0, source_clf_loss.shape[0], 1), source_clf_loss, 'r', label=r'$Source\ Clf\ Loss$')
lns2 = ax2.plot(np.arange(0, acc_s.shape[0]), acc_s, 'b', label=r'$Source\ Accuracy$')
lns3 = ax2.plot(np.arange(0, acc_t.shape[0]), acc_t, 'k', linewidth=0.8, label=r'$Target\ Accuracy$')

ax1.set_xlabel(r'$Iteration$', fontdict={'family': 'Times New Roman', 'size': 14})
ax1.set_ylabel(r'$Loss$', color='r', fontdict={'family': 'Times New Roman', 'size': 14})
ax2.set_ylabel(r'$Accuracy$', color='darkblue', fontdict={'family': 'Times New Roman', 'size': 14})

ax1.set_ylim(0, 30)

lns = lns1+lns2+lns3
labs = [l.get_label() for l in lns]
ax1.legend(lns, labs, loc=5)

plt.show()
"""

"""Dcoral方法"""
""" 1.
# 模型性能随参数变化趋势图 准确率变化图
params = [1, 10, 20, 30, 40, 50, 60, 70, 80, 90]

index = params.index(30)

acc_s = []

acc_mean = []

for param in params:
    acc_s.append(np.load(r'A:\我的交大\Transfer Learning\Deep Transfer Learning\Dcoral方法\{}\total_acc.npy'.format(param)))
    print('{}:'.format(param), np.mean(acc_s[-1][-100:]))
    acc_mean.append(np.mean(acc_s[-1][-100:]))

plt.figure(figsize=(10, 5), dpi=125)
plt.plot(np.arange(0, acc_s[index].shape[0]), acc_s[index], linewidth=0.7)
plt.xlabel(r'$Iteration$', fontdict={'family': 'Times New Roman', 'size': 14})
plt.ylabel(r'$Accuracy$', fontdict={'family': 'Times New Roman', 'size': 14})

plt.figure(figsize=(10, 5), dpi=125)
plt.plot(np.arange(0, len(acc_mean)), acc_mean, color='b', marker='o', markerfacecolor='r', markersize=10)
plt.xticks(np.arange(0, len(acc_mean)), params)
plt.xlabel(r'$Tradeoff\ parameter\ \alpha$', fontdict={'family': 'Times New Roman', 'size': 14})
plt.ylabel(r'$Accuracy$', fontdict={'family': 'Times New Roman', 'size': 14})
plt.show()
"""

""" 2.
# total_loss 与 source_clf的loss 与 transfer_loss 变化趋势图
total_loss = np.load(r'A:\我的交大\Transfer Learning\Deep Transfer Learning\Dcoral方法\30\total_loss.npy')
source_clf_loss = np.load(r'A:\我的交大\Transfer Learning\Deep Transfer Learning\Dcoral方法\30\source_clf_loss.npy')
transfer_loss = np.load(r'A:\我的交大\Transfer Learning\Deep Transfer Learning\Dcoral方法\30\transfer_loss.npy')

plt.figure(figsize=(10, 5), dpi=125)
plt.plot(np.arange(0, total_loss.shape[0]), total_loss, 'b', label=r'$total\ loss$')
plt.plot(np.arange(0, source_clf_loss.shape[0]), source_clf_loss, 'g', label=r'$source\ clf\ loss$')
plt.plot(np.arange(0, transfer_loss.shape[0]), transfer_loss, 'r', label=r'$transfer\ loss(coral)$')
plt.xlabel(r'$Iteration$', fontdict={'family': 'Times New Roman', 'size': 14})
plt.ylabel(r'$Loss$', fontdict={'family': 'Times New Roman', 'size': 14})
plt.ylim((0, 5))
plt.legend()
plt.show()
"""

""" 3.
# 迁移损失趋势图
transfer_loss = np.load(r'A:\我的交大\Transfer Learning\Deep Transfer Learning\Dcoral方法\30\transfer_loss.npy')
plt.figure(figsize=(10, 5), dpi=125)
plt.plot(np.arange(0, transfer_loss.shape[0]), transfer_loss, 'r', linewidth=0.9)
plt.xlabel(r'$Iteration$', fontdict={'family': 'Times New Roman', 'size': 14})
plt.ylabel(r'$Transfer\ loss(coral)$', fontdict={'family': 'Times New Roman', 'size': 14})
plt.show()
"""

"""单层MMD领域适配"""
""" 1.
# 模型性能随参数变化趋势图 准确率变化图
params = [0.01, 0.02, 0.04, 0.06, 0.08, 0.10, 0.12, 0.14, 0.16, 0.18, 0.2]

index = params.index(0.1)

acc_s = []

acc_mean = []

for param in params:
    acc_s.append(np.load(r'A:\我的交大\Transfer Learning\Deep Transfer Learning\单层MMD领域适配\{}\total_acc.npy'.format(param)))
    print('{}:'.format(param), np.mean(acc_s[-1][-100:]))
    acc_mean.append(np.mean(acc_s[-1][-100:]))

plt.figure(figsize=(10, 5), dpi=125)
plt.plot(np.arange(0, acc_s[index].shape[0]), acc_s[index], linewidth=0.8)
plt.xlabel(r'$Iteration$', fontdict={'family': 'Times New Roman', 'size': 14})
plt.ylabel(r'$Accuracy$', fontdict={'family': 'Times New Roman', 'size': 14})

plt.figure(figsize=(10, 5), dpi=125)
plt.plot(np.arange(0, len(acc_mean)), acc_mean, color='b', marker='o', markerfacecolor='r', markersize=10)
plt.xticks(np.arange(0, len(acc_mean)), params)
plt.xlabel(r'$Tradeoff\ parameter\ \alpha$', fontdict={'family': 'Times New Roman', 'size': 14})
plt.ylabel(r'$Accuracy$', fontdict={'family': 'Times New Roman', 'size': 14})
plt.show()
"""

""" 2.
# total_loss 与 source_clf的loss 与 transfer_loss 变化趋势图
total_loss = np.load(r'A:\我的交大\Transfer Learning\Deep Transfer Learning\单层MMD领域适配\0.1\total_loss.npy')
source_clf_loss = np.load(r'A:\我的交大\Transfer Learning\Deep Transfer Learning\单层MMD领域适配\0.1\source_clf_loss.npy')
transfer_loss = np.load(r'A:\我的交大\Transfer Learning\Deep Transfer Learning\单层MMD领域适配\0.1\transfer_loss.npy')

plt.figure(figsize=(10, 5), dpi=125)
plt.plot(np.arange(0, total_loss.shape[0]), total_loss, 'b', label=r'$total\ loss$')
plt.plot(np.arange(0, source_clf_loss.shape[0]), source_clf_loss, 'g', label=r'$source\ clf\ loss$')
plt.plot(np.arange(0, transfer_loss.shape[0]), transfer_loss, 'r', label=r'$transfer\ loss(MMD)$')
plt.xlabel(r'$Iteration$', fontdict={'family': 'Times New Roman', 'size': 14})
plt.ylabel(r'$Loss$', fontdict={'family': 'Times New Roman', 'size': 14})
plt.ylim((0, 7))
plt.legend()
plt.show()
"""

""" 3.
# 迁移损失趋势图
transfer_loss = np.load(r'A:\我的交大\Transfer Learning\Deep Transfer Learning\单层MMD领域适配\0.1\transfer_loss.npy')
plt.figure(figsize=(10, 5), dpi=125)
plt.plot(np.arange(0, transfer_loss.shape[0]), transfer_loss, 'r', linewidth=0.8)
plt.xlabel(r'$Iteration$', fontdict={'family': 'Times New Roman', 'size': 14})
plt.ylabel(r'$Transfer\ loss(MMD)$', fontdict={'family': 'Times New Roman', 'size': 14})
plt.show()
"""

"""多层MK-MMD领域适配"""
length = 4000
""" 1.
# total_loss 与 source_clf的loss 与 transfer_loss 变化趋势图
total_loss = np.load(r'A:\我的交大\Transfer Learning\Deep Transfer Learning\多层MK-MMD领域适配\total_loss.npy')[:length]
source_clf_loss = np.load(r'A:\我的交大\Transfer Learning\Deep Transfer Learning\多层MK-MMD领域适配\source_clf_loss.npy')[:length]
transfer_loss = np.load(r'A:\我的交大\Transfer Learning\Deep Transfer Learning\多层MK-MMD领域适配\transfer_loss.npy')[:length]

plt.figure(figsize=(10, 5), dpi=125)
plt.plot(np.arange(0, total_loss.shape[0]), total_loss, 'b', label=r'$total\ loss$')
plt.plot(np.arange(0, source_clf_loss.shape[0]), source_clf_loss, 'g', label=r'$source\ clf\ loss$')
plt.plot(np.arange(0, transfer_loss.shape[0]), transfer_loss, 'r', label=r'$transfer\ loss$')
plt.xlabel(r'$Iteration$', fontdict={'family': 'Times New Roman', 'size': 14})
plt.ylabel(r'$Loss$', fontdict={'family': 'Times New Roman', 'size': 14})
plt.ylim((0, 8))
plt.legend()
plt.show()
"""

""" 2.
# transfer_loss 与 C1、C2、F1、F2层MMD值 变化趋势图
transfer_loss = np.load(r'A:\我的交大\Transfer Learning\Deep Transfer Learning\多层MK-MMD领域适配\transfer_loss.npy')[:length]
tf_C1 = np.load(r'A:\我的交大\Transfer Learning\Deep Transfer Learning\多层MK-MMD领域适配\tf_C1.npy')[:length]
tf_C2 = np.load(r'A:\我的交大\Transfer Learning\Deep Transfer Learning\多层MK-MMD领域适配\tf_C2.npy')[:length]
tf_F1 = np.load(r'A:\我的交大\Transfer Learning\Deep Transfer Learning\多层MK-MMD领域适配\tf_F1.npy')[:length]
tf_F2 = np.load(r'A:\我的交大\Transfer Learning\Deep Transfer Learning\多层MK-MMD领域适配\tf_F2.npy')[:length]

plt.figure(figsize=(10, 5), dpi=125)
plt.plot(np.arange(0, transfer_loss.shape[0]), transfer_loss, 'r', linewidth=0.7, label=r'$total\ transfer\ loss$')
plt.plot(np.arange(0, tf_C1.shape[0]), tf_C1, 'm', linewidth=0.7, label=r'$C1\ transfer\ loss$')
plt.plot(np.arange(0, tf_C2.shape[0]), tf_C2, 'y', linewidth=0.7, label=r'$C2\ transfer\ loss$')
plt.plot(np.arange(0, tf_F1.shape[0]), tf_F1, 'g', linewidth=0.7, label=r'$F1\ transfer\ loss$')
plt.plot(np.arange(0, tf_F2.shape[0]), tf_F2, 'k', linewidth=0.7, label=r'$F2\ transfer\ loss$')
plt.xlabel(r'$Iteration$', fontdict={'family': 'Times New Roman', 'size': 14})
plt.ylabel(r'$Transfer\ Loss$', fontdict={'family': 'Times New Roman', 'size': 14})
plt.legend()
plt.show()
"""

""" 3.
# 准确率 变化趋势图
acc = np.load(r'A:\我的交大\Transfer Learning\Deep Transfer Learning\多层MK-MMD领域适配\total_acc.npy')[:length]

print('数据长度：', acc.shape)
print('最大准确率：', np.max(acc))
print('此时位置：', np.argmax(acc))
print('后100次的平均准确率：', np.mean(acc[-100:]))

plt.figure(figsize=(10, 5), dpi=125)
plt.plot(np.arange(0, acc.shape[0]), acc)
plt.xlabel(r'$Iteration$', fontdict={'family': 'Times New Roman', 'size': 14})
plt.ylabel(r'$Accuracy$', fontdict={'family': 'Times New Roman', 'size': 14})
plt.show()
"""

"""联合概率分布适配"""
""" 1.
# 各超参数 准确率 MMD变化趋势折线图
alpha_params = [0.01, 0.05, 0.1, 0.5, 1]
beta_params = [0.01, 0.02, 0.03, 0.04, 0.05]

beta_color = {0: 'k', 0.01: 'r', 0.02: 'g', 0.03: 'b', 0.04: 'c', 0.05: 'm'}  # beta参数与颜色映射字典

plt.figure(figsize=(10, 5), dpi=125)
for beta in beta_params:
    print('-'*10)
    acc = []  # 全部准确率
    acc_mean = []  # 后100次平均准确率

    color = beta_color[beta]

    for alpha in alpha_params:
        acc.append(np.load(r'A:\我的交大\Transfer Learning\Deep Transfer Learning\条件分布适配\a{} b{}\total_acc.npy'.format(alpha, beta)))
        print('alpha:{}, beta:{}, acc:'.format(alpha, beta), np.mean(acc[-1][-100:]))
        acc_mean.append(np.mean(acc[-1][-100:]))

    plt.plot(np.arange(0, len(acc_mean)), acc_mean, color=color, marker='o', markersize=6, label=r'$\beta = {}$'.format(beta))
    print('-'*10)
plt.xlabel(r'$Tradeoff\ parameter\ \alpha$', fontdict={'family': 'Times New Roman', 'size': 14})
plt.ylabel(r'$Accuracy$', fontdict={'family': 'Times New Roman', 'size': 14})
plt.xticks(np.arange(0, len(acc_mean)), alpha_params)
plt.legend()


plt.figure(figsize=(10, 5), dpi=125)
for beta in beta_params:
    print('-'*10)
    MMD = []  # 全部MMD
    MMD_mean = []  # 后100次平均MMD

    color = beta_color[beta]

    for alpha in alpha_params:
        MMD.append(np.load(r'A:\我的交大\Transfer Learning\Deep Transfer Learning\条件分布适配\a{} b{}\transfer_loss.npy'.format(alpha, beta)))
        print('alpha:{}, beta:{}, MMD:'.format(alpha, beta), np.mean(MMD[-1][-100:]))
        MMD_mean.append(np.mean(MMD[-1][-100:]))

    plt.plot(np.arange(0, len(MMD_mean)), MMD_mean, color=color, marker='o', markersize=6, label=r'$\beta = {}$'.format(beta))
    print('-'*10)
plt.xlabel(r'$Tradeoff\ parameter\ \alpha$', fontdict={'family': 'Times New Roman', 'size': 14})
plt.ylabel(r'$MMD$', fontdict={'family': 'Times New Roman', 'size': 14})
plt.xticks(np.arange(0, len(MMD_mean)), alpha_params)
plt.legend()
plt.show()
"""

""" 2.
# 各超参数 准确率 热力图
alpha_params = [0.01, 0.05, 0.1, 0.5, 1]
beta_params = [0.05, 0.04, 0.03, 0.02, 0.01]

acc_matrix = []

for beta in beta_params:
    acc_beta = []
    for alpha in alpha_params:
        acc_beta.append(100*np.mean(np.load(r'A:\我的交大\Transfer Learning\Deep Transfer Learning\条件分布适配\a{} b{}\total_acc.npy'.format(alpha, beta))[-100:]))
    acc_matrix.append(acc_beta)
for line in acc_matrix:
    print(line)

plt.imshow(acc_matrix, interpolation='spline36', cmap=plt.cm.Blues)
plt.colorbar()

plt.text(4.6, -0.7, r'$Acc.(\%)$', fontdict={'family': 'Times New Roman', 'size': 12})
tick_marks = np.arange(len(alpha_params))
plt.xticks(tick_marks, alpha_params, rotation=0, size=12)
plt.yticks(tick_marks, beta_params, size=12)
plt.xlabel(r'$Tradeoff\ parameter\ \alpha$', fontdict={'family': 'Times New Roman', 'size': 14})
plt.ylabel(r'$Tradeoff\ parameter\ \beta$', fontdict={'family': 'Times New Roman', 'size': 14})
plt.show()
"""

""" 3.
# total_loss 与 source_clf_loss 与 transfer_loss 和 target_clf_loss变化趋势图
alpha = 0.5
beta = 0.03

total_loss = np.load(r'A:\我的交大\Transfer Learning\Deep Transfer Learning\条件分布适配\a{} b{}\total_loss.npy'.format(alpha, beta))
source_clf_loss = np.load(r'A:\我的交大\Transfer Learning\Deep Transfer Learning\条件分布适配\a{} b{}\source_clf_loss.npy'.format(alpha, beta))
transfer_loss = np.load(r'A:\我的交大\Transfer Learning\Deep Transfer Learning\条件分布适配\a{} b{}\transfer_loss.npy'.format(alpha, beta))
target_clf_loss = np.load(r'A:\我的交大\Transfer Learning\Deep Transfer Learning\条件分布适配\a{} b{}\target_clf_loss.npy'.format(alpha, beta))

plt.figure(figsize=(10, 5), dpi=125)
plt.plot(np.arange(0, total_loss.shape[0]), total_loss, 'b', linewidth=0.7, label=r'$total\ loss$')
plt.plot(np.arange(0, source_clf_loss.shape[0]), source_clf_loss, 'g', linewidth=0.7, label=r'$source\ clf\ loss$')
plt.plot(np.arange(0, transfer_loss.shape[0]), transfer_loss, 'r', linewidth=0.7, label=r'$transfer\ loss$')
plt.plot(np.arange(0, target_clf_loss.shape[0]), target_clf_loss, 'm', linewidth=0.7, label=r'$target\ clf\ loss$')
plt.xlabel(r'$Iteration$', fontdict={'family': 'Times New Roman', 'size': 14})
plt.ylabel(r'$Loss$', fontdict={'family': 'Times New Roman', 'size': 14})
plt.ylim((0, 7))
plt.legend()
plt.show()
"""

""" 4.
# transfer_loss 与 C1、C2、F1、F2层MMD值 变化趋势图
alpha = 0.5
beta = 0.03
transfer_loss = np.load(r'A:\我的交大\Transfer Learning\Deep Transfer Learning\条件分布适配\a{} b{}\transfer_loss.npy'.format(alpha, beta))
tf_C1 = np.load(r'A:\我的交大\Transfer Learning\Deep Transfer Learning\条件分布适配\a{} b{}\tf_C1.npy'.format(alpha, beta))
tf_C2 = np.load(r'A:\我的交大\Transfer Learning\Deep Transfer Learning\条件分布适配\a{} b{}\tf_C2.npy'.format(alpha, beta))
tf_F1 = np.load(r'A:\我的交大\Transfer Learning\Deep Transfer Learning\条件分布适配\a{} b{}\tf_F1.npy'.format(alpha, beta))
tf_F2 = np.load(r'A:\我的交大\Transfer Learning\Deep Transfer Learning\条件分布适配\a{} b{}\tf_F2.npy'.format(alpha, beta))

plt.figure(figsize=(10, 5), dpi=125)
plt.plot(np.arange(0, transfer_loss.shape[0]), transfer_loss, 'r', linewidth=0.7, label=r'$total\ transfer\ loss$')
plt.plot(np.arange(0, tf_C1.shape[0]), tf_C1, 'c', linewidth=0.7, label=r'$C1\ transfer\ loss$')
plt.plot(np.arange(0, tf_C2.shape[0]), tf_C2, 'y', linewidth=0.7, label=r'$C2\ transfer\ loss$')
plt.plot(np.arange(0, tf_F1.shape[0]), tf_F1, 'g', linewidth=0.7, label=r'$F1\ transfer\ loss$')
plt.plot(np.arange(0, tf_F2.shape[0]), tf_F2, 'k', linewidth=0.7, label=r'$F2\ transfer\ loss$')
plt.xlabel(r'$Iteration$', fontdict={'family': 'Times New Roman', 'size': 14})
plt.ylabel(r'$Transfer\ Loss$', fontdict={'family': 'Times New Roman', 'size': 14})
plt.legend()
plt.show()
"""

""" 5.
# 准确率 变化趋势图
alpha = 0.5
beta = 0.03
acc = np.load(r'A:\我的交大\Transfer Learning\Deep Transfer Learning\条件分布适配\a{} b{}\total_acc.npy'.format(alpha, beta))

print('数据长度：', acc.shape)
print('最大准确率：', np.max(acc))
print('此时位置：', np.argmax(acc))
print('后100次的平均准确率：', np.mean(acc[-100:]))

plt.figure(figsize=(10, 5), dpi=125)
plt.plot(np.arange(0, acc.shape[0]), acc)
plt.xlabel(r'$Iteration$', fontdict={'family': 'Times New Roman', 'size': 14})
plt.ylabel(r'$Accuracy$', fontdict={'family': 'Times New Roman', 'size': 14})
plt.show()
"""







