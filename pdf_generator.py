# pdf_generator.py

import io
from datetime import datetime
from fpdf import FPDF

class PDF(FPDF):
    """Clase personalizada para generar cabecera y pie de página."""
    def header(self):
        self.set_font('Helvetica', 'B', 15)
        self.cell(0, 10, 'Reporte de Simulación de Crecimiento de Usuarios', 0, 1, 'C')
        self.ln(5)

    def footer(self):
        self.set_y(-15)
        self.set_font('Helvetica', 'I', 8)
        page_num = self.page_no()
        generation_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.cell(0, 10, f'Página {page_num} | Generado: {generation_date}', 0, 0, 'C')

def _write_markdown_cell(pdf, text):
    """
    Renderiza texto con formato Markdown básico en el PDF de forma robusta.
    Maneja títulos, negritas, backticks y saltos de línea.
    """
    # Limpiar separadores '---' que son para Streamlit
    text = text.replace('\n---\n', '\n')

    for line in text.split('\n'):
        line = line.strip()
        if not line:
            pdf.ln(3) # Espacio para párrafos vacíos
            continue

        # Manejo de Títulos
        if line.startswith('###'):
            pdf.set_font('Helvetica', 'B', 14)
            pdf.ln(6)
            pdf.multi_cell(0, 6, line.replace('###', '').replace('`', '').strip())
            pdf.ln(2)
        elif line.startswith('####'):
            pdf.set_font('Helvetica', 'B', 12)
            pdf.ln(4)
            pdf.multi_cell(0, 6, line.replace('####', '').strip())
            pdf.ln(1)
        else:
            # Manejo de texto normal con formato en línea (negritas, backticks)
            pdf.set_font('Helvetica', '', 10)
            # Reemplazar ` con un estilo monoespaciado si se desea, o simplemente quitarlo
            line = line.replace('`', '') 
            # Dividir la línea por ** para alternar negritas
            segments = line.split('**')
            for i, segment in enumerate(segments):
                if i % 2 == 1: # Texto en negrita
                    pdf.set_font('', 'B')
                else: # Texto normal
                    pdf.set_font('', '')
                pdf.write(5, segment)
            pdf.ln(5) # Salto de línea después de cada línea de texto

def create_pdf_report(params, fig, analysis_text):
    """
    Genera un reporte en PDF con los parámetros, gráficas y análisis.
    
    Returns:
        bytes: El contenido del PDF generado.
    """
    pdf = PDF('P', 'mm', 'A4')
    pdf.add_page()
    
    # --- Sección de Parámetros ---
    pdf.set_font('Helvetica', 'B', 14)
    pdf.cell(0, 10, '1. Parámetros de la Simulación', 0, 1, 'L')
    pdf.set_font('Helvetica', '', 11)
    for key, value in params.items():
        pdf.cell(0, 8, f"  - {key}: {value}", 0, 1, 'L')
    pdf.ln(5)

    # --- Sección de Gráficas ---
    pdf.set_font('Helvetica', 'B', 14)
    pdf.cell(0, 10, '2. Resultados Gráficos', 0, 1, 'L')
    
    # Guardar la figura de matplotlib en un buffer en memoria
    buf = io.BytesIO()
    fig.savefig(buf, format='png', dpi=300, bbox_inches='tight')
    buf.seek(0)
    
    # Insertar la imagen en el PDF
    # Ancho de la página A4 es 210mm, con márgenes de 10mm a cada lado -> 190mm de ancho útil
    pdf.image(buf, x=pdf.get_x(), y=pdf.get_y(), w=190)
    buf.close()
    
    # Añadir nueva página para el análisis para evitar desbordamientos
    pdf.add_page()

    # --- Sección de Análisis ---
    pdf.set_font('Helvetica', 'B', 14)
    pdf.cell(0, 10, '3. Análisis e Interpretación', 0, 1, 'L')
    
    # Usar la función auxiliar para escribir el texto con formato
    _write_markdown_cell(pdf, analysis_text)

    # Generar el PDF como un string de bytes
    return bytes(pdf.output())
