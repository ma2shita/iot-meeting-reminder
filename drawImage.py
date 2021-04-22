from PIL import Image, ImageDraw, ImageFont

def newImage(remind, start, event):
    img = Image.open('background2.bmp')
    img = img.resize((284, 176))
    img = img.convert(mode='1')
    draw = ImageDraw.Draw(img)

    font16 = ImageFont.truetype('Font.ttc', 16)
    font35 = ImageFont.truetype('Font.ttc', 35)

    print(len(event))
    draw.text((15, 15), event, font=font16, fill=255)
    draw.text((115, 60), remind, font=font35)
    draw.text((115, 125), start, font=font35)

    # img = img.transpose(Image.ROTATE_90)
    img = img.convert(mode='1')
    img.save('event.bmp', 'bmp')