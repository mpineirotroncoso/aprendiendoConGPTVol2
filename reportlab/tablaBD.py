from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle
import sqlite3  # Usamos SQLite para conectar con la base de datos

# Función para generar el PDF
def generar_pdf(numero_albaran):
    # Conectar a la base de datos
    conexion = sqlite3.connect("modelosClasicos.dat")  # Reemplaza con tu BD si es diferente
    cursor = conexion.cursor()

    # Consulta para obtener los datos del albarán
    consulta = """
    SELECT d.codigoProduto, p.nomeProduto, d.cantidade, d.prezoUnitario 
    FROM detalleVentas d 
    LEFT JOIN produtos p ON p.codigoProduto = d.codigoProduto 
    WHERE d.numeroAlbaran = ?
    """
    cursor.execute(consulta, (numero_albaran,))
    datos = cursor.fetchall()

    # Cerrar la conexión
    conexion.close()

    # Crear el PDF
    nombre_pdf = f"albaran_{numero_albaran}.pdf"
    pdf = SimpleDocTemplate(nombre_pdf, pagesize=letter)

    # Estructura de la tabla
    data = [["Código", "Producto", "Cantidad", "Precio"]]  # Encabezados
    data.extend(datos)  # Agregar los datos de la BD

    # Crear la tabla con estilos
    tabla = Table(data)
    estilo = TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.gray),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
    ])
    tabla.setStyle(estilo)

    # Guardar el PDF
    pdf.build([tabla])

    print(f"PDF generado: {nombre_pdf}")

# Ejemplo de uso (puedes cambiar el número de albarán)
generar_pdf(1)
