from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User

from timetracker.models import UserData, Span, Task


def create_user(username, *, token, password=None, email=None):
    if password is None:
        password = "password"

    if email is None:
        email = "email@example.com"

    user = User.objects.create_user(username=username, email=email, password=password)
    user.save()

    userdata = UserData(user=user, token=token)
    userdata.save()

    return user


def create_task(user, *, name, subtraction=False, count_multiple=False, allow_day_crossing=False,
                color=None, comment=None):
    if color is None:
        color = "#99DD99"

    task = Task(user=user, name=name, subtraction=subtraction, count_multiple=count_multiple,
                allow_day_crossing=allow_day_crossing, color=color, comment=comment)

    task.save()

    return task


class StartStopTestCase(TestCase):
    def setUp(self):
        self.c = Client()

    def tearDown(self):
        pass

    def test_start_task_with_empty_db(self):
        token = "abc123"
        slug = "testslug"
        rv = self.c.get(reverse("start", args=(token, slug)))
        assert rv.status_code == 404, "Starting a task with empty DB should return 404"

    def test_start_task(self):
        token = "abc123"
        arbitrary_slug = "testslug"

        user = create_user("test1", token=token)

        rv = self.c.get(reverse("start", args=(token, arbitrary_slug)))
        assert rv.status_code == 404, "Starting a task for a user without tasks should return 404"

        rv = self.c.get(reverse("start", args=("bogus_token", arbitrary_slug)))
        assert rv.status_code == 404, "Starting a task with invalid token should return 404"

        task = create_task(user, name="testing task")

        rv = self.c.get(reverse("start", args=(token, arbitrary_slug)))
        assert rv.status_code == 404, "Task start with valid token but invalid slug should return 404"

        rv = self.c.get(reverse("start", args=("bogus_token", task.slug)))
        assert rv.status_code == 404, "Task start with invalid token but valid slug should return 404"

        rv = self.c.get(reverse("start", args=(token, task.slug)))
        assert rv.status_code == 200, "Valid task start should return 200"

        rv = self.c.get(reverse("start", args=(token, task.slug)))
        assert rv.status_code == 400, "Repeated task start should return 400"

        rv = self.c.get(reverse("start", args=(token, arbitrary_slug)))
        assert rv.status_code == 404, "Repeated task start with valid token but invalid slug should return 404"

        rv = self.c.get(reverse("start", args=("bogus_token", task.slug)))
        assert rv.status_code == 404, "Repeated task start with invalid token but valid slug should return 404"

    def test_end_task_with_empty_db(self):
        token = "abc123"
        slug = "testslug"
        rv = self.c.get(reverse("end", args=(token, slug)))
        assert rv.status_code == 404, "Ending a task with empty DB should return 404"

    def test_end_task(self):
        token = "abc123"
        arbitrary_slug = "testslug"

        user = create_user("test1", token=token)
        task = create_task(user, name="testing task")
        rv = self.c.get(reverse("start", args=(token, task.slug)))
        assert rv.status_code == 200, "Valid task start should return 200"

        # test error cases
        rv = self.c.get(reverse("end", args=("bogus_token", task.slug)))
        assert rv.status_code == 404, "Task end with invalid token but valid slug should return 404"

        rv = self.c.get(reverse("end", args=(token, arbitrary_slug)))
        assert rv.status_code == 404, "Task end with valid token but invalid slug should return 404"

        # test valid cases
        rv = self.c.get(reverse("end", args=(token, task.slug)))
        assert rv.status_code == 200, "Valid task end should return 200"

        rv = self.c.get(reverse("end", args=(token, task.slug)))
        assert rv.status_code == 404, "Repeated task end should return 404"
