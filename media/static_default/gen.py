from PIL import Image, ImageDraw, ImageFont

image_width = 100
image_height = 100
background_color = (186, 217, 255)
image = Image.new('RGBA', (image_width, image_height), background_color)

font_size = 60
font_color = (94, 167, 255) 
font_path = 'media/static_default/gen_a-z/ARLRDBD.TTF'  
font = ImageFont.truetype(font_path, font_size)

draw = ImageDraw.Draw(image)

letters = '1234567890'
for i, letter in enumerate(letters):
    image.paste(background_color, (0, 0, image_width, image_height))
    letter_width, letter_height = draw.textsize(letter, font=font)
    x = (image_width - letter_width) // 2
    y = (image_height - letter_height) // 2
    draw.text((x, y), letter, font=font, fill=font_color)
    filename = f'media/static_default/{letter}.png'
    image.save(filename)
