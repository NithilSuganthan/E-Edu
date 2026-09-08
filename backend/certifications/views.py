from django.shortcuts import render, get_object_or_404, redirect
from .models import CertificationCourse, Certificate
from django.contrib import messages
from django.views.decorators.csrf import csrf_exempt

def index(request):
    courses = CertificationCourse.objects.all()
    return render(request, 'certifications/index.html', {'courses': courses})

@csrf_exempt
def verify_certificate(request):
    if request.method == 'POST':
        cert_id = request.POST.get('certificate_id', '').strip()
        if cert_id:
            try:
                certificate = Certificate.objects.get(certificate_id__iexact=cert_id)
                # Redirect to result page
                return redirect('certifications:result', id=certificate.certificate_id)
            except Certificate.DoesNotExist:
                messages.error(request, 'Certificate Not Found / Invalid')
                return redirect('certifications:index')
        else:
             messages.error(request, 'Please enter a Certificate ID')
             return redirect('certifications:index')
    return redirect('certifications:index')

def certificate_result(request, id):
    certificate = get_object_or_404(Certificate, certificate_id=id)
    return render(request, 'certifications/result.html', {'certificate': certificate})
