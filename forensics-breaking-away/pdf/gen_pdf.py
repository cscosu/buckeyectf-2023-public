import pdfkit

pdfkit.from_file('base.html', 'base.pdf')

from PyPDF2 import PdfReader, PdfWriter
reader = PdfReader("base.pdf")

writer = PdfWriter()
writer.clone_document_from_reader(reader)
writer.add_metadata({"ip_creator": "3.225.42.93", "time_creator": "2021-09-28 12:00:00 -400", "is_ipv6": "False" })

with open('out.pdf', 'wb') as f:
    writer.write(f)