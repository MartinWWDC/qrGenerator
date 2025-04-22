import requests
from fpdf import FPDF
import qrcode
import webbrowser
import os


def fetchBFInfo(id):
    url = 'https://api.bikeflip.com/api/v1/bike-ads/'+id
    response = requests.get(url).json()['data']
    return [response['bike_model_text'], response['bike_brand']['name'], response['model_year']]


def generate_pdf(id):
    items = fetchBFInfo(id)
    qr_link = 'https://www.bikeflip.com/it/bikes/'+id
    qr_img = qrcode.make(qr_link)
    qr_img_path = "qr_temp.png"
    qr_img.save(qr_img_path)

    pdf = FPDF(orientation='L')
    pdf.add_page()
    pdf.set_font('helvetica', size=12)

    page_width = pdf.w
    page_height = pdf.h

    margin = 10
    column_width = (page_width - 2 * margin) / 2

    line_height = 10
    text_block_height = len(items) * line_height

    start_y_text = (page_height - text_block_height) / 2
    pdf.set_xy(margin, start_y_text)
    for item in items:
        pdf.cell(column_width, line_height, str(item), ln=1)

    qr_size = 120  # <-- nuovo valore ingrandito
    qr_x = margin + column_width + 10
    qr_y = (page_height - qr_size) / 2
    pdf.image(qr_img_path, x=qr_x, y=qr_y, w=qr_size, h=qr_size)

    pdf.output(id+".pdf")
    webbrowser.open_new(os.path.abspath(id+".pdf"))
    
    


generate_pdf('126334')
