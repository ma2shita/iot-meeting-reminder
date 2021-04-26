from PIL import Image, ImageDraw, ImageFont

def newImage(remind, start, event):
    img = Image.open('background2.bmp')
    img = img.resize((284, 176))
    img = img.convert(mode='1')
    draw = ImageDraw.Draw(img)

    font18 = ImageFont.truetype('GenShinGothic-P-Medium.ttf', 18)
    font35 = ImageFont.truetype('GenShinGothic-Monospace-Medium.ttf', 35)

    draw.text((15, 10), event, font=font18, fill=255)
    draw.text((115, 57), remind, font=font35)
    draw.text((115, 122), start, font=font35)

    # img = img.transpose(Image.ROTATE_90)
    img = img.convert(mode='1')
    img.save('event.bmp', 'bmp')

if __name__ == '__main__':
    newImage('11:45', '12:00', 'テストイベント')