import numpy as np
from scipy.io import loadmat


def data_process(paths, example_size):
    num_example = 589

    datas = []
    A = []
    for i in range(len(paths)):  # 每一个舰船
        datas.append(loadmat(paths[i]))
        datas[i] = list(datas[i]['y'].flatten())

        # 数据切片
        j = 0
        while j + example_size < len(datas[i]):
            A.append(datas[i][j:j + example_size])
            j += example_size

    A = np.array(A)  # 将列表转换为 nd array
    np.random.shuffle(A)

    A = A[:num_example]

    print('A.shape=', A.shape)
    return A


fs = 52734
example_size = 2000

root_path = r'A:\我的交大\Transfer Learning\数据\源A -目标A（滤波、无降采样）'

paths_source_1 = [root_path + r'\39.mat']

paths_source_2 = [root_path + r'\29.mat']

paths_source_3 = [root_path + r'\6.mat']

paths_source_4 = [root_path + r'\25.mat']

paths_source_5 = [root_path + r'\18.mat']


# S1
print('S1 start!')
S1 = data_process(paths_source_1, example_size)
print('S1 over！')
print()
np.save('S1.npy', S1)

# S2
print('S2 start!')
S2 = data_process(paths_source_2, example_size)
print('S2 over！')
print()
np.save('S2.npy', S2)

# S3
print('S3 start!')
S3 = data_process(paths_source_3, example_size)
print('S3 over！')
print()
np.save('S3.npy', S3)

# S4
print('S4 start!')
S4 = data_process(paths_source_4, example_size)
print('S4 over！')
print()
np.save('S4.npy', S4)

# S5
print('S5 start!')
S5 = data_process(paths_source_5, example_size)
print('S5 over！')
print()
np.save('S5.npy', S5)
