import logging
import platform
from selenium import webdriver

logger = logging.getLogger("Video Stream")
fireFoxOptions = webdriver.FirefoxOptions()
fireFoxOptions.set_headless()
driver = webdriver.Firefox(firefox_options=fireFoxOptions)

def start():
    videoHtml = None
    with open("res/video.html", "r") as videoHtmlFile:
        videoHtml = videoHtmlFile.read()
    print(videoHtml)
