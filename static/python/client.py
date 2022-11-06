# noinspection PyUnresolvedReferences,PyPackageRequirements
import pyodide
from sys import getsizeof

# noinspection PyUnresolvedReferences,PyPackageRequirements
import numpy as np
from js import document, console, Image, FileReader, Uint8ClampedArray, Object, Event
# noinspection PyPackages
import db_api

# noinspection PyPackages
from db_api import Database
from kmeans import Kmeans

DATABASE: Database = db_api.download_db()
KMEANS: Kmeans = Kmeans(np.array([]))

def main():
    check_slider_buttons()
    add_slider_events()
    add_file_event()
    add_K_event()

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

def image_size(b64string): 
    return ((len(b64string) * 3) / 4 - b64string.count('=', -2)) / 1000;

def generate_slider_item(image, colors, compressed = False):
    slider = document.getElementById('slider')
    slider_item = Object.assign(
        document.createElement('div'),
    )
    add_class(slider_item, 'slider-item')
    if compressed:
        add_class(slider_item, 'compressed')
    html_string = f"""
        <div class="item-header">
            <img
                src="{image}"
                alt="img-content"
                class="img-content"
            />
        </div>
        <div class="item-body">
            <h4>{colors} colors -> {round(image_size(image),2)}KB</h4>
        </div>
    """
    slider_item.innerHTML = html_string
    slider.prepend(slider_item)
    DATABASE.increment_db()
    check_slider_buttons()

def generate_image(rgba_array, colors, compressed=False):
    size = 256
    width = size
    height = size
    canvas = document.createElement('canvas')
    ctx = canvas.getContext('2d')
    canvas.width = width
    canvas.height = height

    buffer = Uint8ClampedArray.new(len(rgba_array))

    for i in range(0, len(rgba_array), 4):
        buffer[i] = rgba_array[i]
        buffer[i+1] = rgba_array[i+1]
        buffer[i+2] = rgba_array[i+2]
        buffer[i+3] = rgba_array[i+3]

    idata = ctx.createImageData(width, height);
    idata.data.set(buffer);
    ctx.putImageData(idata, 0, 0);
    generate_slider_item(canvas.toDataURL(), colors, compressed)

# https://github.com/pyscript/pyscript/blob/main/examples/numpy_canvas_fractals.html
# Method to fire when a file is loaded
def onload_read_file(e = None):
    img = Image.new()

    # Method fired when an image is loaded
    def on_load(evt=None):
        canvas = document.createElement('canvas')
        context = canvas.getContext('2d')
    
        canvas.width = img.width
        canvas.height = img.height

        context.drawImage(img, 0, 0 )
        image_data = context.getImageData(0, 0, img.width, img.height)
        update_loader(True, 'Converting the image...')
        np_image = np.array(list(image_data.data))

        update_loader(True, 'Image resizing...')
        np_image = np_image.reshape(img.height, img.width, 4) # reshaping image
        np_image = KMEANS.resize(np_image) # resize the image with a maximale size of 256

        np_image = np_image.reshape(-1, 4) # reshaping by 4 because rgba
        np_image, alpha = np_image[:, :3], np_image[:, 3:] # we remove alpha transparency value

        np_image = np_image / 255
        original_colors = np.unique(np_image, axis=0)

        update_loader(True, 'Loading k mean...')
        KMEANS.reset(np_image)
        centroids, idx = KMEANS.run(update_loader)
        np_new_image, new_colors = KMEANS.reshape(centroids, idx, alpha)
        
        update_loader(True, 'Images generation ...')
        generate_image(list(np_new_image), len(new_colors), True)
        generate_image(list(np.concatenate([ np_image * 255, alpha], axis = 1).reshape(-1)), len(original_colors))
        update_loader(False, '')

        if evt:
            evt.preventDefault()
        return False
    
    img.onload = on_load;
    img.src = e.target.result;
    if e:
        e.preventDefault()
    return False

def update_loader(display, message):
    loader = document.getElementById('loader')
    loader_text = document.getElementById('loader-text')

    if display:
        loader_text.innerHTML = message
        remove_class(loader, 'hide')
    else :
        loader_text.innerHTML = ''
        add_class(loader, 'hide')


# Method to add the event on the input file
def add_file_event():
    def evt(e=None):
        try:
            if len(list(e.target.files)) > 0:
                update_loader(True, 'Reading file')
                reader = FileReader.new();
                reader.readAsDataURL(list(e.target.files)[0]);
                reader.onload = onload_read_file
                new_image_button.value = ''
            if e:
                e.preventDefault()
            return False
        except Exception as x:
            print("Error add file: {}".format(x))
            return False
    new_image_button = document.getElementById('new-image')
    new_image_button.onchange = evt

    
def add_K_event():
    def evt(e=None):
        try:
            value = int(e.target.value)
            if value > 0 and value < 255:
                KMEANS.set_k(value)
            if e:
                e.preventDefault()
            return False
        except Exception as x:
            print("Error add file: {}".format(x))
            return False
    kmeans_button = document.getElementById('kmeans')
    kmeans_button.onchange = evt

def remove_class(element, class_name):
    element.classList.remove(class_name)


def add_class(element, class_name):
    element.classList.add(class_name)

try:
    main()
except Exception as x:
    print("Error starting kmeans script: {}".format(x))