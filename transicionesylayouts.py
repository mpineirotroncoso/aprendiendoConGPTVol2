import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk

class LayoutDemo(Gtk.Window):
    def __init__(self):
        super().__init__(title="GTK Layouts con Transiciones")
        self.set_default_size(400, 300)

        # 📌 Caja principal
        vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=6)
        self.add(vbox)

        # 📌 Stack para cambiar entre layouts con transiciones
        self.stack = Gtk.Stack()
        self.stack.set_transition_type(Gtk.StackTransitionType.SLIDE_LEFT_RIGHT)  # Efecto deslizante
        self.stack.set_transition_duration(500)  # Duración en ms

        # 📌 Layout 1: Box
        box_layout = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10)
        box_layout.add(Gtk.Button(label="Botón 1"))
        box_layout.add(Gtk.Button(label="Botón 2"))
        box_layout.add(Gtk.Button(label="Botón 3"))
        self.stack.add_titled(box_layout, "box", "Box Layout")

        # 📌 Layout 2: Grid
        grid_layout = Gtk.Grid()
        grid_layout.set_row_spacing(10)
        grid_layout.set_column_spacing(10)
        grid_layout.attach(Gtk.Button(label="A"), 0, 0, 1, 1)
        grid_layout.attach(Gtk.Button(label="B"), 1, 0, 1, 1)
        grid_layout.attach(Gtk.Button(label="C"), 0, 1, 2, 1)
        self.stack.add_titled(grid_layout, "grid", "Grid Layout")

        # 📌 Layout 3: FlowBox
        flowbox_layout = Gtk.FlowBox()
        for i in range(1, 7):
            flowbox_layout.add(Gtk.Button(label=f"Item {i}"))
        self.stack.add_titled(flowbox_layout, "flowbox", "FlowBox Layout")

        # 📌 Selector de Layouts
        switcher = Gtk.StackSwitcher()
        switcher.set_stack(self.stack)

        # 📌 Agregar elementos a la ventana
        vbox.pack_start(switcher, False, False, 0)
        vbox.pack_start(self.stack, True, True, 0)

        self.connect("destroy", Gtk.main_quit)
        self.show_all()

# Ejecutar la aplicación
if __name__ == "__main__":
    LayoutDemo()
    Gtk.main()
