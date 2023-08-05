"""
- Home page (list of images in our DB?)
- Image "details" page, a form for viewing, changing, or uploading an Image
- Image upload page
- A way to label an image
- Display the aggregate (sum) of the label "votes" for an image
- List the individual votes for an Image 
"""

from django.shortcuts import render, redirect

from rest_framework.decorators import api_view
from rest_framework.response import Response

# from django.template import RequestContext
# from django.http import HttpResponseRedirect
# from django.core.urlresolvers import reverse

from .models import Image
from .serializers import ImageSerializer
from .forms import FileUploadForm

from rest_framework import generics


def form_file_upload(request):
    if request.method == 'POST':
        form = FileUploadForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('index')
    else:
        form = FileUploadForm()
    return render(request, 'labeler/form_file_upload.html', {
        'form': form
    })


def index(request):
    images = Image.objects.all()
    return render(request, 'labeler/index.html', {'images': images})


@api_view(['GET'])
def image_list(request):
    """ A function based view that use the api_view decorator to add functionality to the view. """
    if request.method == 'GET':
        images = Image.objects.all()
        serializer = ImageSerializer(images, many=True)
        return Response(serializer.data)


class ListImages(generics.ListCreateAPIView):
    """ A class based view that inherits from the generics class.

    Creates REST views/forms for simple CRUD operations.
    """
    queryset = Image.objects.all()
    serializer_class = ImageSerializer
