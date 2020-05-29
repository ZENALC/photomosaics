from PIL import Image
import os
import math


# return average RGB tuple from a list of given RGB values
def get_average(flatList):
    r, g, b = 0, 0, 0
    length = len(flatList)
    for elem in flatList:
        r += elem[0]
        g += elem[1]
        b += elem[2]
    r = r / length
    g = g / length
    b = b / length
    return r, g, b


# return an Image object
def get_image(path, dimension=None):
    image = Image.open(path)  # open Image using path
    if dimension:  # if some dimension is given, then resize it
        image.thumbnail(dimension)

    if image.mode == 'P':  # if transparent, convert to RGBA
        image = image.convert('RGBA')
    else:  # else force convert to RGB
        image = image.convert('RGB')

    return image


# crop center of image - copied from Pillow documentation
def crop_center(pil_img, crop_width, crop_height):
    img_width, img_height = pil_img.size
    return pil_img.crop(((img_width - crop_width) // 2,
                         (img_height - crop_height) // 2,
                         (img_width + crop_width) // 2,
                         (img_height + crop_height) // 2))
    

# load all objects in given path and return dictionary containing them
def load_images(path, dimension=None):
    imagesDictionary = {}
    previous_path = os.getcwd()
    os.chdir(path)
    for file in os.listdir():
        image = get_image(file, dimension=dimension)
        width, height = image.size
        if width != height:
            toCrop = min((width, height))
            image = crop_center(image, toCrop, toCrop)
        pixels = list(image.getdata())
        average = get_average(pixels)
        imagesDictionary[average] = image

    os.chdir(previous_path)
    return imagesDictionary


# return euclidean distance between two RGB tuples
def euclidean_distance(l1, l2):
    r = (l1[0] - l2[0]) ** 2
    g = (l1[1] - l2[1]) ** 2
    b = (l1[2] - l2[2]) ** 2
    return math.sqrt((r + g + b))


# return best possible image from imageDict that matches rgbTuple based on euclidean distance
def best_match(rgbTuple, imageDict):
    bestDistance = None
    bestMatch = None
    for otherTuple in imageDict.keys():
        currentDistance = euclidean_distance(rgbTuple, otherTuple)
        if not bestDistance or currentDistance < bestDistance:
            bestDistance = currentDistance
            bestMatch = otherTuple
    return imageDict[bestMatch]


# return a manipulated image with mosaic implemented
def photo_mosaic(imagePath, imageDict, step):
    image = get_image(imagePath)  # load main image to make photo mosaic
    width, height = image.size  # get width and height
    pixels = list(image.getdata())  # get list of RGB values from image
    matrix = [[pixels[width * y + x] for x in range(width)] for y in range(height)]  # get 2D array of RGB values

    editedImage = Image.new(image.mode, (width, height))  # instantiate new image
    for y in range(0, height, step):  # loop over rows incrementing by step
        y2 = y + step if y + step < height else height  # make end point y + step is not over height, else height
        for x in range(0, width, step):  # loop over columns until exhaustion
            x2 = x + step if x + step < width else width  # make end point x + step is not over width, else width
            subList = []  # instantiate new list to append subMatrix values to
            for z in range(y, y2):  # loop over subMatrix
                subMatrix = matrix[z][x:x2]
                subList.append(subMatrix)
            flat_list = [rgbTuple for elem in subList for rgbTuple in elem]  # flatten list
            average = get_average(flat_list)  # get average RGB tuple
            img = best_match(average, imageDict)  # find best matching image
            editedImage.paste(img, (x, y))  # paste image to x, y coordinate
    return editedImage


def save_image(image, imageFile):
    folderName = "Photo Mosaics"
    if not os.path.exists(folderName):
        os.mkdir(folderName)

    previous_path = os.getcwd()
    os.chdir(folderName)

    name, ext = imageFile.split('.')
    counter = 0

    output_image = f"{name}-mosaic.{ext}"
    if os.path.exists(output_image):
        while os.path.exists(output_image):
            output_image = f"{name}-mosaic{counter}.{ext}"
            counter += 1

    path = os.path.join(os.getcwd(), output_image)
    image.save(path)
    print(f"Photo mosaic has been successfully saved to {path}.")
    os.chdir(previous_path)


def main():
    step = 15  # how many pixels we'll jump over
    imageDict = load_images('imgs', dimension=(step, step))  # load images to paste on
    imageFile = 'monkey.jpg'  # image we'll be making a photo mosaic out of
    editedImage = photo_mosaic(imageFile, imageDict=imageDict, step=step)  # get a photo mosaic
    # editedImage.show()  # view image
    save_image(editedImage, imageFile)  # save image


if __name__ == "__main__":
    main()
