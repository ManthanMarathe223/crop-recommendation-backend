from fastapi import APIRouter, HTTPException
from fastapi.responses import StreamingResponse
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from io import BytesIO
from datetime import datetime
from models import CropInput
from ml_models import get_models

router = APIRouter(prefix="", tags=["Reports"])

@router.post("/generate-report")
async def generate_pdf_report(data: CropInput):
    try:
        crop_model, yield_model, price_model, scaler, label_encoder, crop_data = get_models()
        
        # Get predictions
        input_data = [[data.nitrogen, data.phosphorus, data.potassium,
                       data.temperature, data.humidity, data.ph_value, data.rainfall]]
        
        input_scaled = scaler.transform(input_data)
        probabilities = crop_model.predict_proba(input_scaled)[0]
        all_indices = probabilities.argsort()[::-1]
        
        # Get top 3 unique crops
        results = []
        seen_crops = set()
        
        for idx in all_indices:
            crop_name = label_encoder.inverse_transform([idx])[0]
            if crop_name in seen_crops:
                continue
            seen_crops.add(crop_name)
            confidence = float(probabilities[idx] * 100)
            
            crop_specific_data = crop_data[crop_data['Crop'] == crop_name]
            if not crop_specific_data.empty:
                predicted_yield = float(crop_specific_data['Yield'].mean())
                predicted_price = float(crop_specific_data['Price'].mean())
            else:
                predicted_yield = float(yield_model.predict(input_data)[0])
                predicted_price = float(price_model.predict(input_data)[0])
            
            revenue = 0.01 * predicted_yield * predicted_price
            
            results.append({
                "crop": crop_name,
                "confidence": round(confidence, 2),
                "yield": round(predicted_yield, 2),
                "price": round(predicted_price, 2),
                "revenue": round(revenue, 2)
            })
            
            if len(results) == 3:
                break
        
        # Create PDF
        buffer = BytesIO()
        doc = SimpleDocTemplate(buffer, pagesize=A4)
        elements = []
        styles = getSampleStyleSheet()
        
        # Title
        title_style = ParagraphStyle(
            'CustomTitle',
            parent=styles['Heading1'],
            fontSize=24,
            textColor=colors.HexColor('#2E7D32'),
            spaceAfter=30,
            alignment=1
        )
        elements.append(Paragraph("🌾 Crop Recommendation Report", title_style))
        elements.append(Spacer(1, 0.3*inch))
        
        # Report Date
        date_text = f"Generated on: {datetime.now().strftime('%B %d, %Y at %I:%M %p')}"
        elements.append(Paragraph(date_text, styles['Normal']))
        elements.append(Spacer(1, 0.3*inch))
        
        # Soil Parameters Section
        elements.append(Paragraph("📊 Soil & Climate Parameters", styles['Heading2']))
        elements.append(Spacer(1, 0.1*inch))
        
        params_data = [
            ['Parameter', 'Value', 'Unit'],
            ['Nitrogen', f"{data.nitrogen}", 'kg/ha'],
            ['Phosphorus', f"{data.phosphorus}", 'kg/ha'],
            ['Potassium', f"{data.potassium}", 'kg/ha'],
            ['Temperature', f"{data.temperature}", '°C'],
            ['Humidity', f"{data.humidity}", '%'],
            ['pH Value', f"{data.ph_value}", ''],
            ['Rainfall', f"{data.rainfall}", 'mm']
        ]
        
        params_table = Table(params_data, colWidths=[2.5*inch, 1.5*inch, 1*inch])
        params_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#4CAF50')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 12),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
            ('GRID', (0, 0), (-1, -1), 1, colors.black)
        ]))
        
        elements.append(params_table)
        elements.append(Spacer(1, 0.5*inch))
        
        # Top Recommendations Section
        elements.append(Paragraph("🏆 Top 3 Crop Recommendations", styles['Heading2']))
        elements.append(Spacer(1, 0.1*inch))
        
        rec_data = [['Rank', 'Crop', 'Confidence', 'Yield (kg/ha)', 'Price (₹/quintal)', 'Revenue (₹)']]
        
        for i, crop in enumerate(results, 1):
            rec_data.append([
                f"#{i}",
                crop['crop'],
                f"{crop['confidence']}%",
                f"{crop['yield']:,.2f}",
                f"₹{crop['price']:,.2f}",
                f"₹{crop['revenue']:,.2f}"
            ])
        
        rec_table = Table(rec_data, colWidths=[0.6*inch, 1.5*inch, 1*inch, 1.2*inch, 1.3*inch, 1.4*inch])
        rec_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#FF9800')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 10),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (0, 1), colors.HexColor('#FFD54F')),
            ('BACKGROUND', (0, 2), (0, 2), colors.HexColor('#FFE082')),
            ('BACKGROUND', (0, 3), (0, 3), colors.HexColor('#FFECB3')),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
            ('FONTNAME', (1, 1), (1, 1), 'Helvetica-Bold'),
            ('FONTSIZE', (1, 1), (1, 1), 12)
        ]))
        
        elements.append(rec_table)
        elements.append(Spacer(1, 0.5*inch))
        
        # Footer
        footer_text = """
        <para align=center>
        <b>Indra Dhanu - Smart Agriculture Platform</b><br/>
        Powered by Machine Learning | Climate-Resilient Farming Solutions<br/>
        <i>This report is generated based on ML predictions and should be used as guidance only.</i>
        </para>
        """
        elements.append(Paragraph(footer_text, styles['Normal']))
        
        # Build PDF
        doc.build(elements)
        buffer.seek(0)
        
        return StreamingResponse(
            buffer,
            media_type="application/pdf",
            headers={
                "Content-Disposition": f"attachment; filename=crop_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
            }
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))