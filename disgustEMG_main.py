import os
from random import shuffle
from psychopy import visual, core, gui, event

# need a way of writing the block order to the file easily?

# working directories etc
wd = os.getcwd()
imgs = os.path.join(wd, 'imgs\\')

info = {}
info['participant'] = os.listdir(imgs)
info['age'] = ''
dlg = gui.DlgFromDict(info)
if not dlg.OK:  # did they push ok?
    core.quit()

age = info['age']

personalImgDir = os.path.join(imgs, (info['participant'] + '\\'))
perImgLst = os.listdir(personalImgDir)
perImgLst

if os.path.isdir('./data'):
    print('Data Directory Exists, Passing...')
    pass
else:
    print('Data Directory Does Not Exist, Creating...')
    os.mkdir('./data')

dataDir = os.path.join(wd, 'data')

# Data
data = open(str(dataDir + '\\' + info['participant'] + '.txt'), 'w')

data.write(('Participant:\t{}\nAge:\t{}\n\n').format(info['participant'], age))

# This needs to be here becasue the order needs to be written at the top of the file
blockIndictator = [('A', '30'),
                   ('B', '50'),
                   ('C', '70'),
                   ('D', '90')]
shuffle(blockIndictator)

blocks = [x[1] for x in blockIndictator]
blockText = ', '.join(blocks)
data.write('Block Order:\t{}\n\n'.format(blockText))

headers = 'Block\tImage\tRating\tRT\n'
data.write(headers)

# Psychopy objects
win = visual.Window((1280, 1024), color='black', fullscr=False)

fix = visual.TextStim(win, color='white', text='+')

instructStim = visual.TextStim(win, color='white', text='')

faceStim = visual.ImageStim(win, size=(675, 900), pos=(0, 160))

questStim = visual.TextStim(win, color='white',
                            text='How would you feel about passionately kissing this person?',
                            pos=(0, -300),
                            wrapWidth=2000)

ratingStim = visual.RatingScale(win,
                                choices=None,
                                labels=['Excited', 'Neutral', 'Disgusted'],
                                precision=1,
                                low=1,
                                high=7,
                                scale=None,
                                marker='triangle',
                                singleClick=True,
                                pos=(0, -350),
                                textColor='white',
                                mouseOnly=True,
                                stretch=2.0,
                                textSize=0.7,
                                tickHeight=0.0,
                                showAccept=False,
                                markerColor='#48d1cc')

blockLetter = visual.TextStim(win, color='white', pos=(550, 350))

instructions = '''You will be presented with a face, and then a question about that face.
Please use the mouse to answer the question. You will see a number of faces, some may look very similar, but all are different.
Press Space to start.'''

breakText = 'Please take a short break'

# Trial run time

instructStim.text = instructions
instructStim.draw()
win.flip()
event.waitKeys(keyList=['space'])

for block in blockIndictator:
    blockCode = block[0]
    blockName = block[1]

    blockLetter.text = blockCode
    blockLetter.draw()
    win.flip()
    event.waitKeys(keyList=['space'])

    imgPath = os.path.join(personalImgDir, '{}\\'.format(block[1]))
    # imgPath = str(personalImgDir + '\\' + block[1] + '\\')

    faces = [x for x in (os.listdir(imgPath)) if '.png' in x]
    shuffle(faces)

    for face in faces:

        faceStim.image = str(imgPath + face)
        print(faceStim.size)
        # Draw fixation
        for frameN in range(120):
            fix.draw()
            win.flip()

        # Draw rating
        while ratingStim.noResponse:
            faceStim.draw()
            questStim.draw()
            ratingStim.draw()
            win.flip()

        rating = ratingStim.getRating()
        rt = ratingStim.getRT()

        # Log Data
        data.write('{}\t{}\t{}\t{}\n'.format(blockName,
                                             face,
                                             rating,
                                             rt))

        ratingStim.reset()

    instructStim.text = breakText
    instructStim.draw()
    blockLetter.draw()
    win.flip()
    event.waitKeys(keyList=['space', 'escape'])

instructStim.text = 'Ta!'
for frameN in range(120):
    instructStim.draw()
    win.flip()

win.close()
data.close()
core.quit()
