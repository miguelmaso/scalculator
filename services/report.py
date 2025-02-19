
with open('report_template.md', 'r') as f:
    template = f.read()


report_string = template.format(
    project='My project',
    client='A Architects',
    author='It´s me!',
    m_rd=351,
    moment_units='kNm'
)



from weasyprint import HTML
from markdown import markdown

html = markdown(report_string)
pdf = HTML(string=html).write_pdf(target='report.pdf')



# from md2pdf.core import md2pdf

# md2pdf(
#     pdf_file_path='report.pdf',
#     md_content=report_string
# )
