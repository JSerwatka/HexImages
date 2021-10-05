import io 

import PIL.Image

#TODO static type checking
def resize_img_to_height(img, height):
    '''
    Resizes given image to the requested height and returns it
    '''
    # Calculate width based on fixed height
    hpercent = (height / float(img.size[1]))
    wsize = int((float(img.size[0]) * float(hpercent)))

    # Resize image and save in a file object
    return img.resize((wsize, height), PIL.Image.LANCZOS)

#TODO static type checking
def generate_new_img(original_img, original_requested, requested_height):
    '''
    Takes single Image model object and resizes it if needed or leaves the original size.

    Returns:
        output: new, resized img
        format: format of the img (JPG/PNG)
    '''
    # Get the img
    output = io.BytesIO()
    img = PIL.Image.open(original_img.image.path) #TODO change path to url in production
    # Check format - JPG or PNG
    format = img.format

    # Resize if needed
    if not original_requested:
        img = resize_img_to_height(img, requested_height)

    img.save(output, format)
    output.seek(0)

    return output, format