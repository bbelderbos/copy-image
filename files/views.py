from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST

from .aws import upload_to_s3
from .models import Attachment


def index(request):
    """Simple route to test out the app"""
    return render(request, "index.html")


@csrf_exempt
@require_POST
def upload_file(request):
    post = request.POST

    files = request.FILES.getlist("file")
    print("files")
    print(files)

    urls = []
    for file in files:
        url = upload_to_s3(file)
        image, _ = Attachment.objects.get_or_create(url=url)
        urls.append(
            {"filename": image.filename,
             "url": image.signed_url}
        )

    plural = "" if len(files) == 1 else "s"
    files_str = ", ".join([file.name for file in files])
    text = f"uploaded the following file{plural}: {files_str}"

    context = {
        "urls": urls,
    }
    return JsonResponse(context)


