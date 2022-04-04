import time
import gi
import threading
gi.require_version("Gtk","3.0")
from puzzle1 import Rfid
from gi.repository import Gtk, Gdk, GLib

class MyWindow(Gtk.Window):
    def __init__(self):
        super().__init__(title="Puzzle2 - RFID Reader")
        """ Diseño de la ventana """
        self.set_position(Gtk.WindowPosition.CENTER)
        box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        box.set_homogeneous(False)
        box.set_name("box")
        box_up = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        box.pack_start(box_up, True, True, 0) # pack_start(child, expand, fill, padding)
        box_up.set_name("box_up")
        self.text_label = Gtk.Label()
        self.text_label.set_name("text_label")
        self.text_label.set_markup("Please, login with your university card")
        self.button = Gtk.Button(label="Clear window")
        self.button.connect("clicked", self.on_button_clicked)
        box_up.pack_start(self.text_label, True, True, 0)
        box.pack_start(self.button, True, True, 0)
        """ Añadimos css para dar estilo a la ventana """
        screen = Gdk.Screen.get_default()
        provider = Gtk.CssProvider()
        provider.load_from_path("style.css")
        Gtk.StyleContext.add_provider_for_screen(screen, provider, Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION)
        self.add(box)

    # Reset window
    def on_button_clicked(self, widget): 
        self.text_label.set_markup("Please, login with your university card")
        self.text_label.modify_bg(Gtk.StateType.NORMAL, Gdk.color_parse("#D8E3E7"))


def read_uid():
    rf = Rfid()
    while True:
        uid = rf.read_id()
        print_uid(uid)

def print_uid(uid): # GLiB - acceder de forma asyncrona a los widgets de la pantalla
    GLib.idle_add(window.text_label.set_markup, f"<span foreground='#F8F1F1'> uid: <b>{uid}</b></span>") 
    GLib.idle_add(window.text_label.modify_bg, Gtk.StateType.NORMAL, Gdk.color_parse("#16C79A") )
    time.sleep(1)
    GLib.idle_add(window.text_label.modify_bg, Gtk.StateType.NORMAL, Gdk.color_parse("#11698E") )


if __name__ == '__main__':
    """ Thread para ejecutar de forma paralela la funcion rad_uid() """
    thread_ = threading.Thread(target=read_uid)
    thread_.start()
    """ Inicializamos y mostramos la interficie gráfica """
    window = MyWindow()
    window.connect("destroy", Gtk.main_quit)
    window.show_all()
    Gtk.main()