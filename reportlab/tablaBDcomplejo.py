from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle
import sqlite3


def generar_pdf(numero_albaran):
    # Conectar a la base de datos
    conexion = sqlite3.connect("modelosClasicos.dat")
    cursor = conexion.cursor()

    # Consulta a la BD
    consulta = """
    SELECT d.codigoProduto, p.nomeProduto, d.cantidade, d.prezoUnitario 
    FROM detalleVentas d 
    LEFT JOIN produtos p ON p.codigoProduto = d.codigoProduto 
    WHERE d.numeroAlbaran = ?
    """
    cursor.execute(consulta, (numero_albaran,))
    datos = cursor.fetchall()
    conexion.close()

    # Nombre del archivo PDF
    nombre_pdf = f"albaran_{numero_albaran}.pdf"

    # Crear el PDF con un lienzo (Canvas)
    c = canvas.Canvas(nombre_pdf, pagesize=letter)
    ancho, alto = letter

    # 📌 Dibujar un título
    c.setFont("Helvetica-Bold", 16)
    c.drawString(200, alto - 50, f"Albarán Nº {numero_albaran}")

    # 📌 Dibujar líneas horizontales (ejemplo de margen)
    c.setStrokeColor(colors.blue)
    c.line(50, alto - 60, ancho - 50, alto - 60)  # Línea debajo del título

    # 📌 Dibujar líneas verticales
    c.setStrokeColor(colors.red)
    c.line(50, 100, 50, alto - 60)  # Línea izquierda
    c.line(ancho - 50, 100, ancho - 50, alto - 60)  # Línea derecha

    # 📌 Crear la tabla con los datos
    data = [["Código", "Producto", "Cantidad", "Precio"]] + datos

    tabla = Table(data, colWidths=[100, 200, 80, 80])
    estilo = TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.lightgrey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.black),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ('LINEABOVE', (0, 0), (-1, 0), 1.5, colors.black),  # Línea arriba del encabezado
    ])
    tabla.setStyle(estilo)

    # 📌 Dibujar la tabla en el PDF
    tabla.wrapOn(c, ancho, alto)
    tabla.drawOn(c, 50, alto - 250)  # Posición de la tabla

    # Guardar el PDF
    c.save()

    print(f"PDF generado: {nombre_pdf}")


# Prueba con un número de albarán
generar_pdf(1)
