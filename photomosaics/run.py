from photomosaics import PhotoMosaic
import argparse


def main():
    parser = argparse.ArgumentParser(description='Convert an image to a photo mosaic.')
    parser.add_argument('imagePath', type=str, help='path to image file that will be converted')
    parser.add_argument('imagesFolder', type=str, help='path to folder with images that will be used for photo mosaic')
    parser.add_argument('--baseWidth', type=int, help='target width for photo mosaic',
                        nargs=1, default=[5000])
    parser.add_argument('--step', type=int, help='height and width of sub-image in photo mosaic',
                        nargs=1, default=[100])
    args = parser.parse_args()

    PhotoMosaic(args.imagePath, args.imagesFolder, args.step[0], args.baseWidth[0]).save_image()


if __name__ == '__main__':
    main()
