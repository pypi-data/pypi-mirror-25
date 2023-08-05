""" CNN 16-layer neural net that generalizes well from 1000 cat images

- uses the bottleneck features of a pre-trained VGG16 network
- customizes the top layers of the pre-trained VGG16 network

References:
  [keras blog](https://blog.keras.io/building-powerful-image-classification-models-using-very-little-data.html)
  [code for keras blog](https://gist.github.com/fchollet/f35fbc80e066a49d65f1688a7e99f069)
  [weights for pretrained VGG16](https://gist.github.com/baraldilorenzo/07d7802847aaad0a35d3)
  [more labeled images](https://www.flickr.com/services/api/)
  [cats and dogs images on kaggle](https://www.kaggle.com/c/dogs-vs-cats/data)
  [image net images of more objects](http://image-net.org/download)
"""
import os

from keras.preprocessing.image import ImageDataGenerator
from keras.preprocessing.image import load_img, img_to_array  # , array_to_img

import labeler_site.settings

BASE_DIR = labeler_site.settings.BASE_DIR


# datagen = ImageDataGenerator(
#         rotation_range=40,
#         width_shift_range=0.2,
#         height_shift_range=0.2,
#         rescale=1./255,
#         shear_range=0.2,
#         zoom_range=0.2,
#         horizontal_flip=True,
#         fill_mode='nearest')


datagen = ImageDataGenerator(
    rotation_range=180,
    width_shift_range=0.2,
    height_shift_range=0.2,
    shear_range=0.2,
    zoom_range=0.2,
    horizontal_flip=True,
    fill_mode='nearest')


image_path = os.path.join(BASE_DIR, *('user_uploads images HUNT0133.jpg'.split()))
img = load_img(image_path)  # this is a PIL image
x = img_to_array(img)  # this is a Numpy array with shape (3, 150, 150)
x = x.reshape((1,) + x.shape)  # this is a Numpy array with shape (1, 3, 150, 150)

# the .flow() command below generates batches of randomly transformed images
# and saves the results to the `preview/` directory
i = 0
preview_path = os.path.join(BASE_DIR, *('user_uploads images preview'.split()))
for batch in datagen.flow(x, batch_size=1,
                          save_to_dir=preview_path, save_prefix='HUNT0133', save_format='jpeg'):
    i += 1
    if i > 20:
        break  # otherwise the generator would loop indefinitely
