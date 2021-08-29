# Machine learning models

In order to perform real-time inventory management, DeepPantry uses machine<br>
learning models that are specialized in object detection tasks.

This repository already comes with *ssd-mobilenet.onnx* out of the box.<br>
For this project, ...

Anyways, it is easy for DeepPantry to load your own models. Just make sure to<br>
move both ONNX and labels file to this folder and adjust paths on [settings](../config/CONFIG.md).<br>
This is the [tutorial](https://github.com/dusty-nv/jetson-inference/blob/master/docs/pytorch-collect-detection.md) I followed to train AI.
