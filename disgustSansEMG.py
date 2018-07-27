from psychopy import visual, core, event, gui
from random import shuffle
import os



def sassyGob(lst, format='png'):
    '''Returns a list of files if passed a file list'''
    return [x for x in (os.listdir(lst)) if format in x]


# # -- ## Working Directories ## -- ##

wd = os.getcwd()
imgs = os.path.join(wd, 'imgs\\')

info = {}
info['Participant'] = os.listdir(imgs)
dlg = gui.DlgFromDict(info)
if not dlg.OK:  # did they push ok?
    core.quit()

imgMainPth = os.path.join(imgs, '{}\\'.format(info['Participant']))

pairs = [('30', '50'),
         ('30', '70'),
         ('30', '90'),
         ('50', '70'),
         ('50', '90'),
         ('70', '90')]
# shuffle(pairs)

# # -- ## Data ## -- ##

if os.path.isdir('./No_EMG_data'):
    print('Data Directory Exists, Passing...')
    pass
else:
    print('Data Directory Does Not Exist, Creating...')
    os.mkdir('./No_EMG_Data')

dataDir = os.path.join(wd, 'No_EMG_Data')

data = open(str(dataDir + '\\' + info['Participant'] + '.txt'), 'w')

data.write('Participant:\t{}\n\n'.format(info['Participant']))

blocks = [str(x) for x in pairs]
blockText = ', '.join(blocks)

data.write('Block Order:\t{}\n\n'.format(blockText))

data.write('trialN\timgL_%\timgR_%\timg\tresp\tselection\tRT\n')

# # -- ## PsychoPy Stuff ## -- ##

win = visual.Window((1280, 1024), fullscr=False, color='black', units='pix')

imgL = visual.ImageStim(win, pos=(-300, 75), size=(675, 900))
imgR = visual.ImageStim(win, pos=(300, 75), size=(675, 900))

z = visual.TextStim(win, text='z', color='white', pos=(-300, -390), height=75)
m = visual.TextStim(win, text='m', color='white', pos=(300, -390), height=75)

instructionStim = visual.TextStim(win, color='white', text='', wrapWidth=1000)

rtClock = core.Clock()

fix = visual.TextStim(win, text='+', color='white')

mainInstruct = 'Main Study Instructions'

# # -- ## Trial Runtime ## -- ##

fiveMinTimer = core.CountdownTimer(300)

questionText = 'For the following images, please indicate which face you would prefer to passionately kiss\n\nPress space to continue'
instructionStim.text = questionText
instructionStim.draw()
win.flip()
event.waitKeys()

# pair
trialN = 1
for imageList in pairs:

    pth1 = os.path.join(imgMainPth, str(imageList[0] + '\\'))
    pth2 = os.path.join(imgMainPth, str(imageList[1] + '\\'))

    imgList1 = sassyGob(pth1)
    # print imgList1
    imgList2 = sassyGob(pth2)
    # print imgList2

    zippedImages = list(zip(imgList1, imgList2))
    shuffle(zippedImages)
    print(zippedImages)

    counter = 1
    for imagePair in zippedImages:

        print(imagePair[0], 'Pair 1')
        print(imagePair[1], 'Pair 2')

        if fiveMinTimer.getTime() <= 0:
            instructionStim.text = 'Take a break, press space when ready'
            instructionStim.draw()
            win.flip()
            event.waitKeys(keyList=['space'])
            fiveMinTimer.reset()

        if counter % 2 == 0:
            leftSim = imageList[0]
            rightSim = imageList[1]
            imgL.image = str(pth1 + imagePair[0])
            imgR.image = str(pth2 + imagePair[1])
            counter += 1
        else:
            leftSim = imageList[1]
            rightSim = imageList[0]
            imgL.image = str(pth2 + imagePair[1])
            imgR.image = str(pth1 + imagePair[0])
            counter += 1

        for frameN in range(30):
            fix.draw()
            win.flip()

        win.callOnFlip(rtClock.reset)
        imgL.draw()
        imgR.draw()
        z.draw()
        m.draw()
        win.flip()
        keys = event.waitKeys(keyList=['z', 'm'])

        resp = keys[0]

        if resp == 'z':
            answer = leftSim
        elif resp == 'm':
            answer = rightSim
        else:
            answer = 'WTF'

        rt = rtClock.getTime()

        data.write('{}\t{}\t{}\t{}\t{}\t{}\n'.format(trialN, leftSim,
                                                     rightSim, imagePair[0],
                                                     resp, answer, rt))
        trialN += 1

data.close()
win.close()
core.quit()

# imageList
data.write('trialN\timgL_%\timgR_%\timg\tresp\tselection\tRT\n')
