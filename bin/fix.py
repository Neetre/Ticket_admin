'''
element = driver.find_element_by_css_selector('#px-captcha')
action = ActionChains(driver)
click = ActionChains(driver)
action.click_and_hold(element)
action.perform()
time.sleep(10)
action.release(element)
action.perform()
time.sleep(0.2)
action.release(element)
'''

'''
url = "{Your URL}"
driver.get(url)
sleep(randint(2,3))

element = driver.find_element_by_xpath("//div[@id='px-captcha']")
# print(len(element.text), '- Value found by method text')
action = ActionChains(driver)
click = ActionChains(driver)
frame_x = element.location['x']
frame_y = element.location['y']
# print('x: ', frame_x)
# print('y: ', frame_y)
# print('size box: ', element.size)
# print('x max click: ', frame_x + element.size['width'])
# print('y max click: ', frame_y + element.size['height'])
x_move = frame_x + element.size['width']*0.5
y_move = frame_y + element.size['height']*0.5
action.move_to_element_with_offset(element, x_move, y_move).click_and_hold().perform()
time.sleep(10)
action.release(element)
action.perform()
time.sleep(0.2)
action.release(element)

'''