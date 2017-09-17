from skimage import feature, io, filters, transform, segmentation
import matplotlib.pyplot as plt


img_file = "../data/similar_objects/4.JPG"

# load the image and convert it to a floating point data type
image = io.imread(img_file)
image = transform.rescale(image, 0.1)

segm_f = segmentation.quickshift(image)
plt.imshow(segm_f)
plt.show()