from psychopy import visual, event, core
from psychopy.hardware import keyboard
from random import uniform

def newText(win, name, text, height=0.035, pos=(0, 0)):
    return visual.TextStim(win=win, name=name,
        text=text, font='Arial', pos=pos, height=height, wrapWidth=None, ori=0.0, 
        color='white', colorSpace='rgb', opacity=None, languageStyle='LTR', depth=0.0)
def newKey(keyList=None, maxWait=float('inf')):
    #print(f"newKey(keyList={keyList},maxWait={maxWait})")
    key = None
    if keyList is None:
        key = event.waitKeys(maxWait=maxWait)
    else:
        if 'escape' not in keyList:
            keyList.append('escape')
        key = event.waitKeys(keyList=keyList,maxWait=maxWait)
    if key is not None and 'escape' in key:
        core.quit()
    return key
def timedKey(callback, keyList=None, maxWait=4.0):
    remainder = maxWait
    clock = core.getTime()
    key = event.waitKeys(keyList=keyList, maxWait=remainder)
    pressTime = float('inf')
    if key is not None:
        pressTime = core.getTime() - clock
        callback()
    else:
        return None
    remainder = maxWait - pressTime
    core.wait(remainder)
    return key, pressTime
def newImage(win, image=None, zoom=1.0, pos=(0, 0.2)):
    image = visual.ImageStim(
        win=win,
        name='image', units='norm', 
        image=image, mask=None,
        ori=0, pos=pos, size=None,
        color=[1,1,1], colorSpace='rgb', opacity=1,
        flipHoriz=False, flipVert=False,
        texRes=512, interpolate=True, depth=0.0)
    sz = image.size
    image.setSize((sz[0] * zoom, sz[1] * zoom))
    return image
def newInstruction(win, name, row, keyList=None):
    inst1 = newText(win, name, row[name])
    inst1.draw()
    win.flip()
    newKey(keyList=keyList)
def newCross(win, wait_time=0.3):
    cross = visual.ShapeStim(
        win=win, name='fixationcross', vertices='cross',
        size=(0.035, 0.035),
        ori=0.0, pos=(0, 0),
        lineWidth=1.0,     colorSpace='rgb',  lineColor='white', fillColor='white',
        opacity=None, depth=0.0, interpolate=True)
    cross.draw()
    win.flip()
    #wait_time = uniform(0.3, 0.5)
    core.wait(wait_time)
def showImage(win, img_path, wait_time, rating, keyList=['1','2','3','4','5'], pos=(0, 0.2), ref_image=None, ref_image_pos=(-0.35, 0.2),zoom=0.7):
    image = newImage(win, image=img_path, zoom=zoom, pos=pos)
    rating = newText(win, "rating", rating, pos=(0, -0.2))
    image.draw()
    rating.draw()
    if ref_image:
        ref_image = newImage(win, image=ref_image, zoom=zoom, pos=ref_image_pos)
        ref_image.draw()
    win.flip()
    def disableRating():
        image.draw()
        if ref_image:
            ref_image.draw()
        win.flip()
    return timedKey(disableRating, keyList=keyList,maxWait=wait_time)