from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST

from .aws import upload_to_s3
from .models import Attachment


def index(request):
    """Simple route to test out the app"""
    attachments = Attachment.objects.all()
    context = {
        "attachments": attachments,
    }
    return render(request, "index.html", context)


@csrf_exempt
@require_POST
def upload_file(request):
    files = request.FILES.getlist("file")
    urls = []

    for file in files:
        url = upload_to_s3(file)
        image, _ = Attachment.objects.get_or_create(url=url)
        urls.append(
            {"filename": image.filename, "url": image.signed_url})

    return JsonResponse({"urls": urls})
