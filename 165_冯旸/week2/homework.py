# coding:utf8

import torch
import torch.nn as nn
import numpy as np
import random
import json
import matplotlib.pyplot as plt

"""

基于pytorch框架编写模型训练
实现一个自行构造的找规律(机器学习)任务，多分类，使用上交叉熵
规律：x是一个10维向量，1+2最大为1类，3+4最大为2类...

"""

def build_sample():
    x = np.random.random(10)
    max = 0
    s = 0
    for n in range(5):
        if x[s] + x[s+1] > max :
            max = x[s] + x[s+1]
        s += 2
    # if x[0] + x[1] == max:
    #     return x, 0
    # elif x[2] + x[3] == max :
    #     return x, 1
    # elif x[4] + x[5] == max :
    #     return x, 2
    # elif x[6] + x[7] == max :
    #     return x, 3
    # elif x[8] + x[9] == max :
    #     return x, 4        #如果这里y改成[0,0,0,0,1]，可行吗

    if x[0] + x[1] == max:
        return x, [1,0,0,0,0]
    elif x[2] + x[3] == max :
        return x, [0,1,0,0,0]
    elif x[4] + x[5] == max :
        return x, [0,0,1,0,0]
    elif x[6] + x[7] == max :
        return x, [0,0,0,1,0]
    elif x[8] + x[9] == max :
        return x, [0,0,0,0,1]


def build_dataset(total_sample_num):
    X = []
    Y = []
    for i in range(total_sample_num):
        x, y = build_sample()
        X.append(x)
        Y.append(y)
    # return torch.FloatTensor(X), torch.LongTensor(Y)
    return torch.FloatTensor(X), torch.FloatTensor(Y)


class TorchModel(nn.Module):
    def __init__(self, input_size):
        super(TorchModel, self).__init__()
        self.linear = nn.Linear(input_size, 5)  # 线性层
        self.activation = torch.sigmoid  # sigmoid归一化函数
        self.loss = nn.functional.cross_entropy  # loss函数采用交叉熵

        # 当输入真实标签，返回loss值；无真实标签，返回预测值
    def forward(self, x, y=None):
        x = self.linear(x)  # (batch_size, input_size) -> (batch_size, 1)
        y_pred = self.activation(x)  # (batch_size, 1) -> (batch_size, 1)

        if y is not None:
            return self.loss(y_pred, y)  # 预测值和真实值计算损失
        else:
            return y_pred  # 输出预测结果

def evaluate(model):
    model.eval()
    test_sample_num = 100
    x, y = build_dataset(test_sample_num)
    # print("本次预测集中共有%d个正样本，%d个负样本" % (sum(torch.argmax(y)), test_sample_num - sum(torch.argmax(y))))
    correct, wrong = 0, 0
    with torch.no_grad():
        y_pred = model(x)  # 模型预测
        for y_p, y_t in zip(y_pred, y):  # 与真实标签进行对比
            if torch.argmax(y_p) == torch.argmax(y_t):
                correct += 1
            else:
                wrong += 1
    print("正确预测个数：%d, 正确率：%f" % (correct, correct / (correct + wrong)))
    return correct / (correct + wrong)


def main():
    # 配置参数
    epoch_num = 20  # 训练轮数
    batch_size = 20  # 每次训练样本个数
    train_sample = 5000  # 每轮训练总共训练的样本总数
    input_size = 10  # 输入向量维度
    learning_rate = 0.001  # 学习率
    # 建立模型
    model = TorchModel(input_size)
    # 选择优化器
    optim = torch.optim.Adam(model.parameters(), lr=learning_rate)
    log = []
    # 创建训练集，正常任务是读取训练集
    train_x, train_y = build_dataset(train_sample)
    # 训练过程
    for epoch in range(epoch_num):
        model.train()
        watch_loss = []
        for batch_index in range(train_sample // batch_size):
            x = train_x[batch_index * batch_size : (batch_index + 1) * batch_size]
            y = train_y[batch_index * batch_size : (batch_index + 1) * batch_size]

            loss = model(x, y)  # 计算loss
            loss.backward()  # 计算梯度
            optim.step()  # 更新权重
            optim.zero_grad()  # 梯度归零
            watch_loss.append(loss.item())
        print("=========\n第%d轮平均loss:%f" % (epoch + 1, np.mean(watch_loss)))
        acc = evaluate(model)  # 测试本轮模型结果
        log.append([acc, float(np.mean(watch_loss))])
    # 保存模型
    torch.save(model.state_dict(), "modelwork.pt")
    # 画图
    print(log)
    plt.plot(range(len(log)), [l[0] for l in log], label="acc")  # 画acc曲线
    plt.plot(range(len(log)), [l[1] for l in log], label="loss")  # 画loss曲线
    plt.legend()
    plt.show()
    return
























if __name__ == "__main__":
    main()
