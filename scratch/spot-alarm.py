#!/usr/bin/python
import time
from splinter import Browser
browser = Browser('phantomjs')
# browser = Browser()
browser.visit('file:///home/ethompsy/Projects/spot/html/spotify_test.html')
print browser.url
print browser.html
with browser.get_iframe('player') as iframe:
	iframe.is_element_present_by_id('play-button', wait_time=10)
	print iframe.find_by_id('play-button').first
	iframe.find_by_id('play-button').first.click()
time.sleep(5)
browser.quit()
