from selenium.common.exceptions import NoSuchElementException
driver = None
elementFound = False

def setDriver(d):
    global driver
    driver = d

def setByXpath(elementPath):
    '''Sets the driver to point at the first iFrame where element xPath is found'''
    global elementFound
    setFrameRecursive(elementPath)
    elementFound = False


def setFrameRecursive(elementPath):
    '''Recursively finds and sets the driver to point at the first iFrame where element xPath is found'''
    global elementFound
    if elementFound: return
    try:
        iFrames = driver.find_elements_by_tag_name('iframe')
    except NoSuchElementException:
        return
    for iFrame in iFrames:
        try:
            driver.switch_to.frame(iFrame)
        except Exception:
            return
        if checkExistsByXpath(elementPath):
            elementFound = True
            return
        else:
            currentWindow = driver.current_window_handle
            setFrameRecursive(elementPath)
            driver.switch_to.window(currentWindow)


def checkExistsByXpath(xpath):
    '''Checks if the xpath is present in current iFrame'''
    try:
        driver.find_element_by_xpath(xpath)
    except NoSuchElementException:
        return False
    return True