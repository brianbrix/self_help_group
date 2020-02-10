from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Paragraph, Image,Spacer, PageBreak, Table, TableStyle
styles = getSampleStyleSheet()
styleNormal = styles['Normal']
styleHeading = styles['Heading1']
styleHeading.alignment = 1
story = []

story.append(Image('logos/toplogo.png',hAlign='CENTER'))
story.append(Spacer(inch, .25*inch))

tableData = [ ['Value 1', 'Value 2', 'Sum'],
[34, 78, 112],
[67,56, 123],
[75,23, 98]]
story.append(Table(tableData))
doc = SimpleDocTemplate('report.pdf', pagesize = A4, title = "Access Grid Venue Usage Report ", author = "AGSC")
doc.build(story)