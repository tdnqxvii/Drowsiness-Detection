# -*- coding: utf-8 -*-
"""Gradio.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1e-RAgOvUQuBsHksxyb3nRDOOO_LW8vUy
"""

!pip install -q gradio

import gradio as gr

from keras.models import load_model
model = load_model('/content/drive/MyDrive/AI/fish_KOI.h5')

#class_names = ['Closed', 'Open', 'no_yawn', 'yawn']

class_names =['Asagi', 'Bekko', 'Difference', 'Hikarimuji mono', 'Kohaku','Sanke', 
           'Showa', 'Shusui', 'Tancho', 'Utsuri']

def predict_image(img):
  img_4d=img.reshape(-1,256,256,3)
  prediction=model.predict(img_4d).flatten()    
  return {class_names[i]: float(prediction[i]) for i in range(10)}

image = gr.inputs.Image(shape=(256,256))
label = gr.outputs.Label(num_top_classes=1)

gr.Interface(fn=predict_image, inputs=image, outputs=label).launch(debug='True')

