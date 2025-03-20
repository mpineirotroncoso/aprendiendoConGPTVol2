import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk

class MiVentana(Gtk.Window):
    def __init__(self):
        super().__init__(title="Ejemplo de attach_next_to() en GtkGrid")

        grid = Gtk.Grid()
        self.add(grid)

        boton1 = Gtk.Button(label="Botón 1")
        boton2 = Gtk.Button(label="Botón 2")
        boton3 = Gtk.Button(label="Botón 3")

        grid.attach(boton1, 0, 0, 1, 1)  # Botón 1 en (0,0)
        grid.attach_next_to(boton2, boton1, Gtk.PositionType.RIGHT, 1, 1)  # Botón 2 a la derecha de Botón 1
        grid.attach_next_to(boton3, boton1, Gtk.PositionType.BOTTOM, 2, 1)  # Botón 3 abajo de Botón 1, ocupa 2 columnas

        self.connect("destroy", Gtk.main_quit)
        self.show_all()

Gtk.init()
MiVentana()
Gtk.main()
