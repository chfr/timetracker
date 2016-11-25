from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.http import HttpResponse


@login_required
def index(request):
    context = {}
    return render(request, "timetracker/index.html", context)


@login_required
def tasks(request):
    context = {}
    return render(request, "timetracker/tasks.html", context)


@login_required
def task(request, slug):
    context = {}
    return render(request, "timetracker/task.html", context)


@login_required
def spans(request):
    context = {}
    return render(request, "timetracker/spans.html", context)


@login_required
def span(request, span_id):
    context = {}
    return render(request, "timetracker/span.html", context)


@login_required
def settings(request):
    context = {}
    return render(request, "timetracker/settings.html", context)
