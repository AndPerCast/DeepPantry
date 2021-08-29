# Machine learning models

In order to perform real-time inventory management, **DeepPantry** uses deep<br>
learning models that are specialized in **object detection** tasks. This repository<br>
already comes with ***ssd-mobilenet.onnx*** out of the box.<br>

For this project, I collected my own dataset in *Pascal VOC* format with images<br>
of my pantry and some food items I had around. Classification involves 5<br>
different types of objects:
- Cookies
- Tomato Sauce
- Champignon
- Pineapple
- Couscous

I used pre-trained *[SSD Mobilenet V1](https://nvidia.box.com/shared/static/djf5w54rjvpqocsiztzaandq1m3avr7c.pth)* as a base. Then, I applied transfer learning<br>
to train my custom model using ***PyTorch*** with roughly 300 images, during 300<br>
epochs. This is the [tutorial](https://github.com/dusty-nv/jetson-inference/blob/master/docs/pytorch-collect-detection.md) I followed to do so.

Anyways, it is easy for **DeepPantry** to load your own models. Just make sure to<br>
move both ***ONNX*** and ***labels*** files to this folder and adjust paths on [settings](../config/CONFIG.md).

> The very first time you import a new model can take a while, as ***[TensorRT](https://developer.nvidia.com/tensorrt)***<br>
> will optimize it to enhance inferencing performance.