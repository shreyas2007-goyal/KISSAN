from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.http import HttpResponse
from .models import DiseaseProfile, CropHealthAnalysis
from apps.crops.models import Crop
from .inference import preprocess_and_screen_image
from io import BytesIO
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib import colors

def wellness_home_view(request):
    crops = Crop.objects.all()
    recent_analyses = CropHealthAnalysis.objects.select_related('crop', 'predicted_disease')[:6]
    diseases = DiseaseProfile.objects.select_related('crop')[:10]
    return render(request, 'crop_wellness/index.html', {
        'crops': crops,
        'recent_analyses': recent_analyses,
        'diseases': diseases,
    })

def wellness_screen_view(request):
    crops = Crop.objects.all()
    if request.method == 'POST' and request.FILES.get('image'):
        crop_id = request.POST.get('crop')
        crop = get_object_or_404(Crop, id=crop_id)
        image_file = request.FILES['image']

        analysis = CropHealthAnalysis.objects.create(
            farmer=request.user.farmer_profile if request.user.is_authenticated and hasattr(request.user, 'farmer_profile') else None,
            crop=crop,
            image=image_file,
            model_version='KisanVision-PyTorch-v2.1',
        )

        # Run OpenCV & PyTorch analysis
        res = preprocess_and_screen_image(analysis.image.path, crop.name)
        if res.get('status') == 'success':
            analysis.is_healthy = res['is_healthy']
            analysis.predicted_disease = res['disease']
            analysis.confidence_score = res['confidence']
            analysis.severity = res['severity']
            analysis.save()
            messages.success(request, "Crop image analyzed successfully!")
            return redirect('wellness:detail', analysis_id=analysis.id)
        else:
            messages.error(request, res.get('message', 'Failed to process image.'))
            return redirect('wellness:home')

    return render(request, 'crop_wellness/upload.html', {'crops': crops})

def wellness_detail_view(request, analysis_id):
    analysis = get_object_or_404(CropHealthAnalysis, id=analysis_id)
    return render(request, 'crop_wellness/detail.html', {'analysis': analysis})

def wellness_catalog_view(request):
    diseases = DiseaseProfile.objects.select_related('crop').all()
    return render(request, 'crop_wellness/catalog.html', {'diseases': diseases})

def wellness_export_pdf(request, analysis_id):
    analysis = get_object_or_404(CropHealthAnalysis, id=analysis_id)
    buffer = BytesIO()
    p = canvas.Canvas(buffer, pagesize=letter)
    width, height = letter

    # Header
    p.setFillColor(colors.HexColor('#14532D'))
    p.rect(0, height - 70, width, 70, fill=True, stroke=False)
    p.setFillColor(colors.white)
    p.setFont("Helvetica-Bold", 18)
    p.drawString(40, height - 45, "KisanSAATHI 2.0 - AI Crop Disease Screening Report")
    p.setFont("Helvetica", 9)
    p.drawString(40, height - 60, "Preliminary Digital Health Assessment & Treatment Guidance")

    # Body
    p.setFillColor(colors.black)
    p.setFont("Helvetica-Bold", 12)
    p.drawString(40, height - 100, f"Analysis Reference: KS-AI-2026-{analysis.id}")
    p.setFont("Helvetica", 10)
    p.drawString(40, height - 120, f"Crop Tested: {analysis.crop.name}")
    disease_title = analysis.predicted_disease.name_en if analysis.predicted_disease else ("Healthy Foliage" if analysis.is_healthy else "Inconclusive")
    p.drawString(40, height - 140, f"Identified Condition: {disease_title}")
    p.drawString(40, height - 160, f"Confidence Calibration: {analysis.confidence_score*100:.1f}%")
    p.drawString(40, height - 180, f"Severity Assessment: {analysis.get_severity_display()}")

    p.line(40, height - 195, width - 40, height - 195)

    if analysis.predicted_disease:
        p.setFont("Helvetica-Bold", 11)
        p.drawString(40, height - 215, "Observed Symptoms:")
        p.setFont("Helvetica", 9)
        p.drawString(40, height - 230, analysis.predicted_disease.symptoms[:100])
        
        p.setFont("Helvetica-Bold", 11)
        p.drawString(40, height - 255, "Recommended Cultural & Organic Treatment:")
        p.setFont("Helvetica", 9)
        p.drawString(40, height - 270, analysis.predicted_disease.treatment[:100])

        p.setFont("Helvetica-Bold", 11)
        p.drawString(40, height - 295, "Approved Chemical Formulation:")
        p.setFont("Helvetica", 9)
        p.drawString(40, height - 310, analysis.predicted_disease.recommended_pesticide or "Follow standard university package of practices.")

    p.setFont("Helvetica-Bold", 10)
    p.setFillColor(colors.red)
    p.drawString(40, 70, "IMPORTANT LEGAL & AGRONOMIC DISCLAIMER:")
    p.setFont("Helvetica", 8)
    p.setFillColor(colors.gray)
    p.drawString(40, 55, "This is an AI screening estimation based on visual pattern matching, NOT a certified laboratory diagnosis.")
    p.drawString(40, 42, "Always verify with your local KVK (Krishi Vigyan Kendra) extension officer before applying scheduled chemicals.")

    p.showPage()
    p.save()
    buffer.seek(0)
    return HttpResponse(buffer, content_type='application/pdf')
