import PIL.Image


def resize_img_to_height(img, height):
    """#TODO docstring"""

    
    # Calculate width based on fixed height
    hpercent = (height / float(img.size[1]))
    wsize = int((float(img.size[0]) * float(hpercent)))

    # Resize image and save in a file object
    return img.resize((wsize, height), PIL.Image.LANCZOS)