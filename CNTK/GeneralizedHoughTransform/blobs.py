from skimage import feature, io, filters, transform

img_file = "../data/similar_objects/4.JPG"

# load the image and convert it to a floating point data type
image = io.imread(img_file)
image = transform.rescale(image, 0.4)


from matplotlib import pyplot as plt
from skimage import data
from skimage.feature import blob_dog, blob_log, blob_doh
from math import sqrt
from skimage.color import rgb2gray

image_gray = rgb2gray(image)

plt.imshow(image_gray)
plt.show()


blobs_log = blob_log(image_gray, max_sigma=30, num_sigma=10, threshold=.1)
# Compute radii in the 3rd column.
blobs_log[:, 2] = blobs_log[:, 2] * sqrt(2)


#blobs_doh = blob_doh(image_gray, max_sigma=30, threshold=.01)

blobs_list = [blobs_log]
colors = ['yellow']
titles = ['Laplacian of Gaussian']
sequence = zip(blobs_list, colors, titles)


fig,axes = plt.subplots(1, 2, sharex=True, sharey=True, subplot_kw={'adjustable':'box-forced'})
axes = axes.ravel()
for blobs, color, title in sequence:
    ax = axes[0]
    axes = axes[1:]
    ax.set_title(title)
    ax.imshow(image, interpolation='nearest')
    for blob in blobs:
        y, x, r = blob
        c = plt.Circle((x, y), 2, color=color, linewidth=2, fill=False)
        ax.add_patch(c)

plt.show()