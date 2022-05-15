import cv2
import numpy as np
import paddle
import paddleseg.transforms as T
from paddleseg.models.unet import UNet


class LITSSeg(object):
    def __init__(self, weight_path: str) -> None:
        self.transforms = T.Compose([
            T.Resize(target_size=(512, 512)),
            T.Normalize()
        ])
        self.model = UNet(num_classes=3)
        self.model.set_dict(paddle.load(weight_path))
        self.model.eval()

    def pridect(self, imgs: np.ndarray) -> np.ndarray:
        preds = []
        for i in range(imgs.shape[0]):
            img = imgs[i, :, :]
            img[img > 200] = 200
            img[img < -200] = -200
            img = cv2.cvtColor(img, cv2.COLOR_GRAY2RGB)
            img, _ = self.transforms(img)
            img = paddle.to_tensor(img[None], dtype="float32")
            pred = self.model(img)
            preds.append(paddle.argmax(pred[0], axis=1).squeeze().numpy().astype("uint8"))
        return np.stack(preds, axis=0)