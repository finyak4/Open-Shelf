from library import models
from django.core.management.base import BaseCommand

class Command(BaseCommand):
    help = 'Seed the database with initial data'

    def handle(self, *args, **kwargs):
        models.Genre.objects.all().delete()
        models.Book.objects.all().delete()
        models.Author.objects.all().delete()

        genres = ['Science Fiction', 'Fantasy', 'Mystery', 'Romance', 'Horror']
        for genre_name in genres:
            models.Genre.objects.create(name=genre_name)

        authors = ['Isaac Asimov', 'J.K. Rowling', 'Agatha Christie', 'Jane Austen', 'Stephen King']
        descriptions = [
            "Prolific science fiction author known for the Foundation series.",
            "British author, best known for the Harry Potter series.",
            "Renowned mystery writer, famous for Hercule Poirot and Miss Marple.",
            "Classic novelist known for works like Pride and Prejudice.",
            "Master of horror fiction, author of The Shining and IT."
        ]
        for author_name, desc in zip(authors, descriptions):
            models.Author.objects.create(name=author_name, description=desc)

        for i in range(1, 6):
            models.Book.objects.create(
                title=f"Foundation Vol. {i}",
                author=models.Author.objects.get(name="Isaac Asimov"),
                description="A complex saga of humans scattered on planets throughout the galaxy all living under the rule of the Galactic Empire.",
                availability=5,
                publication_year=1951,
                genre=models.Genre.objects.get(name="Science Fiction"),
                cover_image="https://cdn.kobo.com/book-images/4a4b2cb4-bde2-40be-8165-9b0c7c8bf191/353/569/90/False/foundation-the-foundation-trilogy-book-1-1.jpg"
            )

            models.Book.objects.create(
                title=f"Harry Potter and the Sorcerer's Stone Vol. {i}",
                author=models.Author.objects.get(name="J.K. Rowling"),
                description="The first book in the Harry Potter series, introducing us to the young wizard and his adventures at Hogwarts.",
                availability=10,
                publication_year=1997,
                genre=models.Genre.objects.get(name="Fantasy"),
                cover_image="https://static.wikia.nocookie.net/qghficsimjkaeibhfztnpjrqiezhzuadzsjxwpnxusefbthfes/images/a/a6/C2BBA2A0-8850-42FC-A499-F6F80E92EB0E.webp/revision/latest?cb=20210812200542"
            )
            models.Book.objects.create(
                title=f"Murder on the Orient Express Vol. {i}",
                author=models.Author.objects.get(name="Agatha Christie"),
                description="Detective Hercule Poirot must solve a murder on a snowbound train filled with suspects.",
                availability=4,
                publication_year=1934,
                genre=models.Genre.objects.get(name="Mystery"),
                cover_image="https://m.media-amazon.com/images/I/418gG3dQKyL._SY445_SX342_.jpg"
            )

            models.Book.objects.create(
                title=f"Pride and Prejudice Vol. {i}",
                author=models.Author.objects.get(name="Jane Austen"),
                description="A classic romance novel exploring love, class, and misunderstandings in Regency England.",
                availability=6,
                publication_year=1813,
                genre=models.Genre.objects.get(name="Romance"),
                cover_image="https://www.imdb.com/title/tt0414387/mediaviewer/rm1343528192/?ref_=tt_ov_i"
            )

            models.Book.objects.create(
                title=f"IT Vol. {i}",
                author=models.Author.objects.get(name="Stephen King"),
                description="A horror novel about a shape-shifting entity that terrorizes children in Derry, Maine.",
                availability=4,
                publication_year=1986,
                genre=models.Genre.objects.get(name="Horror"),
                cover_image="https://image.ceneostatic.pl/data/products/56084131/i-it-king-stephen.jpg"
            )

            models.Book.objects.create(
                title=f"The Robots of Dawn Vol. {i}",
                author=models.Author.objects.get(name="Isaac Asimov"),
                description="A sci-fi mystery where detective Elijah Baley must solve a murder on a distant planet populated by robots.",
                availability=7,
                publication_year=1983,
                genre=models.Genre.objects.get(name="Science Fiction"),
                cover_image="https://m.media-amazon.com/images/I/71Vm4mFih+L._UF1000,1000_QL80_.jpg"
            )

            models.Book.objects.create(
                title=f"Harry Potter and the Chamber of Secrets Vol. {i}",
                author=models.Author.objects.get(name="J.K. Rowling"),
                description="The second book in the Harry Potter series, following Harry’s adventures as the Chamber of Secrets is opened at Hogwarts.",
                availability=8,
                publication_year=1998,
                genre=models.Genre.objects.get(name="Fantasy"),
                cover_image="https://a.allegroimg.com/original/11c3ea/2e135999485b959b76099ac78ec9/J-K-Rowling-Harry-Potter-and-the-Chamber-of-Secrets"
            )

            models.Book.objects.create(
                title=f"And Then There Were None Vol. {i}",
                author=models.Author.objects.get(name="Agatha Christie"),
                description="Ten strangers are invited to a remote island, where they are killed one by one in this chilling mystery.",
                availability=5,
                publication_year=1939,
                genre=models.Genre.objects.get(name="Mystery"),
                cover_image="https://m.media-amazon.com/images/I/71EXMl7hbBL._UF1000,1000_QL80_.jpg"
            )

            models.Book.objects.create(
                title=f"Sense and Sensibility Vol. {i}",
                author=models.Author.objects.get(name="Jane Austen"),
                description="A romantic drama about the Dashwood sisters as they navigate love and societal expectations.",
                availability=4,
                publication_year=1811,
                genre=models.Genre.objects.get(name="Romance"),
                cover_image="https://m.media-amazon.com/images/M/MV5BY2MyZWJhNjktMWQ2My00OTgwLWI1NjEtYjUzM2M2N2M4Mzc4XkEyXkFqcGc@._V1_.jpg"
            )

            models.Book.objects.create(
                title=f"The Shining Vol. {i}",
                author=models.Author.objects.get(name="Stephen King"),
                description="A psychological horror novel about a family isolated in a haunted hotel.",
                availability=2,
                publication_year=1977,
                genre=models.Genre.objects.get(name="Horror"),
                cover_image="https://m.media-amazon.com/images/M/MV5BNmM5ZThhY2ItOGRjOS00NzZiLWEwYTItNDgyMjFkOTgxMmRiXkEyXkFqcGc@._V1_FMjpg_UX1000_.jpg"
            )

        self.stdout.write(self.style.SUCCESS('Database seeded successfully.'))