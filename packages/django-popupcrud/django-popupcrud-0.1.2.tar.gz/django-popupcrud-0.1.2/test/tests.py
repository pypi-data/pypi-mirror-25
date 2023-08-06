# -*- coding: utf-8 -*-
import re
import json

from django.test import TestCase
from django.core.urlresolvers import reverse
from django.http import JsonResponse

from .models import Author
from .views import AuthorCrudViewset

RE_CREATE_EDIT_FORM = r"\n<form class='form-horizontal' id='create-edit-form' action='{0}' method='post' accept-charset='utf-8'>.*</form>\n"

class PopupCrudViewSetTests(TestCase):

    def test_settings(self):
        from popupcrud.views import POPUPCRUD
        self.assertEquals(POPUPCRUD['base_template'], "test/base.html")

    def test_template(self):
        author = Author.objects.create(name="John", age=26)
        response = self.client.get(reverse("authors"))
        self.assertTemplateUsed(response, "popupcrud/list.html")
        # template should have the three embedded bootstrap modals
        modal_patterns = [
            r'<div class="modal fade".*id="create-edit-modal"',
            r'<div class="modal fade".*id="delete-modal"',
            r'<div class="modal fade".*id="delete-result-modal"',
        ]
        for pattern in modal_patterns:
            self.assertTrue(
                re.search(pattern, response.content.decode('utf-8')))

    def test_list_display(self):
        author = Author.objects.create(name="John", age=26)
        response = self.client.get(reverse("authors"))
        self.assertContains(response, "<th>Name</th>")
        self.assertContains(response, "<th>Age</th>")
        self.assertContains(response, "<th>Half Age</th>")
        self.assertContains(response, "<th>Double Age</th>")
        # also tests the get_obj_name() method
        self.assertTrue(
            re.search(r'<td>John.*/div></td>', response.content.decode('utf-8')))
        #self.assertContains(response, "<td>John.*/div></td>")
        self.assertContains(response, "<td>26</td>")
        self.assertContains(response, "<td>13</td>") # Author.half_age
        self.assertContains(response, "<td>52</td>") # AuthorCrudViewSet.double_age

    def test_get_obj_name(self):
        # Also tests that unicode characters are rendered correctly
        author = Author.objects.create(name="何瑞理", age=46)
        response = self.client.get(reverse("authors"))
        self.assertContains(response, "<td>何瑞理<div data-name=\'何瑞理 - 46\'></div></td>")

    def test_page_title(self):
        author = Author.objects.create(name="John", age=26)
        response = self.client.get(reverse("authors"))
        self.assertEquals(response.context['page_title'], "Author List")

    def test_empty_data(self):
        response = self.client.get(reverse("authors"))
        self.assertNotContains(response, "<table class='table")
        self.assertNotContains(response, "<th>Name</th>")
        self.assertNotContains(response, "<th>Age</th>")
        self.assertContains(response, "No items")

    def test_urls(self):
        for _ in range(0, 10):
            Author.objects.create(name="John", age=25)
        response = self.client.get(reverse("authors"))
        self.assertContains(response, "New Author")
        self.assertContains(response, AuthorCrudViewset.new_url)
        for obj in Author.objects.all():
            self.assertContains(response, AuthorCrudViewset().get_edit_url(obj))
            self.assertContains(response, AuthorCrudViewset().get_delete_url(obj))

    def test_pagination(self):
        for _ in range(0, 30):
            Author.objects.create(name="John", age=25)
        response = self.client.get(reverse("authors"))
        po = response.context['page_obj']
        self.assertEqual(po.number, 1)
        self.assertTrue(po.has_next())
        self.assertFalse(po.has_previous())
        self.assertEqual(po.paginator.num_pages, 3)

    def test_create_form_template(self):
        # when requested through an AJAX, should only contain the <form></form>
        url = reverse("new-author")
        response = self.client.get(url, HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        match = re.search(RE_CREATE_EDIT_FORM.format(url),
                          response.content.decode('utf-8'), re.DOTALL)
        self.assertEqual(match.pos, 0)

    def test_update_form_template(self):
        # when requested through an AJAX, should only contain the <form></form>
        john = Author.objects.create(name="John", age=25)
        url = reverse("edit-author", kwargs={'pk': john.pk})
        response = self.client.get(url, HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        match = re.search(RE_CREATE_EDIT_FORM.format(url),
                          response.content.decode('utf-8'), re.DOTALL)
        self.assertEqual(match.pos, 0)

    def test_create(self):
        url = reverse("new-author")
        response = self.client.post(
            url,
            data={'name': 'John', 'age': 55},
            HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        john = Author.objects.get(name='John', age=55)
        result = json.loads(response.content.decode('utf-8'))
        self.assertEquals(result, {'name': 'John', 'pk': john.pk})

    def test_update(self):
        john = Author.objects.create(name="John", age=25)
        url = reverse("edit-author", kwargs={'pk': john.pk})
        response = self.client.post(
            url,
            data={'name': 'Peter', 'age': 35},
            HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        result = json.loads(response.content.decode('utf-8'))
        self.assertEquals(result, {'name': 'Peter', 'pk': john.pk})
        john.refresh_from_db()
        self.assertEquals(john.name, 'Peter')

