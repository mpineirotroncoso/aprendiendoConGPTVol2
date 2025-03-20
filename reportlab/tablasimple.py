from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle

# Crear el documento PDF
pdf = SimpleDocTemplate("tabla.pdf", pagesize=letter)

# Datos de la tabla
data = [
    ["Código", "Producto", "Cantidad", "Precio"],
    [101, "Manzana", 2, "$1.00"],
    [102, "Banana", 5, "$0.50"],
    [103, "Naranja", 3, "$0.75"],
]

# Crear la tabla
tabla = Table(data)

# Estilos para la tabla
estilo = TableStyle([
    ('BACKGROUND', (0, 0), (-1, 0), colors.gray),
    ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
    ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
    ('GRID', (0, 0), (-1, -1), 1, colors.black),
])

tabla.setStyle(estilo)

# Agregar la tabla al PDF y guardarlo
pdf.build([tabla])
print("PDF con tabla generado.")
