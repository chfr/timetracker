import datetime
from argparse import _AppendAction

from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseBadRequest
from django.utils import timezone

from .models import UserData, Span, Task


class TableCell:
    def __init__(self):
        self._spans = []
        self._firsts = {}
        self._lasts = {}

    @property
    def spans(self):
        return self._spans

    def add_span(self, index, span):
        self._spans.append((index, span))

    def has_span(self, span):
        return span in self._spans

@login_required
def index(request):
    tasks = Task.objects.filter(user=request.user)

    # 24*7 matrix where each cell represents one hour in a week
    # table[15][0] is the hour between 15:00 and 16:00 on Monday
    table = [[None] * 7 for _ in range(24)]

    tz = timezone.get_default_timezone()
    dt = datetime.datetime.utcnow()

    delta = tz.utcoffset(dt)
    offset_hours = int(abs(delta.total_seconds())) // 3600  # dirty!


    for task in tasks:
        spans = Span.objects.filter(task=task)
        for span in spans:
            if span.has_ended():
                dow = span.start.weekday()  # day of week
                start_hour = span.start.hour + offset_hours
                end_hour = span.end.hour + offset_hours

                end_dow = span.end.weekday()
                day_diff = end_dow - dow
                end_hour += day_diff * 24

                if not table[start_hour][dow]:
                    table[start_hour][dow] = TableCell()

                hour = start_hour

                for i in range(end_hour - start_hour + 1):

                    if hour > 23:
                        hour = 0
                        dow = (dow + 1) % 7  # if this crosses a week boundary there will be blood

                    if not table[hour][dow]:
                        table[hour][dow] = TableCell()
                    if i == end_hour - start_hour:
                        table[hour][dow].add_span(-1, span)
                    else:
                        table[hour][dow].add_span(i, span)

                    hour += 1

    context = {"table": table, "hours": range(24), "days": range(7)}
    return render(request, "timetracker/index.html", context)


@login_required
def tasks(request):
    tasks = Task.objects.filter(user=request.user)

    context = {"tasks": tasks}
    return render(request, "timetracker/tasks.html", context)


@login_required
def task(request, slug):
    context = {}
    return render(request, "timetracker/task.html", context)


@login_required
def spans(request):
    tasks = Task.objects.filter(user=request.user)
    spans = Span.objects.filter(task__in=tasks)

    context = {"spans": spans}
    return render(request, "timetracker/spans.html", context)


@login_required
def span(request, span_id):
    context = {}
    return render(request, "timetracker/span.html", context)


@login_required
def settings(request):
    context = {}
    return render(request, "timetracker/settings.html", context)


def start(request, token, slug):
    user = get_object_or_404(User, userdata__token=token)
    task = get_object_or_404(Task, user=user, slug=slug)

    if Span.objects.filter(task=task, end=None):
        return HttpResponseBadRequest("duplicate task start")

    span = Span(task=task)  # automatically sets start timestamp to now()
    span.save()

    return HttpResponse("OK")


def end(request, token, slug):
    user = get_object_or_404(User, userdata__token=token)
    task = get_object_or_404(Task, user=user, slug=slug)
    span = get_object_or_404(Span, task=task, end=None)

    span.end = timezone.now()
    span.save()

    return HttpResponse("OK")



