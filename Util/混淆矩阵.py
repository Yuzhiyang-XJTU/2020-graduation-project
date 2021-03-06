import numpy as np
import matplotlib.pyplot as plt

classes = ['1', '2', '3', '4', '5']
confusion_matrix = np.array([[97, 0, 0, 0, 0],
                             [4, 77, 0, 16, 0],
                             [2, 0, 95, 0, 0],
                             [0, 0, 0, 97, 0],
                             [0, 0, 0, 0, 97]], dtype=np.float64)/97

plt.imshow(confusion_matrix, interpolation='nearest', cmap=plt.cm.Blues)  # 按照像素显示出矩阵
# plt.title('confusion_matrix')
cb = plt.colorbar()
tick_marks = np.arange(len(classes))
plt.xticks(tick_marks, classes, rotation=0, size=12)
plt.yticks(tick_marks, classes, size=12)

thresh = confusion_matrix.max() / 2.
# iters = [[i,j] for i in range(len(classes)) for j in range((classes))]
# ij配对，遍历矩阵迭代器
iters = np.reshape([[[i, j] for j in range(5)] for i in range(5)], (confusion_matrix.size, 2))
for i, j in iters:
    plt.text(j, i, format(round(confusion_matrix[i, j], 3) if confusion_matrix[i, j] != 0 else 0), horizontalalignment="center",
             color='white' if confusion_matrix[i, j] > thresh else 'black')  # 显示对应的数字

plt.ylabel('True label', fontdict={'family': 'Times New Roman', 'size': 15})
plt.xlabel('Predicted label', fontdict={'family': 'Times New Roman', 'size': 15})
plt.tight_layout()
plt.show()
