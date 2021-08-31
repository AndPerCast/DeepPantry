# Machine learning models

In order to perform real-time inventory management, **DeepPantry** uses deep<br>
learning models that are specialized in **object detection** tasks. This repository<br>
already comes with ***ssd-mobilenet.onnx*** out of the box.<br>

For this project, I collected my own [dataset](https://drive.google.com/drive/folders/1nAAdmjYm_6k_V1LJ90OaN4FSZnznbGuJ?usp=sharing) in *Pascal VOC* format with images<br>
of my pantry and some food items I had around. Classification involves 5<br>
different types of objects, which I included in my *labels.txt* file:
- Cookies
- Tomato Sauce
- Champignon
- Pineapple
- Couscous

> BACKGROUND class is required, but only for ***PyTorch*** training.

I used pre-trained *[SSD Mobilenet V1](https://nvidia.box.com/shared/static/djf5w54rjvpqocsiztzaandq1m3avr7c.pth)* as a base. Then, I applied transfer learning<br>
to train my custom model using ***PyTorch*** with roughly 300 images, during 300<br>
epochs. This is the [tutorial](https://github.com/dusty-nv/jetson-inference/blob/master/docs/pytorch-collect-detection.md) I followed to do so.

Anyways, it is easy for **DeepPantry** to load your own models. Just make sure to<br>
move both ***[ONNX](https://onnx.ai)*** and ***labels*** files to this folder and adjust paths on [settings](../config/CONFIG.md).

> The very first time you import a new model can take a while, as ***[TensorRT](https://developer.nvidia.com/tensorrt)***<br>
> will optimize it to enhance inferencing performance.