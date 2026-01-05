from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, HRFlowable
from reportlab.lib.units import inch
from reportlab.lib.enums import TA_RIGHT, TA_CENTER, TA_LEFT
from io import BytesIO

def create_pdf(data):
    template = data.get('template', 'classic')
    
    if template == 'modern':
        return create_modern_pdf(data)
    else:
        return create_classic_pdf(data)

def format_link(text, url=None):
    if not url:
        return text
    # Clean up URL for href
    href = url.strip()
    if not href.startswith('http'):
        href = 'https://' + href
    return f'<link href="{href}" color="blue">{text}</link>'

def get_font_name(font_key, is_bold=False):
    fonts = {
        'sans': ('Helvetica', 'Helvetica-Bold'),
        'serif': ('Times-Roman', 'Times-Bold'),
        'mono': ('Courier', 'Courier-Bold')
    }
    font_pair = fonts.get(font_key, fonts['sans'])
    return font_pair[1] if is_bold else font_pair[0]

def create_classic_pdf(data):
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter,
                            rightMargin=50, leftMargin=50,
                            topMargin=50, bottomMargin=50)
    
    story = []
    styles = getSampleStyleSheet()
    
    selected_font = data.get('font', 'sans')
    
    # Custom Styles
    style_name = ParagraphStyle(
        'Name',
        parent=styles['Heading1'],
        fontSize=24,
        leading=28,
        spaceAfter=6,
        textColor=colors.HexColor('#1a1a1a'),
        fontName=get_font_name(selected_font, True),
        alignment=TA_LEFT
    )
    
    style_contact = ParagraphStyle(
        'Contact',
        parent=styles['Normal'],
        fontSize=10,
        leading=14, # Increased leading for stacked items
        textColor=colors.HexColor('#666666'),
        fontName=get_font_name(selected_font),
        alignment=TA_LEFT
    )
    
    style_section_header = ParagraphStyle(
        'SectionHeader',
        parent=styles['Heading2'],
        fontSize=14,
        leading=16,
        spaceBefore=12,
        spaceAfter=6,
        textColor=colors.HexColor('#2c3e50'),
        fontName=get_font_name(selected_font, True),
        borderPadding=(0, 0, 5, 0)
    )
    
    style_item_title = ParagraphStyle(
        'ItemTitle',
        parent=styles['Normal'],
        fontSize=12,
        leading=14,
        spaceBefore=6,
        fontName=get_font_name(selected_font, True),
        textColor=colors.HexColor('#333333')
    )
    
    style_item_sub = ParagraphStyle(
        'ItemSub',
        parent=styles['Normal'],
        fontSize=10,
        leading=12,
        textColor=colors.HexColor('#666666'),
        fontName=get_font_name(selected_font)
    )
    
    style_normal = ParagraphStyle(
        'Body',
        parent=styles['Normal'],
        fontSize=10,
        leading=14,
        fontName=get_font_name(selected_font),
        textColor=colors.HexColor('#333333')
    )

    # Helper to add section line
    def add_section_line():
        story.append(Spacer(1, 2))
        story.append(HRFlowable(width="100%", thickness=1, color=colors.HexColor('#eeeeee'), spaceBefore=2, spaceAfter=10))

    # --- Header ---
    if data.get('full_name'):
        story.append(Paragraph(data.get('full_name'), style_name))
    
    # Contact Info (Stacked)
    contact_items = []
    if data.get('email'): 
        contact_items.append(data.get('email'))
    if data.get('phone'): 
        contact_items.append(data.get('phone'))
    if data.get('linkedin'): 
        contact_items.append(format_link(f"LinkedIn: {data.get('linkedin')}", data.get('linkedin')))
    if data.get('github'): 
        contact_items.append(format_link(f"GitHub: {data.get('github')}", data.get('github')))
    
    for item in contact_items:
        story.append(Paragraph(item, style_contact))
    
    story.append(Spacer(1, 20))

    # Add content sections
    add_common_sections(story, data, style_section_header, style_normal, style_item_title, style_item_sub, add_section_line)

    doc.build(story)
    buffer.seek(0)
    return buffer

def create_modern_pdf(data):
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter,
                            rightMargin=40, leftMargin=40,
                            topMargin=40, bottomMargin=40)
    
    story = []
    styles = getSampleStyleSheet()
    
    selected_font = data.get('font', 'sans')
    
    # Modern Colors
    accent_color = colors.HexColor('#2980b9') # Flat Blue
    text_color = colors.HexColor('#2c3e50')
    
    # Custom Styles
    style_name = ParagraphStyle(
        'Name',
        parent=styles['Heading1'],
        fontSize=28,
        leading=32,
        spaceAfter=10,
        textColor=accent_color,
        fontName=get_font_name(selected_font, True),
        alignment=TA_LEFT
    )
    
    style_contact = ParagraphStyle(
        'Contact',
        parent=styles['Normal'],
        fontSize=9,
        leading=14, # Increased leading
        textColor=text_color,
        fontName=get_font_name(selected_font),
        alignment=TA_LEFT
    )
    
    style_section_header = ParagraphStyle(
        'SectionHeader',
        parent=styles['Heading2'],
        fontSize=12,
        leading=14,
        spaceBefore=15,
        spaceAfter=8,
        textColor=accent_color,
        fontName=get_font_name(selected_font, True),
        textTransform='uppercase'
    )
    
    style_item_title = ParagraphStyle(
        'ItemTitle',
        parent=styles['Normal'],
        fontSize=11,
        leading=13,
        spaceBefore=4,
        fontName=get_font_name(selected_font, True),
        textColor=colors.black
    )
    
    style_item_sub = ParagraphStyle(
        'ItemSub',
        parent=styles['Normal'],
        fontSize=9,
        leading=11,
        textColor=colors.HexColor('#7f8c8d'),
        fontName=get_font_name(selected_font)
    )
    
    style_normal = ParagraphStyle(
        'Body',
        parent=styles['Normal'],
        fontSize=10,
        leading=13,
        fontName=get_font_name(selected_font),
        textColor=colors.HexColor('#34495e')
    )

    def add_section_line():
        # Modern line: thick colored line
        story.append(Spacer(1, 2))
        story.append(HRFlowable(width="100%", thickness=1.5, color=accent_color, spaceBefore=0, spaceAfter=8))

    # --- Header Block (Left Aligned with Accent) ---
    if data.get('full_name'):
        story.append(Paragraph(data.get('full_name'), style_name))
    
    # Contact Info (Stacked)
    contact_items = []
    if data.get('email'): 
        contact_items.append(data.get('email'))
    if data.get('phone'): 
        contact_items.append(data.get('phone'))
    if data.get('linkedin'): 
        contact_items.append(format_link(f"LinkedIn: {data.get('linkedin')}", data.get('linkedin')))
    if data.get('github'): 
        contact_items.append(format_link(f"GitHub: {data.get('github')}", data.get('github')))
    
    for item in contact_items:
        story.append(Paragraph(item, style_contact))
    
    story.append(Spacer(1, 25))

    # Add content sections
    add_common_sections(story, data, style_section_header, style_normal, style_item_title, style_item_sub, add_section_line)

    doc.build(story)
    buffer.seek(0)
    return buffer


def add_footer_note(story, styles):
    style_footer = ParagraphStyle(
        'FooterNote',
        parent=styles['Normal'],
        fontSize=8,
        textColor=colors.gray,
        alignment=TA_CENTER,
        spaceBefore=20
    )
    story.append(Spacer(1, 20))
    story.append(HRFlowable(width="100%", thickness=0.5, color=colors.lightgrey))
    story.append(Paragraph("Note: Links in this document are clickable.", style_footer))

def add_common_sections(story, data, style_header, style_normal, style_title, style_sub, line_func):
    # --- Summary ---
    if data.get('summary'):
        story.append(Paragraph("Professional Summary", style_header))
        line_func()
        story.append(Paragraph(data.get('summary'), style_normal))
        story.append(Spacer(1, 10))

    # --- Skills ---
    if data.get('skills'):
        story.append(Paragraph("Skills", style_header))
        line_func()
        skills = data.get('skills')
        if isinstance(skills, list):
            skills = ", ".join(skills)
        story.append(Paragraph(skills, style_normal))
        story.append(Spacer(1, 10))

    # --- Experience ---
    if data.get('experience') and len(data.get('experience')) > 0:
        story.append(Paragraph("Experience", style_header))
        line_func()
        for exp in data.get('experience'):
            title = exp.get('title', '')
            company = exp.get('company', '')
            dates = exp.get('dates', '')
            
            # Use a table for better alignment of dates
            header_text = f"<b>{title}</b>"
            if company:
                header_text += f" | {company}"
            
            # Table for header
            data_row = [[Paragraph(header_text, style_title), Paragraph(dates, style_sub)]]
            t = Table(data_row, colWidths=[None, 1.5*inch])
            t.setStyle(TableStyle([
                ('ALIGN', (1,0), (1,0), 'RIGHT'),
                ('VALIGN', (0,0), (-1,-1), 'TOP'),
                ('LEFTPADDING', (0,0), (-1,-1), 0),
                ('RIGHTPADDING', (0,0), (-1,-1), 0),
            ]))
            story.append(t)
            
            if exp.get('description'):
                story.append(Paragraph(exp.get('description'), style_normal))
            story.append(Spacer(1, 8))
        story.append(Spacer(1, 2))

    # --- Projects ---
    if data.get('projects') and len(data.get('projects')) > 0:
        story.append(Paragraph("Projects", style_header))
        line_func()
        for proj in data.get('projects'):
            name = proj.get('name', '')
            tech = proj.get('tech', '')
            
            text = name
            if tech:
                text += f" ({tech})"
            
            story.append(Paragraph(text, style_title))
            if proj.get('description'):
                story.append(Paragraph(proj.get('description'), style_normal))
            story.append(Spacer(1, 8))
        story.append(Spacer(1, 2))

    # --- Education ---
    if data.get('education') and len(data.get('education')) > 0:
        story.append(Paragraph("Education", style_header))
        line_func()
        for edu in data.get('education'):
            school = edu.get('school', '')
            degree = edu.get('degree', '')
            year = edu.get('year', '')
            
            # Table for education
            data_row = [[Paragraph(degree, style_title), Paragraph(year, style_sub)]]
            t = Table(data_row, colWidths=[None, 1.5*inch])
            t.setStyle(TableStyle([
                ('ALIGN', (1,0), (1,0), 'RIGHT'),
                ('VALIGN', (0,0), (-1,-1), 'TOP'),
                ('LEFTPADDING', (0,0), (-1,-1), 0),
                ('RIGHTPADDING', (0,0), (-1,-1), 0),
            ]))
            story.append(t)
            
            story.append(Paragraph(school, style_sub))
            story.append(Spacer(1, 8))

    # --- Certifications ---
    if data.get('certifications') and len(data.get('certifications')) > 0:
        story.append(Paragraph("Certifications", style_header))
        line_func()
        for cert in data.get('certifications'):
            name = cert.get('name', '')
            issuer = cert.get('issuer', '')
            year = cert.get('year', '')
            
            text = name
            if issuer:
                text += f" - {issuer}"
            if year:
                text += f" ({year})"
            story.append(Paragraph(text, style_normal))
            story.append(Spacer(1, 4))
