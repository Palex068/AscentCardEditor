from PIL import Image, ImageFont
from PIL.ImageDraw import Draw
from constants import *



def CardTitle(image, title):

    x_limit = 445
    y_limit = 45
    fontsize = 100

    draw = Draw(image)

    font = ImageFont.truetype('fonts/Colus.ttf', fontsize)

    x, y = draw.textsize(title, font = font)
    while x > x_limit or y > y_limit:
        fontsize -= 1
        font = ImageFont.truetype('fonts/Colus.ttf', fontsize)
        x, y = draw.textsize(title, font = font)

    draw.text((160 + (x_limit - x) // 2, 52 + (y_limit - y) // 2), title, font = font)

def CardSubtype(image, subtype_index):

    x_limit = 670
    y_limit = 40
    fontsize = 100
    subtype = CARDSUBTYPES[subtype_index]

    draw = Draw(image)

    font = ImageFont.truetype('fonts/Colus.ttf', fontsize)
    x, y = draw.textsize(subtype, font = font)
    while x > x_limit or y > y_limit:
        fontsize -= 1
        font = ImageFont.truetype('fonts/Colus.ttf', fontsize)
        x, y = draw.textsize(subtype, font = font)

    draw.text((40 + (x_limit - x) // 2, 629 + (y_limit - y) // 2), subtype, font = font)

def CardCredits(image, artist):

    x_limit = 300
    y_limit = 30
    fontsize = 100
    if artist == "":
        artist = "unknown"
    artline = "Арт: " + artist + ", ТЕСТ"

    draw = Draw(image)

    font = ImageFont.truetype('fonts/Spectral-Regular.ttf', fontsize)
    x, y = draw.textsize(artline, font = font)
    while x > x_limit or y > y_limit:
        fontsize -= 1
        font = ImageFont.truetype('fonts/Spectral-Regular.ttf', fontsize)
        x, y = draw.textsize(artline, font = font)
    draw.text((217 + (x_limit - x) // 2, 935 + (y_limit - y) // 2), artline, font = font, fill = "black")

def CardCopyright(image):
    
    x_limit = 300
    y_limit = 30
    line = "Восхождение™"

    draw = Draw(image)

    font = ImageFont.truetype('fonts/Spectral-Regular.ttf', 22)
    x, y = draw.textsize(line, font = font)
    draw.text((217 + (x_limit - x) // 2, 957 + (y_limit - y) // 2), line, font = font, fill = "black")

def CardPower(image, power):
    
    x_limit = 71
    y_limit = 103
    fontsize = 40

    draw = Draw(image)

    font = ImageFont.truetype('fonts/Spectral-Regular.ttf', fontsize)
    x, y = draw.textsize(power, font = font)

    draw.text((602 + (x_limit - x) // 2, 813 + (y_limit - y) // 2), power, font = font, fill = (58, 57, 57))

def __BuildRuletext(image, words, x_limit, y_limit, fontsize):

    result = ""

    draw = Draw(image)

    for i in words:

        temp = result + i + " "

        font = ImageFont.truetype('fonts/Spectral-Regular.ttf', fontsize)
        x, y = draw.textsize(temp, font = font)
        

        if y > y_limit:
            return __BuildRuletext(image, words, x_limit, y_limit, fontsize - 1)

        if x > x_limit:
            temp = result + "\n" + i + " "

            font = ImageFont.truetype('fonts/Spectral-Regular.ttf', fontsize)
            x, y = draw.textsize(temp, font = font)

            if x > x_limit or y > y_limit:
                return __BuildRuletext(image, words, x_limit, y_limit, fontsize - 1)

        result = temp

    return result, fontsize

def CardRuletext(image, text):
    
    x_limit = 495
    y_limit = 235
    fontsize = 40
    words = text.replace('\n', ' \n').split(' ')
    result = ""

    draw = Draw(image)

    font = ImageFont.truetype('fonts/Spectral-Regular.ttf', fontsize)

    result, fontsize = __BuildRuletext(image, words, x_limit, y_limit, fontsize)

    font = ImageFont.truetype('fonts/Spectral-Regular.ttf', fontsize)

    temp = ""
    result = result.split(' ')
    result.append('')
    
        
    for i in range(len(result) - 1):
        flag = 0
        for kw in KEYWORDS:
            if kw in result[i]:
                flag = 1
        if flag == 1:
            temp += '*' + result[i] + ' '
            result[i + 1] = '!' + result[i + 1]
        else:
            temp += result[i] + ' '
    result = temp
        
    lines = result.split('\n')
    line_height = 0

    for i in range(len(lines)):
        line = lines[i]

        words = line.split(' ')
        line_weight = 0

        for j in words:
            word = j + ' '

            while '*' in word or '_' in word or '!' in word:
                flag = 0
                if word[0] == '*':
                    word = word[1:]
                    font = ImageFont.truetype('fonts/spectral/Spectral-Bold.ttf', fontsize)
                    flag = 1
                elif word[0] == '_':
                    word = word[1:]
                    font = ImageFont.truetype('fonts/spectral/Spectral-LightItalic.ttf', fontsize)
                    flag = 1
                elif word[0] == '!':
                    word = word[1:]
                    font = ImageFont.truetype('fonts/Spectral-Regular.ttf', fontsize)
                    flag = 1
                if flag == 0:
                    break
            
            match word:
                case "-- ":
                    word = "— "


            draw.text((94 + line_weight, 690 + line_height), word, font = font, fill = "black")
            line_weight += draw.textsize(word, font)[0]
            
        line_height += y_limit // len(lines) 

def CardColor(image, color_index):
    match color_index:
        case 0:
            frame = Image.open('data/FrameW.png')
        case 1:
            frame = Image.open('data/FrameB.png')
        case 2:
            frame = Image.open('data/FrameU.png')
        case 3:
            frame = Image.open('data/FrameR.png')
        case 4:
            frame = Image.open('data/FrameN.png')

    mask = Image.open('data/FrameMask.png').convert('L')
    image.paste(frame, (0, 0), mask)

def CardCost(image, cost):

    if cost == "":
        frame = Image.open('data/Coin.png')
    else:
        frame = Image.open('data/' + cost + '.png')
    mask = Image.open('data/CoinMask.png').convert('L')
    image.paste(frame, (0, 0), mask)

def CardType(image, card_type):
    match card_type:
        case 0:
            cardtype = "Unit"
        case 1:
            cardtype = "City"
        case 2:
            cardtype = "Order"
        case 3:
            cardtype = "Rite"
        case 4:
            cardtype = "Relic"

    frame = Image.open('data/' + cardtype + '.png')
    mask = Image.open('data/' + cardtype + 'Mask.png').convert('L')
    image.paste(frame, (0, 0), mask)