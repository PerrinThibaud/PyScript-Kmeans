# noinspection PyUnresolvedReferences,PyPackageRequirements
import pyodide

# noinspection PyUnresolvedReferences,PyPackageRequirements
import numpy as np
from js import document, console, Image, FileReader
# noinspection PyPackages
import db_api

# noinspection PyPackages
from db_api import Database

DATABASE: Database = db_api.download_db()

def main():
    check_slider_buttons()
    add_slider_events()
    add_file_event()

def check_slider_buttons():
    previous_button = document.getElementById('previous')
    next_button = document.getElementById('next')

    if DATABASE.maxLeft:
        previous_button.setAttribute('disabled', '');
    else:
        previous_button.removeAttribute('disabled');

    if DATABASE.maxRight:
        next_button.setAttribute('disabled', '');
    else:
        next_button.removeAttribute('disabled');


def fire_previous_action():
    # update the db
    DATABASE.move_previous()
    # recalculate the position
    slider = document.getElementById('slider')
    slider.style.transform = f"translate({DATABASE.index * -17.5}rem)" # 256 => 16 and 24 => 1.5 = 17.5rem
    check_slider_buttons()

def fire_next_action():
    # update the db
    DATABASE.move_next()
    # recalculate the position
    slider = document.getElementById('slider')
    slider.style.transform = f"translate({DATABASE.index * -17.5}rem)" # 256 => 16 and 24 => 1.5 = 17.5rem
    check_slider_buttons()

def add_slider_events():
    def previous_evt(e=None):
        fire_previous_action()
        if e:
            e.preventDefault()
        return False
    
    def next_evt(e=None):
        fire_next_action()
        if e:
            e.preventDefault()
        return False


    previous_button = document.getElementById('previous')
    next_button = document.getElementById('next')
    previous_button.onclick = previous_evt
    next_button.onclick = next_evt

# Method to fire when a file is loaded
def onload_read_file(e = None):
    img = Image.new()

    # Method fired when an image is loaded
    def on_load(evt=None):
        canvas = document.createElement('canvas')
        context = canvas.getContext('2d')

        console.log('img.width', img.width)
        console.log('img.height', img.height)
        console.log('img', img)

        canvas.width = img.width
        canvas.height = img.height

        context.drawImage(img, 0, 0 )
        image_data = context.getImageData(0, 0, img.width, img.height)

        np_image = np.array(list(image_data.data))
        np_image = np_image.reshape(-1, 4) # reshaping by 4 because rgba
        print(np_image.shape)
        np_image = np_image / 255
        print(np_image)
        if evt:
            evt.preventDefault()
        return False
    
    img.onload = on_load;
    img.src = e.target.result;
    if e:
        e.preventDefault()
    return False

# Method to add the event on the input file
def add_file_event():
    def evt(e=None):
        try:
            reader = FileReader.new();
            reader.readAsDataURL(list(e.target.files)[0]);
            reader.onload = onload_read_file
            if e:
                e.preventDefault()
            return False
        except Exception as x:
            print("Error add file: {}".format(x))
            return False

    new_image_button = document.getElementById('new-image')
    new_image_button.onchange = evt

def remove_class(element, class_name):
    element.classList.remove(class_name)


def add_class(element, class_name):
    element.classList.add(class_name)

try:
    main()
except Exception as x:
    print("Error starting kmeans script: {}".format(x))