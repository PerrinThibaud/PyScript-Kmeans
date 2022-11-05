# noinspection PyUnresolvedReferences,PyPackageRequirements
import pyodide
# noinspection PyUnresolvedReferences,PyPackageRequirements
from js import DOMParser, document, setInterval, console
# noinspection PyPackages
import db_api

# noinspection PyPackages
from db_api import Database

DATABASE: Database = db_api.download_db()

def main():
    check_slider_buttons()
    add_slider_events()

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



def remove_class(element, class_name):
    element.classList.remove(class_name)


def add_class(element, class_name):
    element.classList.add(class_name)

try:
    main()
except Exception as x:
    print("Error starting weather script: {}".format(x))