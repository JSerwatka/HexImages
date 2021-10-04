import io 

import PIL.Image


def resize_img_to_height(img, height):
    """#TODO docstring"""

    
    # Calculate width based on fixed height
    hpercent = (height / float(img.size[1]))
    wsize = int((float(img.size[0]) * float(hpercent)))

    # Resize image and save in a file object
    return img.resize((wsize, height), PIL.Image.LANCZOS)

def generate_new_img(original_img, original_requested, requested_height):
    '''#TODO docstring'''

    # Get the img
    output = io.BytesIO()
    img = PIL.Image.open(original_img.image.path) #TODO change path to url
    # Check format - JPG or PNG
    format = img.format

    # Resize if needed
    if not original_requested:
        img = resize_img_to_height(img, requested_height)

    img.save(output, format)
    output.seek(0)

    return output, format