import datetime
import time

from PyQt5.QtWidgets import QFileDialog
from reportlab.lib import colors, styles
from reportlab.lib.enums import TA_JUSTIFY
from reportlab.lib.pagesizes import letter, A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image, Table, TableStyle, Frame, KeepInFrame
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import *
from reportlab.lib.enums import TA_LEFT


def render_statement(data, paragraphss, quarterly, fileName):
    doc = SimpleDocTemplate(fileName, pagesize=A4,
                            rightMargin=72, leftMargin=56,
                            topMargin=5, bottomMargin=18)
    Story = []
    logo = "logos/toplogo.png"
    logo2 = "logos/bottomlogo.png"
    im = Image(logo, 8 * inch, 3 * inch)
    im2 = Image(logo2, 7 * inch, 1 * inch)
    t_keep = KeepInFrame(0, 0, Story, mode='shrink', hAlign='CENTER', vAlign='MIDDLE')
    lista = [data.columns[:, ].values.astype(str).tolist()] + data.values.tolist()
    t1 = None
    if not quarterly:
        t1 = Table(lista, 4 * [1.5 * inch, 1.5 * inch, 2 * inch, 1.5 * inch], (len(lista)) * [0.3 * inch],
                   hAlign='CENTER')
    else:
        t1 = Table(lista, 2 * [3.2 * inch, 3.2 * inch], (len(lista)) * [0.3 * inch],
                   hAlign='CENTER')

    # t1.setStyle(TableStyle([('ALIGN', (1, 1), (-2, -2), 'RIGHT'),
    #                         ('TEXTCOLOR', (1, 1), (-2, -2), colors.red),
    #                         ('VALIGN', (0, 0), (0, -1), 'TOP'),
    #                         ('TEXTCOLOR', (0, 0), (0, -1), colors.blue),
    #                         ('ALIGN', (0, -1), (-1, -1), 'CENTER'),
    #                         ('VALIGN', (0, -1), (-1, -1), 'MIDDLE'),
    #                         ('TEXTCOLOR', (0, -1), (-1, -1), colors.green),
    #                         ('INNERGRID', (0, 0), (-1, -1), 0.25, colors.black),
    #                         ('BOX', (0, 0), (-1, -1), 0.25, colors.black),
    #                         ]))
    t1.setStyle(TableStyle(
        [("BOX", (0, 0), (-1, -1), 0.25, colors.black),
         ('INNERGRID', (0, 0), (-1, -1), 0.25, colors.black)]
    ))
    data_len = len(lista)

    for each in range(data_len):
        if each % 2 == 0:
            bg_color = colors.whitesmoke
        else:
            bg_color = colors.lightgrey

        t1.setStyle(TableStyle([('BACKGROUND', (0, each), (-1, each), bg_color)]))
    Story.append(im)
    style = ParagraphStyle(
        name='Normal',
        fontSize=12,
        borderPadding=1,
        padding=1,
        alignment=TA_LEFT,
        leading=24,
        leftMargin=10,

    )
    for x, y in paragraphss.items():
        p = ""
        p += '<b>' + x + '</b>' + ":" + y
        p += "\n"
        Story.append(Paragraph(p, style=style))
    Story.append(t1)

    Story.append(Spacer(1, 12))
    Story.append(im2)
    Story.append(t_keep)
    doc.build(Story)
