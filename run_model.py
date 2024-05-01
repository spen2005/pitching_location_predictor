import torch
import torch.nn as nn
import math

# 定义神经网络模型
class SimpleNN(nn.Module):
    def __init__(self, input_size, hidden_size, output_size):
        super(SimpleNN, self).__init__()
        self.fc1 = nn.Linear(input_size, hidden_size)
        self.fc2 = nn.Linear(hidden_size, hidden_size)
        self.fc3 = nn.Linear(hidden_size, output_size)

    def forward(self, x):
        x = torch.relu(self.fc1(x))
        x = torch.relu(self.fc2(x))
        x = self.fc3(x)
        return x

# 加载训练好的模型参数
def load_model():
    model = SimpleNN(input_size=19, hidden_size=64, output_size=3)
    model.load_state_dict(torch.load('model.pth'))
    model.eval()
    return model

# 用户交互
def user_input(input_data):
    input_data = [float(num) for num in input_data]  # 将输入转换为浮点数
    normalized_input_data = []
    #regularization_value = sqrt(input_data[0]**2 + input_data[1]**2)
    regularization_value = math.sqrt(input_data[0]**2 + input_data[1]**2)
    for i in range(8):
        vec_x = input_data[i*2]
        vec_y = input_data[i*2+1]

        if regularization_value != 0:
            vec_x /= regularization_value
            vec_y /= regularization_value
        normalized_input_data.extend([vec_x, vec_y])
    timestamp = input_data[16]
    x_prime = input_data[17]
    y_prime = input_data[18]

    if regularization_value != 0:
        x_prime /= regularization_value
        y_prime /= regularization_value
    normalized_input_data.extend([timestamp, x_prime, y_prime])
    return normalized_input_data

# 模型预测
def predict(model, input_data):
    with torch.no_grad():
        output = model(torch.tensor(input_data, dtype=torch.float32).unsqueeze(0))
    return output.squeeze().cpu().numpy()

if __name__ == "__main__":
    # 加载模型
    model = load_model()

    # 读取文件内容
    with open('input.txt', 'r') as file:
        input_data = file.read().split()  # 按空格分割文件内容并存储为列表

    # 用户交互
    input_data = user_input(input_data)

    # 模型预测
    x_pred, y_pred, z_pred = predict(model, input_data)

    # 输出预测结果
    print(f"Predicted x: {x_pred}")
    print(f"Predicted y: {y_pred}")
    print(f"Predicted z: {z_pred}")

