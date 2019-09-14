# -*- coding: utf-8 -*-
"""modelo_pix2pix.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/107OYvVrU5E9L-CTeGW-kKZYzwN_Yktqo
"""

# Commented out IPython magic to ensure Python compatibility.
# %tensorflow_version 2.x

from google.colab import drive
drive.mount('/content/drive')

from __future__ import absolute_import, division, print_function, unicode_literals

try:
  # %tensorflow_version only exists in Colab.
  !pip install tf-nightly-gpu-2.0-preview
except Exception:
  pass
import tensorflow as tf

import os
import time
import numpy as np
import matplotlib.pyplot as plt
from IPython.display import clear_output

#ruta
PATH ="/content/drive/My Drive/Dataset2"
#ruta de datos de entrada
INPATH = PATH + '/input'
#ruta de datos de salida
OUPATH = PATH + '/output'
#ruta de datos de checkpoints
CKPATH = PATH + '/checkpoints'

imgurls = !ls -1 "{INPATH}"

n = 50
train_n = round(n*0.90)

#Listado mesclado
randurls = np.copy(imgurls)
np.random.seed()
np.random.shuffle(randurls)

#Particion train/test.
tr_urls = randurls[:train_n]
ts_urls = randurls[train_n:n]
print(len(imgurls), len(tr_urls), len(ts_urls))

IMG_WIDTH = 256
IMG_HEIGHT = 256

#Reescalar imagenes

def resize(inimg, tgimg, height, width):
  inimg = tf.image.resize(inimg, [height, width])
  tgimg = tf.image.resize(tgimg, [height, width])
  return inimg, tgimg

# Normaliza al rango[-1, +1] la imagen.

def normalize(inimg, tgimg):
  inimg = (inimg / 127.5) - 1
  tgimg = (tgimg / 127.5) - 1
  return inimg, tgimg

#@tf.function
def random_jitter(inimg, tgimg):
  
  inimg, tgimg = resize(inimg, tgimg, 286, 286)
  
  stacked_image = tf.stack([inimg, tgimg], axis=0)
  cropped_image = tf.image.random_crop(stacked_image,size = [2, IMG_HEIGHT, IMG_WIDTH, 3])
  
  inimg, tgimg = cropped_image[0], cropped_image[1]
  
  if tf.random.uniform(()) > 0.5:
    
    inimg = tf.image.flip_left_right(inimg)
    tgimg = tf.image.flip_left_right(tgimg)
    
  return inimg, tgimg

#Aumentacion de datos : Random crop + flip.


def load_image(filename, augment = True):
  
  inimg = tf.cast(tf.image.decode_jpeg(tf.io.read_file(INPATH + '/'+filename)), tf.float32)[..., :3]
  tgimg = tf.cast(tf.image.decode_jpeg(tf.io.read_file(OUPATH + '/'+filename)), tf.float32)[..., :3]
  
  inimg , tgimg = resize(inimg, tgimg, IMG_HEIGHT, IMG_WIDTH)
  
  if augment:
    inimg, tgimg = random_jitter(inimg, tgimg)
  
  inimg, tgimg = normalize(inimg, tgimg)
  
  return inimg, tgimg

def load_train_image(filename):
  return load_image(filename, True)

def load_test_image(filename):
  return load_image(filename, False)

plt.imshow(((load_test_image(randurls[0])[0])+1)/2)

train_dataset = tf.data.Dataset.from_tensor_slices(tr_urls)
train_dataset = train_dataset.map(load_train_image, num_parallel_calls = tf.data.experimental.AUTOTUNE)
train_dataset = train_dataset.batch(1)

test_dataset  = tf.data.Dataset.from_tensor_slices(ts_urls)
test_dataset  = test_dataset.map( load_test_image, num_parallel_calls = tf.data.experimental.AUTOTUNE)
test_dataset  = test_dataset.batch(1)

from tensorflow.keras import *
from tensorflow.keras.layers import *

def downsample(filters, apply_batchnorm=True):
  result = Sequential()
  initializer = tf.random_normal_initializer(0, 0.02)
  
  #Capa convolucional.
  result.add(Conv2D(filters,
                   kernel_size=4,
                   strides=2,
                   padding="same",
                   kernel_initializer=initializer,
                   use_bias=not apply_batchnorm))
  if apply_batchnorm:
    #Capa de BatchNorm.
    result.add(BatchNormalization())
    
  #capa de activacion.
  result.add(LeakyReLU())
  
  return result

downsample(64)

def upsample(filters, apply_dropout=False):
  result = Sequential()
  initializer = tf.random_normal_initializer(0, 0.02)
  
  #Capa convolucional.
  result.add(Conv2DTranspose(filters,
                             kernel_size=4,
                             strides=2,
                             padding="same",
                             kernel_initializer=initializer,
                             use_bias=False))
  result.add(BatchNormalization())
  
  if apply_dropout:
    #Capa de BatchNorm.
    result.add(Dropout(0.5))
    
  #capa de activacion.
  result.add(ReLU())
  
  return result

upsample(64)

loss_object = tf.keras.losses.BinaryCrossentropy(from_logits = True)

def Generator():
  
  inputs = tf.keras.layers.Input(shape=[None,None,3])
  down_stack = [
    downsample(64, apply_batchnorm=False), # (bs, 128, 128, 64)
    downsample(128), # (bs, 64, 64, 128)
    downsample(256), # (bs, 32, 32, 256)
    downsample(512), # (bs, 16, 16, 512)
    downsample(512), # (bs, 8, 8, 512)
    downsample(512), # (bs, 4, 4, 512)
    downsample(512), # (bs, 2, 2, 512)
    downsample(512), # (bs, 1, 1, 512)
  ]

  up_stack = [
    upsample(512, apply_dropout=True), # (bs, 2, 2, 1024)
    upsample(512, apply_dropout=True), # (bs, 4, 4, 1024)
    upsample(512, apply_dropout=True), # (bs, 8, 8, 1024)
    upsample(512), # (bs, 16, 16, 1024)
    upsample(256), # (bs, 32, 32, 512)
    upsample(128), # (bs, 64, 64, 256)
    upsample(64), # (bs, 128, 128, 128)
  ]
  
  initializer = tf.random_normal_initializer(0, 0.02)
  last = Conv2DTranspose(filters = 3,
                         kernel_size = 4,
                         strides=2,
                         padding='same',
                         kernel_initializer=initializer,
                         activation='tanh') # (bs, 256, 256, 3)

  concat = tf.keras.layers.Concatenate()

  
  x = inputs
  s = []
  concat = Concatenate()
  
  for down in down_stack:
    x = down(x)
    s.append(x)

  s = reversed(s[:-1])

  # Upsampling and establishing the skip connections
  for up, sk in zip(up_stack, s):
    x = up(x)
    x = concat([x, sk])

  last = last(x)

  return Model(inputs=inputs, outputs=last)

generator = Generator()

def Discriminator():
  
  ini = Input(shape=[None, None, 3], name="input_img")
  gen = Input(shape=[None, None, 3], name="gener_img")
  
  con = concatenate([ini, gen])
  
  initializer = tf.random_normal_initializer(0, 0.02)
  
  down1 = downsample(64, apply_batchnorm=False)(con)
  down2 = downsample(128)(down1)
  down3 = downsample(256)(down2)
  down4 = downsample(512)(down3)
  
  last = tf.keras.layers.Conv2D(filters=1,
                              kernel_size=4,
                              strides=1,
                              kernel_initializer=initializer,
                              padding="same")(down4)
  return tf.keras.Model(inputs=[ini, gen],outputs=last)

discriminator= Discriminator()

#disc_out = discriminator([((inimg+1)*255), gen_output], training=False)
#plt.imshow(disc_out[0,...,-1], vmin=-20, vmax=20, cmap = 'RdBu_r')
#plt.colorbar()
#disc_out.shape

def discriminator_loss(disc_real_output,disc_generated_output):
   
  real_loss = loss_object(tf.ones_like(disc_real_output), disc_real_output)
  
  generated_loss = loss_object(tf.zeros_like(disc_generated_output), disc_generated_output)
  
  total_disc_loss = real_loss + generated_loss
  
  return total_disc_loss

LAMBDA = 100
def generator_loss(disc_generated_output, gen_output, target):
  gan_loss = loss_object(tf.ones_like(disc_generated_output), disc_generated_output)
  l1_loss = tf.reduce_mean(tf.abs(target - gen_output))
  total_gen_loss = gan_loss + (LAMBDA * l1_loss)
  return total_gen_loss

import os
generator_optimizer     = tf.keras.optimizers.Adam(2e-4, beta_1 = 0.5)
discriminator_optimizer = tf.keras.optimizers.Adam(2e-4, beta_1 = 0.5)

checkpoint_prefix = os.path.join(CKPATH, "ckpt")
checkpoint = tf.train.Checkpoint(generator_optimizer = generator_optimizer,
                                discriminator_optimizer = discriminator_optimizer,
                                generator = generator,
                                discriminator = discriminator)
checkpoint.restore(tf.train.latest_checkpoint(CKPATH))#.assert_consumed()

def generate_images(model,test_input, tar,save_filename=False,display_imgs=True):
  prediction = model(test_input, training=True)
  
  if save_filename:
    tf.keras.preprocessing.image.save_img(PATH + '/outputB/' + save_filename + '.jpg', prediction[0,...])
  plt.figure(figsize=(10,10))
  
  display_list = [test_input[0], tar[0], prediction[0]]
  title = ['Input Image', 'Ground Truth', 'Predicted Image']
  
  if display_imgs:
    for i in range(3):
      plt.subplot(1,3, i+1)
      plt.title(title[i])
      plt.imshow(display_list[i] * 0.5 + 0.5)
      plt.axis('off')
  plt.show()

from IPython.display import clear_output
def train(dataset, epochs):
  for epoch in range(epochs):
    imgi = 0
    for input_image, target in dataset:
      print('epoch' + str(epoch) + ' - train: ' + str(imgi) + '/'+str(len(tr_urls)))
      imgi+=1
      train_step(input_image, target)
    
      clear_output(wait=True)
    imgi = 0
    for inp, tar in test_dataset.take(5):
      generate_images(generator, inp, tar, str(imgi) + '_' + str(epoch), display_imgs=True)
      imgi += 1
    if ( epoch + 1)%50 ==0:
      checkpoint.save(file_prefix = checkpoint_prefix)

@tf.function()
def train_step(input_image, target):
  
  with tf.GradientTape() as gen_tape, tf.GradientTape() as discr_tape:
    
    output_image = generator(input_image, training = True)
    
    output_gen_discr = discriminator([output_image, input_image], training = True)
    
    output_trg_discr = discriminator([target, input_image], training = True)
    
    discr_loss = discriminator_loss(output_trg_discr, output_gen_discr)
    
    gen_loss = generator_loss(output_gen_discr, output_image, target)
    
    
    generator_grads = gen_tape.gradient(gen_loss, generator.trainable_variables)
    
    discriminator_grads = discr_tape.gradient(discr_loss, discriminator.trainable_variables)
    
    generator_optimizer.apply_gradients(zip(generator_grads, generator.trainable_variables))
    
    discriminator_optimizer.apply_gradients(zip(discriminator_grads, discriminator.trainable_variables))
# Run the trained model on the entire test dataset
num=0
for inp, tar in test_dataset.take(5):
  #generate_images(generator, inp, tar)
  num +=1
  generate_images(generator, inp, tar, str(num) , display_imgs=True)
#train(train_dataset, 100)
