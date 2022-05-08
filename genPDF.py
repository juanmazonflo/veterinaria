import jinja2
import pdfkit

def crea_pdf(ruta_template, info, rutacss = ''):
    nombre_template = ruta_template.split('/')[-1]
    ruta_template = ruta_template.replace(nombre_template,'')

    env = jinja2.Environment(loader = jinja2.FileSystemLoader(ruta_template))
    template = env.get_template(nombre_template)
    html = template.render(info)

    options = { 'page-size': 'Letter',
                'margin-top': '0.5in',
                'margin-bottom': '0.5in',
                'margin-left': '0.5in',
                'margin-right': '0.5in',
                'encoding': 'UTF-8'
    }

    config = pdfkit.configuration(wkhtmltopdf = 'C:\Program Files\wkhtmltopdf')
    ruta_salida = '/static/PDFs/descargar.pdf'
    pdfkit.from_string(html, ruta_salida,css = rutacss, options = options, configuration = config)

if __name__ == "__main__":
    ruta_template = '/veterinaria/templates/generadorPDF.html'
    info = {"nombre_mascota": "chuy", "medicamento_recetado": "Pathozone", "cantidad_asignada": "3", "frecuencia": "Cada 8 horas"}
    crea_pdf(ruta_template, info)