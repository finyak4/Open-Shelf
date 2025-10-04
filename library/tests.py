from django.test import TestCase
from library import models

# Create your tests here.

class LibraryTests(TestCase):
    def setUp(self):
        self.author1 = models.Author.objects.create(name="Test Author")
        self.genre1 = models.Genre.objects.create(name="Fiction")

        self.author2 = models.Author.objects.create(name="Another Author")
        self.genre2 = models.Genre.objects.create(name="Non-Fiction")

        self.book1 = models.Book.objects.create(
            title="Test Book",
            author=self.author1,
            description="This is a test book description." * 10,
            availability=5,
            publication_year=2020,
            genre=self.genre1,
            cover_image="http://example.com/cover.jpg"
        )
        self.book2 = models.Book.objects.create(
            title="Another Book",
            author=self.author2,
            description="This is another book description." * 10,
            availability=0,
            publication_year=2018,
            genre=self.genre2,
            cover_image="http://example.com/another_cover.jpg"
        )

    def test_library_filters(self):
        response = self.client.get('/?author=Test+Author')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Test Book")
        self.assertNotContains(response, "Another Book")

        response = self.client.get('/?genre=Fiction')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Test Book")
        self.assertNotContains(response, "Another Book")

        response = self.client.get('/?available=true')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Test Book")
        self.assertNotContains(response, "Another Book")

        response = self.client.get('/?available=false')
        self.assertEqual(response.status_code, 200)
        self.assertNotContains(response, "Test Book")
        self.assertContains(response, "Another Book")    

    def test_add_book_valid(self):
        response = self.client.post('/', {
            'title': "New Book",
            'author': "New Author",
            'description': "This is a new book description." * 10,
            'availability': 3,
            'publication_year': 2021,
            'genre': "New Genre",
            'cover_image': "http://example.com/new_cover.jpg"
        })
        self.assertEqual(response.status_code, 302)
        self.assertTrue(models.Book.objects.filter(title="New Book").exists())
        self.assertTrue(models.Author.objects.filter(name="New Author").exists())
        self.assertTrue(models.Genre.objects.filter(name="New Genre").exists())

    def test_add_book_invalid(self):
        response = self.client.post('/', {
            'title': "",
            'author': "Invalid Author",
            'description': "Short desc",
            'availability': -1,
            'publication_year': 21,
            'genre': "New Genre",
            'cover_image': "not_a_url"
        })
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Form is not valid. Book was not added.")
        self.assertFalse(models.Book.objects.filter(title="").exists())
        self.assertFalse(models.Author.objects.filter(name="Invalid Author").exists())
        self.assertFalse(models.Genre.objects.filter(name="New Genre").exists())

    def test_edit_book_valid(self):
        response = self.client.put(f'/book/{self.book1.id}/', 
            data={
                'title': "Updated Test Book",
                'author': "Updated Author",
                'description': "Updated description." * 10,
                'availability': 10,
                'year': 2022,
                'genre': "Updated Genre",
                'url': "http://example.com/updated_cover.jpg"
            },
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 200)
        self.book1.refresh_from_db()
        self.assertEqual(self.book1.title, "Updated Test Book")
        self.assertEqual(self.book1.author.name, "Updated Author")
        self.assertEqual(self.book1.description, "Updated description." * 10)
        self.assertEqual(self.book1.availability, 10)
        self.assertEqual(self.book1.publication_year, 2022)
        self.assertEqual(self.book1.genre.name, "Updated Genre")
        self.assertEqual(self.book1.cover_image, "http://example.com/updated_cover.jpg")    

    def test_edit_book_invalid(self):
        response = self.client.put(f'/book/{self.book1.id}/', 
            data={
                'title': "",
                'author': "Another Invalid Author",
                'description': "Short desc",
                'availability': -5,
                'year': 99,
                'genre': "Another Genre",
                'url': "invalid_url"
            },
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 400) 
        self.book1.refresh_from_db()
        self.assertNotEqual(self.book1.title, "")
        self.assertNotEqual(self.book1.author.name, "Another Invalid Author")
        self.assertNotEqual(self.book1.description, "Short desc")
        self.assertNotEqual(self.book1.availability, -5)
        self.assertNotEqual(self.book1.publication_year, 99)
        self.assertNotEqual(self.book1.genre.name, "Another Genre")
        self.assertNotEqual(self.book1.cover_image, "invalid_url")    