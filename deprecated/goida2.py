from PIL import Image
from super_image import EdsrModel, ImageLoader

path_to_image = 'processed_images\m31.png'
image = Image.open(path_to_image).convert('L')  # Преобразование изображения в черно-белое
# print(image.size)

model = EdsrModel.from_pretrained('eugenesiow/edsr-base', scale=2)  # scale 2, 3 and 4 models available
inputs = ImageLoader.load_image(image)
# print(inputs.shape)
preds = model(inputs)

ImageLoader.save_image(preds, './scaled_2x.png')  # save the output 2x scaled image to `./scaled_2x.png`
ImageLoader.save_compare(inputs, preds, './scaled_2x_compare.png')  # save an output comparing
