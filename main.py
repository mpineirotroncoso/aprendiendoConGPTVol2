import gi

gi.require_version("Gtk", "3.0")
from gi.repository import Gtk, GObject
from conexionBD import ConexionBD  # Importamos la clase de conexión a la BD

# Nombre de la base de datos SQLite
DB_PATH = "datos.db"


class VentanaPrincipal(Gtk.Window):
    def __init__(self):
        super().__init__(title="Gestión de Datos")
        self.set_default_size(500, 300)

        # Crear conexión a la base de datos
        self.bd = ConexionBD(DB_PATH)
        self.bd.conectaBD()
        self.bd.creaCursor()

        # Crear la interfaz
        self.crear_interfaz()

    def crear_interfaz(self):
        """Configura la interfaz con un TreeView y botones para añadir y actualizar datos."""

        # Caja vertical para organizar los widgets
        vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=6)
        self.add(vbox)

        # Modelo de datos (ListStore) para la tabla
        self.modelo = Gtk.ListStore(int, str, int)  # Columnas: ID (int), Nombre (str), Edad (int)
        self.cargar_datos()

        # Creación del TreeView
        self.treeview = Gtk.TreeView(model=self.modelo)

        # Definir las columnas de la tabla
        columnas = [("ID", 0), ("Nombre", 1), ("Edad", 2)]
        for titulo, indice in columnas:
            renderizador = Gtk.CellRendererText()
            columna = Gtk.TreeViewColumn(titulo, renderizador, text=indice)
            self.treeview.append_column(columna)

        # Agregar el TreeView dentro de un ScrolledWindow
        scrolled_window = Gtk.ScrolledWindow()
        scrolled_window.set_vexpand(True)
        scrolled_window.add(self.treeview)
        vbox.pack_start(scrolled_window, True, True, 0)

        # Botones para añadir y actualizar
        hbox = Gtk.Box(spacing=6)
        vbox.pack_start(hbox, False, False, 0)

        self.entrada_nombre = Gtk.Entry()
        self.entrada_nombre.set_placeholder_text("Nombre")
        hbox.pack_start(self.entrada_nombre, True, True, 0)

        self.entrada_edad = Gtk.Entry()
        self.entrada_edad.set_placeholder_text("Edad")
        hbox.pack_start(self.entrada_edad, True, True, 0)

        boton_añadir = Gtk.Button(label="Añadir")
        boton_añadir.connect("clicked", self.on_añadir_clicked)
        hbox.pack_start(boton_añadir, True, True, 0)

        boton_actualizar = Gtk.Button(label="Actualizar")
        boton_actualizar.connect("clicked", self.on_actualizar_clicked)
        hbox.pack_start(boton_actualizar, True, True, 0)

    def cargar_datos(self):
        """Carga los datos de la base de datos en el modelo del TreeView."""
        self.modelo.clear()
        consulta = "SELECT * FROM personas"
        registros = self.bd.consultaSenParametros(consulta)
        if registros:
            for fila in registros:
                self.modelo.append(list(fila))

    def on_añadir_clicked(self, button):
        """Añade un nuevo registro a la base de datos."""
        nombre = self.entrada_nombre.get_text().strip()
        edad = self.entrada_edad.get_text().strip()

        if nombre and edad.isdigit():
            self.bd.engadeRexistro("INSERT INTO personas (nombre, edad) VALUES (?, ?)", nombre, int(edad))
            self.cargar_datos()  # Refrescar la tabla
            self.entrada_nombre.set_text("")
            self.entrada_edad.set_text("")
        else:
            print("Error: Ingresa un nombre y una edad válida.")

    def on_actualizar_clicked(self, button):
        """Actualiza el registro seleccionado en la base de datos."""
        seleccion = self.treeview.get_selection()
        modelo, iterador = seleccion.get_selected()

        if iterador:
            id_persona = modelo.get_value(iterador, 0)  # Obtener ID del registro seleccionado
            nuevo_nombre = self.entrada_nombre.get_text().strip()
            nueva_edad = self.entrada_edad.get_text().strip()

            if nuevo_nombre and nueva_edad.isdigit():
                self.bd.actualizaRexistro("UPDATE personas SET nombre=?, edad=? WHERE id=?", nuevo_nombre,
                                          int(nueva_edad), id_persona)
                self.cargar_datos()  # Refrescar la tabla
                self.entrada_nombre.set_text("")
                self.entrada_edad.set_text("")
            else:
                print("Error: Ingresa un nombre y una edad válida.")
        else:
            print("Selecciona un registro para actualizar.")


# Crear la base de datos y la tabla si no existen
def inicializar_bd():
    bd = ConexionBD(DB_PATH)
    bd.conectaBD()
    bd.creaCursor()
    bd.engadeRexistro(
        "CREATE TABLE IF NOT EXISTS personas (id INTEGER PRIMARY KEY AUTOINCREMENT, nombre TEXT, edad INTEGER)")
    bd.pechaBD()


if __name__ == "__main__":
    inicializar_bd()
    win = VentanaPrincipal()
    win.connect("destroy", Gtk.main_quit)
    win.show_all()
    Gtk.main()
