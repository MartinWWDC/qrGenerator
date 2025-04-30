from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from PyPDF2 import PdfReader, PdfWriter
import io

def crea_layer_testo_con_immagine(dati, posizioni, dimensioni_font, percorso_immagine, img_pos, img_size, dimensione_pagina):
    packet = io.BytesIO()
    c = canvas.Canvas(packet, pagesize=dimensione_pagina)

    # Scrive il testo
    for campo, valore in dati.items():
        x, y = posizioni.get(campo, (0, 0))
        size = dimensioni_font.get(campo, 12)
        c.setFont("Helvetica", size)
        c.drawString(x, y, valore)

    # Inserisce immagine (logo o QR code)
    if percorso_immagine:
        img_x, img_y = img_pos
        img_w, img_h = img_size
        c.drawImage(percorso_immagine, img_x, img_y, width=img_w, height=img_h, mask='auto')

    c.save()
    packet.seek(0)
    return PdfReader(packet)

def unisci_pdf(template_path, layer_reader, output_path):
    template_reader = PdfReader(template_path)
    writer = PdfWriter()

    page = template_reader.pages[0]
    page.merge_page(layer_reader.pages[0])
    writer.add_page(page)

    with open(output_path, "wb") as f_out:
        writer.write(f_out)

# === ESEMPIO DI UTILIZZO ===
def test():
    # Dati da scrivere
    dati = {
        "nome": "Mario Rossi",
        "corso": "Ingegneria Informatica",
        "data": "30/04/2025",
        "test": "Corso di Python Avanzato"
    }

    # Coordinate (x, y) in punti
    posizioni = {
        "nome": (50, 410),
        "corso": (50, 325),
        "data": (50, 235),
        "test": (50, 150)  
    }


    # Dimensione testo per ciascun campo
    dimensioni_font = {
        "nome": 25,
        "corso": 25,
        "data": 25,
        "test": 25
    }

    # Immagine da inserire (es. QR code o logo)
    percorso_immagine = "qr_temp.png" 
    img_pos = (546, 177)              
    img_size = (170, 170)             

    # PDF di partenza (grafica di sfondo) e PDF finale
    template_pdf = "cartellino_template.pdf"
    output_pdf = "cartellino_finale.pdf"
    dimensione_pagina = (21000,29700)  # O usa (larghezza, altezza) se diverso

    # Crea layer e unisci al PDF
    layer = crea_layer_testo_con_immagine(
        dati,
        posizioni,
        dimensioni_font,
        percorso_immagine,
        img_pos,
        img_size,
        dimensione_pagina
    )
    unisci_pdf(template_pdf, layer, output_pdf)

    print("✅ PDF finale generato con successo:", output_pdf)

