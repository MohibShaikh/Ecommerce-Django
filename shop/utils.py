from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from django.conf import settings
import os
from datetime import datetime
import json

def generate_receipt_pdf(order, amount_pkr, amount_usd):
    # Create the PDF directory if it doesn't exist
    pdf_dir = os.path.join(settings.MEDIA_ROOT, 'receipts')
    os.makedirs(pdf_dir, exist_ok=True)

    # Create the PDF file
    filename = f'receipt_{order.order_id}.pdf'
    filepath = os.path.join(pdf_dir, filename)
    doc = SimpleDocTemplate(filepath, pagesize=letter)
    
    # Container for the 'Flowable' objects
    elements = []
    styles = getSampleStyleSheet()
    
    # Add title
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=24,
        spaceAfter=30
    )
    elements.append(Paragraph("Order Receipt", title_style))
    elements.append(Spacer(1, 20))

    # Add order details
    order_data = [
        ['Order ID:', str(order.order_id)],
        ['Date:', datetime.now().strftime("%B %d, %Y")],
        ['Amount Paid:', f'₨{amount_pkr:.2f} ({amount_usd})'],
        ['Payment Status:', 'Paid'],
    ]
    
    # Create the order details table
    order_table = Table(order_data, colWidths=[2*inch, 4*inch])
    order_table.setStyle(TableStyle([
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ('BACKGROUND', (0, 0), (0, -1), colors.grey),
        ('TEXTCOLOR', (0, 0), (0, -1), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, -1), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 12),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 12),
        ('TOPPADDING', (0, 0), (-1, -1), 12),
    ]))
    elements.append(order_table)
    elements.append(Spacer(1, 20))

    # Add customer details
    elements.append(Paragraph("Customer Information", styles['Heading2']))
    customer_data = [
        ['Name:', order.name],
        ['Email:', order.email],
        ['Phone:', order.phone],
        ['Address:', f"{order.address}, {order.city}, {order.state} - {order.zip_code}"],
    ]
    
    # Create the customer details table
    customer_table = Table(customer_data, colWidths=[2*inch, 4*inch])
    customer_table.setStyle(TableStyle([
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ('BACKGROUND', (0, 0), (0, -1), colors.grey),
        ('TEXTCOLOR', (0, 0), (0, -1), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, -1), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 12),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 12),
        ('TOPPADDING', (0, 0), (-1, -1), 12),
    ]))
    elements.append(customer_table)
    elements.append(Spacer(1, 20))

    # Add order items
    elements.append(Paragraph("Order Items", styles['Heading2']))
    items_data = [['Item', 'Quantity', 'Price', 'Total']]
    
    # Parse the items JSON string (dict of lists)
    try:
        items = json.loads(order.items_json)
        for key, value in items.items():
            # value: [quantity, name, price]
            quantity = value[0]
            name = value[1]
            price = float(value[2])
            total = price * quantity
            items_data.append([
                name,
                str(quantity),
                f'₨{price:.2f}',
                f'₨{total:.2f}'
            ])
    except Exception as e:
        items_data.append(['Error loading items', '', '', ''])
        print(f"Error processing items: {str(e)}")
    
    # Create the items table
    items_table = Table(items_data, colWidths=[3*inch, 1*inch, 1*inch, 1*inch])
    items_table.setStyle(TableStyle([
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 12),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 12),
        ('TOPPADDING', (0, 0), (-1, -1), 12),
    ]))
    elements.append(items_table)
    elements.append(Spacer(1, 20))

    # Add footer
    footer_style = ParagraphStyle(
        'Footer',
        parent=styles['Normal'],
        fontSize=10,
        textColor=colors.grey,
        alignment=1
    )
    elements.append(Paragraph("Thank you for shopping with BuyEverything!", footer_style))
    elements.append(Paragraph("This is a computer-generated receipt and does not require a signature.", footer_style))

    # Build the PDF
    doc.build(elements)
    
    return filename 