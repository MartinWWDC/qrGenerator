import requests
from fpdf import FPDF
import qrcode
import webbrowser
import os

from svg import crea_layer_testo_con_immagine, unisci_pdf


def fetchBFInfo(id):
    url = 'https://api.bikeflip.com/api/v1/bike-ads/'+id
    response = requests.get(url).json()['data']
    

    dati = {
        "model_text": response['bike_model_text'],
        "brand_name": response['bike_brand']['name'],
        "year": str(response['model_year']),
        "size": response['sizes'][0]['title']
    }

    posizioni = {
        "model_text": (50, 410),
        "brand_name": (50, 325),
        "year": (50, 235),
        "size": (50, 150)  
    }


    dimensioni_font = {
        "model_text": 25,
        "brand_name": 25,
        "year": 25,
        "size": 25
    }

    return [dati, posizioni, dimensioni_font]


def generate_pdf(id):
    items = fetchBFInfo(id)
    qr_link = 'https://www.bikeflip.com/it/bikes/'+id
    qr_img = qrcode.make(qr_link)
    qr_img_path = "qr_temp.png"
    qr_img.save(qr_img_path)

    img_pos = (546, 177)              
    img_size = (170, 170)             

    template_pdf = "cartellino_template.pdf"
    output_pdf = id+'.pdf'
    dimensione_pagina = (21000,29700)  

    layer = crea_layer_testo_con_immagine(
        items[0],
        items[1],
        items[2],
        qr_img_path,
        img_pos,
        img_size,
        dimensione_pagina
    )
    unisci_pdf(template_pdf, layer, output_pdf)

    print("✅ PDF finale generato con successo:", output_pdf)
    webbrowser.open_new(os.path.abspath(id+".pdf"))
    
    


