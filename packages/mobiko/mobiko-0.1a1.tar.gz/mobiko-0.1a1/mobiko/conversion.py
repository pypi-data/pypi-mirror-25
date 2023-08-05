from PIL import Image


def scale(image, size):
	new_image = image.thumbnail((size, size), Image.ANTIALIAS)
	return new_image
