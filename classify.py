import sys
import torch
import torch.nn as nn
from torchvision import transforms
from PIL import Image

class BinaryClassificationNet(nn.Module):
    def __init__(self):
        super(BinaryClassificationNet, self).__init__()
        self.conv1 = nn.Conv2d(3, 32, 3, padding=1)
        self.pool = nn.MaxPool2d(2, 2)
        self.conv2 = nn.Conv2d(32, 64, 3, padding=1)
        self.conv3 = nn.Conv2d(64, 128, 3, padding=1)
        self.fc1 = nn.Linear(128 * 8 * 8, 128)
        self.fc2 = nn.Linear(128, 1)
        self.sigmoid = nn.Sigmoid()

    def forward(self, x):
        x = self.pool(torch.relu(self.conv1(x)))
        x = self.pool(torch.relu(self.conv2(x)))
        x = self.pool(torch.relu(self.conv3(x)))
        x = x.view(-1, 128 * 8 * 8)
        x = torch.relu(self.fc1(x))
        x = self.sigmoid(self.fc2(x))
        return x

def load_model():
    model = BinaryClassificationNet()
    model.load_state_dict(torch.load('binary_classification_net.pth', map_location=torch.device('cpu')))
    model.eval()
    return model

def classify_image(image_path):
    model = load_model()
    
    transform = transforms.Compose([
        transforms.Resize((64, 64)),
        transforms.ToTensor(),
        transforms.Normalize((0.5, 0.5, 0.5), (0.5, 0.5, 0.5))
    ])
    
    image = Image.open(image_path)
    image = transform(image).unsqueeze(0)
    
    with torch.no_grad():
        output = model(image)
        prediction = torch.sigmoid(output)
        predicted_class = (prediction > 0.5).float().item()
    
    return "This is an automobile" if predicted_class == 1.0 else "This is an aircraft"

if __name__ == "__main__":
    image_path = sys.argv[1]
    result = classify_image(image_path)
    print(result)
