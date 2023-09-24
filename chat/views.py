from django.shortcuts import render
from django.http import HttpRequest
from django.contrib.auth.decorators import login_required


@login_required
def visit(request: HttpRequest):
    return render(
        request=request,
        template_name='chat/index.html', 
    )