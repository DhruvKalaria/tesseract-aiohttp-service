from pdf2image import convert_from_path, convert_from_bytes


def convert_pdf_to_jpeg(file_path):
    images = convert_from_path(file_path)
    if len(images) == 0:
        return None
    else:
        return images
