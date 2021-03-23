import PySimpleGUI as sg
from pikepdf import Pdf, PdfImage, Name, _cpphelpers
import os
import sys

# folder_dir consists of all pdf files that wants to be changed
def anonymize(folder_dir, new=True):
    dest_folder  = os.path.join(folder_dir, 'anonymized')

    if not os.path.exists(dest_folder):
        os.makedirs(dest_folder)

    to_delete = { '/Im11': 1, '/Im8': 1, '/Im5': 1, '/Im13': 1} if new else { '/Im5': 1, '/Im12': 1, '/Im9': 1}
    
    for img in os.listdir(folder_dir):
        if img.endswith('.pdf'):
            src_path = os.path.join(folder_dir, img)
            dest_path = os.path.join(dest_folder, img)
            pdf = Pdf.open(src_path)
            new_image = pdf.make_stream(b'\xff')
            new_image.Width,  new_image.Height = 1, 1
            new_image.BitsPerComponent = 1
            new_image.ImageMask = True
            new_image.Decode = [0, 1]
            page = pdf.pages[0]

            for image_name, image in page.images.items():
                if image_name in to_delete:
                    page.Resources.XObject[image_name] = new_image

            pdf.save(dest_path)
