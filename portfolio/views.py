from django.shortcuts import render


def home(request):
    return render(request, 'portfolio/home.html')


def about(request):
    return render(request, 'portfolio/about.html')


def experience(request):
    return render(request, 'portfolio/experience.html')


def projects(request):
    return render(request, 'portfolio/projects.html')


def resume(request):
    return render(request, 'portfolio/resume.html')


def contact(request):
    return render(request, 'portfolio/contact.html')
