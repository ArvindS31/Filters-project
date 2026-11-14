from PIL import Image, ImageFilter
from math import floor
from random import randint, uniform
import random
from time import sleep
       
def check_max(pixel):
    pixel = list(pixel)
    if pixel[0]>255:
        pixel[0] = 255
    if pixel[1]>255:
        pixel[1] = 255
    if pixel[2]>255:
        pixel[2] = 255
       
    if pixel[0]<0:
        pixel[0] = 0
    if pixel[1]<0:
        pixel[1] = 0
    if pixel[2]<0:
        pixel[2] = 0
    return tuple(pixel)

def checkered_flag(image, image_pixels, edit, num_squares):
    side_length = max(image.height, image.width)//num_squares

    excess_height = image.height % side_length
    excess_width = image.width % side_length
   
    for y in range(floor(0.5*excess_height),floor(image.height-0.5*excess_height)):
        for x in range(floor(0.5*excess_width),floor(image.width-0.5*excess_width)):
            pixel = image_pixels[x,y]
            colomb = ((x-excess_width//2)//side_length) #find the colomb its in
            row = ((y-excess_height//2)//side_length) #find the row its in
            if (colomb+row)%2 == 1:
                coulor = 'black'
                pixel = (round(pixel[0]*0.8),round(pixel[1]*0.8),round(pixel[2]*0.8))
                pixel = check_max(pixel)
            else:
                coulor = 'white'
                pixel = (round(pixel[0]*1.2),round(pixel[1]*1.2),round(pixel[2]*1.2))
                pixel = check_max(pixel)
            edit.append(pixel)
    new_size = (image.width-excess_width,image.height-excess_height)
    new_image = Image.new('RGB', new_size)
    new_image.putdata(edit)  
    return new_image      

def old_paper(image, image_pixels, edit):
    for y in range(image.height):
        for x in range(image.width):
            pixel = image_pixels[x,y]
            avg = sum(pixel)//3
            pixel = (avg,avg,avg)
            if randint(0,1) == 0:
                grain_level = uniform(0.00,1.00)
                gray = 255*grain_level
                pixel = (round((pixel[0]+gray)/2),round((pixel[1]+gray)/2),round((pixel[2]+gray)/2))
            pixel = (round(pixel[0]*1.3),pixel[1],round(pixel[2]*0.6))
            check_max(pixel)
            edit.append(pixel)
    new_image = Image.new('RGB', image.size)
    new_image.putdata(edit)
    return new_image

def warm(image, amount):  # 20 for amount works well - maybe ask user for amount 15-25 or 10-30
   pixels = image.load()
   edited_pixels = []

   for y in range(image.height):
       for x in range(image.width):
           r, g, b = pixels[x, y]
           r = max(0, min(255, r + amount))
           g = max(0, min(255, g + amount // 2))
           b = max(0, min(255, b - amount // 2))
           pixel = (r,g,b)
           pixel = check_max(pixel)
           edited_pixels.append(pixel)

   edited_image = Image.new("RGB", image.size)
   edited_image.putdata(edited_pixels)
   return edited_image

def noise(image, amount):  # 50 for amount works well
   pixels = image.load()
   edited_pixels = []

   for y in range(image.height):
       for x in range(image.width):
           r, g, b = pixels[x, y]
           pixel = pixels[x,y]
           if random.randint(0, 1) == 1:
               r = max(0, min(255, r + amount))
               g = max(0, min(255, g + amount))
               b = max(0, min(255, b + amount))
               pixel = (r,g,b)
               pixel = check_max(pixel)
               edited_pixels.append(pixel)
           else:
               edited_pixels.append((r,g,b))
   edited_image = Image.new("RGB", image.size)
   edited_image.putdata(edited_pixels)
   return edited_image

def vintage_film(image, warmth, grain):  # 20 warmth and 50 grain works well
   return noise(warm(image, warmth), grain)

def contrast(image, amount):  # 10-20 for amount works well
   pixels = image.load()
   edited_pixels = []
   for y in range(image.height):
       for x in range(image.width):
           r, g, b = pixels[x, y]
           if r < 128:
               r = max(0, r - amount)
           else:
               r = min(255, r + amount)
           if g < 128:
               g = max(0, g - amount)
           else:
               g = min(255, g + amount)
           if b < 128:
               b = max(0, b - amount)
           else:
               b = min(255, b + amount)
           edited_pixels.append((r, g, b))
   edited_image = Image.new("RGB", image.size)
   edited_image.putdata(edited_pixels)
   return edited_image

def sharp_contrast(image, amount): #20 for amount works well
   sharp_image = image.filter(ImageFilter.SHARPEN)
   edited_image = contrast(sharp_image, amount)
   return edited_image

def dim_filter(image, strength):
   pixels = image.load()
   width, height = image.size
   new_pixels = []

   for y in range(height):
       for x in range(width):
           r, g, b = pixels[x, y]

           brightness = (r + g + b) / 3
           factor = 1 - (brightness / 255) * strength

           r = int(r * factor)
           g = int(g * factor)
           b = int(b * factor)
           pixel = (r,g,b)
           pixel = check_max(pixel)
           new_pixels.append(pixel)

   new_img = Image.new("RGB", image.size)
   new_img.putdata(new_pixels)
   return new_img

def vignette_filter(image, strength):
   pixels = image.load()
   width, height = image.size

   center_x = width / 2
   center_y = height / 2
   max_dist = (center_x**2 + center_y**2) ** 0.5

   new_pixels = []

   for y in range(height):
       for x in range(width):
           r, g, b = pixels[x, y]

           dx = x - center_x
           dy = y - center_y
           dist = (dx**2 + dy**2) ** 0.5

           factor = 1 - (dist / max_dist) * strength

           r = int(r * factor)
           g = int(g * factor)
           b = int(b * factor)
           pixel = (r,g,b)
           pixel = check_max(pixel)
           new_pixels.append(pixel)

   new_img = Image.new("RGB", image.size)
   new_img.putdata(new_pixels)
   return new_img

def contrast_filter(image, contrast):
   pixels = image.load()
   width, height = image.size
   new_pixels = []

   for y in range(height):
       for x in range(width):
           r, g, b = pixels[x, y]

           r = int((r - 128) * contrast + 128)
           g = int((g - 128) * contrast + 128)
           b = int((b - 128) * contrast + 128)

           r = max(0, min(255, r))
           g = max(0, min(255, g))
           b = max(0, min(255, b))
           pixel = (r,g,b)
           pixel = check_max(pixel)
           new_pixels.append(pixel)

   new_img = Image.new("RGB", image.size)
   new_img.putdata(new_pixels)
   return new_img

def sharpen_filter(image):
    return image.filter(ImageFilter.SHARPEN)

def cinematic_stack(image, contrast, dim_strength, vignette_strength):
   image = dim_filter(image, dim_strength)
   image = contrast_filter(image, contrast)
   image = vignette_filter(image, vignette_strength)
   image = sharpen_filter(image)

   return image





print("Welcome to AutoAura Images, where your car photography is taken to creative heights!\n We offer 10 filters with many user customizations making possibilities endless.")
sleep(1)
name = input('Provide the image file name:   ')
try:
    car = Image.open(name)
    check = True
except OSError:
    check = False
while check is False:
    name = input('Make sure to provide the correct image file name and are in the same location (files):   ')
    try:
        car = Image.open(name)
        check = True
    except OSError:
        check = False
car_pixels = car.load()
edit_car = []

filter_ = input('''Which filter would you like to use?  
1: Checkered flag
2: Warmth
3: Noise
4: Vintage film
5: Old paper
6: Contrast
7: Sharpen and contrast
8: Dim
9: Vignette
10: Cinematic stack\n''')

try:
    filter_ = int(filter_)
    check = True
except ValueError:
    check = False
   
while check is False or int(filter_) not in list(range(1,11)):
    filter_ = input('''Which filter would you like to use? Please provide a number in the correct range:  
1: Checkered flag
2: Warmth
3: Noise
4: Vintage film
5: Old paper
6: Contrast
7: Sharpen and contrast
8: Dim
9: Vignette
10: Cinematic stack\n''')
    try:
        filter_ = int(filter_)
        check = True
    except ValueError:
        check = False
       
if filter_ == 1:
    num_squares = input('Please provide the number of squares you would like the longest side of your image to be, range 2-800:   ')
    try:
        num_squares = int(num_squares)
        check = True
    except ValueError:
        check = False
    while check is False or num_squares < 2 or num_squares > 800:
        num_squares = input('Please provide the number of squares you would like the longest side of your image to be, range 2-800:   ')
        try:
            num_squares = int(num_squares)
            check = True
        except ValueError:
            check = False

    checkered_car = checkered_flag(car, car_pixels, edit_car, num_squares)
    base_name = name.split(".")[0]
    checkered_car.save("checkered_" + base_name + ".jpg")

    print("Saved as checkered_" + base_name + ".jpg")
   
elif filter_ == 2:
    ammount = input('How much red would you like to add?   ')
    try:
        ammount = int(ammount)
        check = True
    except ValueError:
        check = False
    while check is False:
        ammount = input('How much red would you like to add?   ')
        try:
            ammount = int(ammount)
            check = True
        except ValueError:
            check = False
    warm_car = warm(car, ammount)
    base_name = name.split(".")[0]
    warm_car.save("warm_" + base_name + ".jpg")

    print("Saved as warm_" + base_name + ".jpg")
   
elif filter_ == 3:
    ammount = input('How much noise would you like to add?   ')
    try:
        ammount = int(ammount)
        check = True
    except ValueError:
        check = False
    while check is False:
        ammount = input('How much noise would you like to add?   ')
        try:
            ammount = int(ammount)
            check = True
        except ValueError:
            check = False
    noise_car = noise(car, ammount)
    base_name = name.split(".")[0]
    noise_car.save("noise_" + base_name + ".jpg")

    print("Saved as noise_" + base_name + ".jpg")

elif filter_ == 4:
    warmth = input('How much red would you like to add?   ')
    try:
        warmth = int(warmth)
        check = True
    except ValueError:
        check = False
    while check is False:
        warmth = input('How much red would you like to add?   ')
        try:
            warmth = int(warmth)
            check = True
        except ValueError:
            check = False
    grain = input('How much grain would you like to add?   ')
    try:
        grain = int(grain)
        check = True
    except ValueError:
        check = False
    while check is False:
        grain = input('How much grain would you like to add?   ')
        try:
            grain = int(grain)
            check = True
        except ValueError:
            check = False
    vintage_car = vintage_film(car, warmth, grain)
    base_name = name.split(".")[0]
    vintage_car.save("vintage_" + base_name + ".jpg")

    print("Saved as vintage_" + base_name + ".jpg")

elif filter_ == 5:
    old_paper_car =  old_paper(car, car_pixels, edit_car)
    base_name = name.split(".")[0]
    old_paper_car.save("old_paper_" + base_name + ".jpg")

    print("Saved as old_paper_" + base_name + ".jpg")
   
elif filter_ == 6:
    ammount = input('How much constrast would you like to have?   ')
    try:
        ammount = int(ammount)
        check = True
    except ValueError:
        check = False
    while check is False:
        ammount = input('How much contrast would you like to have?   ')
        try:
            ammount = int(ammount)
            check = True
        except ValueError:
            check = False
    contrast_car = contrast(car, ammount)
    base_name = name.split(".")[0]
    contrast_car.save("contrast_" + base_name + ".jpg")

    print("Saved as contrast_" + base_name + ".jpg")
   
elif filter_ == 7:
    ammount = input('How much contrast/sharpenss would you like to add?   ')
    try:
        ammount = int(ammount)
        check = True
    except ValueError:
        check = False
    while check is False:
        ammount = input('How much contrast/sharpenss would you like to add?   ')
        try:
            ammount = int(ammount)
            check = True
        except ValueError:
            check = False
    sharp_contrast_car = sharp_contrast(car, ammount)
    base_name = name.split(".")[0]
    sharp_contrast_car.save("sharp_contrast_" + base_name + ".jpg")

    print("Saved as sharp_contrast_" + base_name + ".jpg")
           
elif filter_ == 8:
    ammount = input('How much would you like to dim?   ')
    try:
        ammount = float(ammount)
        check = True
    except ValueError:
        check = False
    while check is False:
        ammount = input('How much would you like to dim?   ')
        try:
            ammount = float(ammount)
            check = True
        except ValueError:
            check = False
    dim_filter_car = dim_filter(car,ammount)
    base_name = name.split(".")[0]
    dim_filter_car.save("dim_filter_" + base_name + ".jpg")

    print("Saved as dim_filter_" + base_name + ".jpg")
   
elif filter_ == 9:
    ammount = input('How much boarder for vignette would you like?   ')
    try:
        ammount = float(ammount)
        check = True
    except ValueError:
        check = False
    while check is False:
        ammount = input('How boarder for vignette would you like?   ')
        try:
            ammount = float(ammount)
            check = True
        except ValueError:
            check = False
    border_car = vignette_filter(car,ammount)
    base_name = name.split(".")[0]
    border_car.save("vignette_filter_" + base_name + ".jpg")

    print("Saved as vignette_filter_" + base_name + ".jpg")
   
elif filter_ == 10:
    contrast_ = input('How much contrast would you like?   ')
    try:
        contrast_ = float(contrast_)
        check = True
    except ValueError:
        check = False
    while check is False:
        contrast_ = input('How contrast would you like?   ')
        try:
            contrast_ = float(contrast_)
            check = True
        except ValueError:
            check = False
    border = input('How much boarder for vignette would you like?   ')
    try:
        border = float(border)
        check = True
    except ValueError:
        check = False
    while check is False:
        border = input('How boarder for vignette would you like?   ')
        try:
            border = float(border)
            check = True
        except ValueError:
            check = False
    darkness = input('How much would you like to darken the image?   ')
    try:
        darkness = float(darkness)
        check = True
    except ValueError:
        check = False
    while check is False:
        darkness = input('How would you like to darken the image?   ')
        try:
            darkness = float(darkness)
            check = True
        except ValueError:
            check = False
    cinematic_car = cinematic_stack(car,contrast_ ,darkness , border)
    base_name = name.split(".")[0]
    cinematic_car.save("cinematic_" + base_name + ".jpg")

    print("Saved as cinematic_" + base_name + ".jpg")