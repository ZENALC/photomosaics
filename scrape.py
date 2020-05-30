"""
    This code scrapes images from the website unsplash.com.
    Unsplash is a website that provides all of its images free of charge to everyone, so scraping
    images should not be an issue.

    With the chromedriver.exe provided on GitHub, it only works for Chrome Version 83. If you have another version
    of Chrome installed, you can download it at https://chromedriver.chromium.org/downloads.
"""

from selenium.common.exceptions import StaleElementReferenceException
from selenium.webdriver.common.keys import Keys
from selenium import webdriver
import urllib.request
import os


# Return a driver to use Selenium with
def create_driver():
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument("--start-maximized")
    chrome_options.add_argument("--incognito")
    return webdriver.Chrome('chromedriver.exe', options=chrome_options)


# Return a list of URLs of image sources
def scrapeImageURLs(driverArgument, pages):
    print("Scraping image URLs...")
    totalImages = set()
    for counter in range(pages):
        images = driverArgument.find_elements_by_tag_name('img')
        for image in images:
            try:
                src = image.get_attribute('src')
                if 'photo' in src and 'profile' not in src:
                    totalImages.add(src)  # scrape all photos but profile pics
            except StaleElementReferenceException:
                continue
        driverArgument.find_element_by_tag_name('body').send_keys(Keys.PAGE_DOWN, Keys.PAGE_DOWN, Keys.PAGE_DOWN)
    driverArgument.quit()

    return totalImages


# Download images provided in srcList and save them to folder
def downloadImages(srcList, arg):
    print(f"Downloading {arg} images...")
    previous_path = os.getcwd()
    folder = f'{arg.capitalize()} Images'
    if not os.path.exists(folder):
        os.mkdir(folder)
    os.chdir(folder)
    amtOfImages = len(srcList)
    counter = 0
    for index, src in enumerate(srcList):
        imageName = f'{arg}-{counter}.jpg'
        if os.path.exists(imageName):
            while os.path.exists(imageName):
                counter += 1
                imageName = f'{arg}-{counter}.jpg'
        urllib.request.urlretrieve(src, imageName)
        print(f"Downloaded {index + 1}/{amtOfImages} images.")

    os.chdir(previous_path)


def main():
    arg = 'dog'  # what to download images of
    url = f'https://unsplash.com/s/photos/{arg}'  # website url we will download from
    driver = create_driver()  # get a driver
    driver.get(url)  # connect and view website
    imgSources = scrapeImageURLs(driver, pages=5)  # scrape img URLs
    downloadImages(imgSources, arg)  # download images


if __name__ == '__main__':
    main()
