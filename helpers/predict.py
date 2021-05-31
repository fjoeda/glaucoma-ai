import torch
import torchvision
from torchvision import transforms

class ImagePredictor:

    def __init__(self):
        super().__init__()
        self.normalize = transforms.Normalize(
            mean = [0.485,0.456,0.406], 
            std = [0.229, 0.224, 0.225]
        )
        self.device = torch.device('cpu')
        self.loaded_model = torch.load('glaucoma_net.pth', map_location=torch.device('cpu'))
        self.loaded_model.to(self.device)
        self.loaded_model.eval()
        self.val_data_transforms = transforms.Compose([
            transforms.Resize((224,224)),
            transforms.ToTensor(),
            self.normalize
        ])

    def predict(self,img):
        img_tensor = self.val_data_transforms(img)
        img_tensor = img_tensor.unsqueeze(0).to(self.device)

        output = self.loaded_model(img_tensor)
        pred = torch.max(output.data,1)[1]
        prob = torch.softmax(output,1)
        return prob[0][0].item(), prob[0][1].item()