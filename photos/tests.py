from django.test import TestCase
from datetime import datetime
# Create your tests here.
from .models import *


#  test categories class
class TestUser (TestCase):
    def setUp(self):
        self.vikki = User(username='vikki', password='akisijui')
        self.vikki.save()

    def tearDown(self):
        User.objects.all().delete()

    def test_instance(self):
        self.assertEqual(self.vikki.username, 'vikki')
        self.assertEqual(self.vikki.password, 'akisijui')
        self.assertTrue(isinstance(self.vikki, User))


#  test categories class
class TestUserProfile (TestCase):
    def setUp(self):

        self.vikki = User(username='vikki', password='akisijui')
        self.vikki.save()
        self.lord_stark = UserProfile(user=self.vikki, name='Victor Ireri',
                                      user_name='Lord_stark', bio='i care', email='vikkicoder@gmail.com')
        self.lord_stark.save_profile()

    def tearDown(self):
        UserProfile.objects.all().delete()

    def test_instance(self):
        self.assertEqual(self.lord_stark.name, 'Victor Ireri')
        self.assertEqual(self.lord_stark.user_name, 'Lord_stark')
        self.assertEqual(self.lord_stark.bio, 'i care')
        self.assertEqual(self.lord_stark.email, 'vikkicoder@gmail.com')
        self.assertTrue(isinstance(self.lord_stark, UserProfile))

    def test_save_profile(self):
        self.assertTrue(len(UserProfile.objects.all()) > 0)


class TestLocation (TestCase):
    def setUp(self):
        self.nai = Location(location='nairobi')
        self.nai.save_location

    def tearDown(self):
        Location.objects.all().delete()

    def test_instance(self):
        self.assertEqual(self.nai.location, 'nairobi')
        self.assertTrue(isinstance(self.nai, Location))


class TestPhoto (TestCase):
    def setUp(self):

        self.vikki = User(username='vikki', password='akisijui')
        self.vikki.save()
        self.waterfall = Photo(uploaded_by=self.vikki, photo='test.jpg',
                               caption='this is a test photo', post_date=datetime.utcnow())
        self.waterfall.save_photo(self.vikki)

    def tearDown(self):
        Photo.objects.all().delete()

    def test_instance(self):
        self.assertEqual(self.waterfall.uploaded_by, self.vikki)
        self.assertEqual(self.waterfall.photo, 'test.jpg')
        self.assertEqual(self.waterfall.caption, 'this is a test photo')
        self.assertTrue(isinstance(self.waterfall, Photo))

    def test_all_photos(self):
        self.assertTrue(len(Photo.objects.all()) > 0)

    def test_user_photos(self):
        self.assertTrue(len(Photo.user_photos(self.vikki)) > 0)

    def test_filter_by_search_term(self):
        self.assertTrue(len(Photo.filter_by_search_term('this')) > 0)

    def test_get_user_profile(self):
        self.assertTrue(len(Photo.get_user_profile(self.waterfall)) > 0)


class TestComment (TestCase):
    def setUp(self):

        self.vikki = User(username='vikki', password='akisijui')
        self.vikki.save()
        self.waterfall = Photo(uploaded_by=self.vikki, photo='test.jpg',
                               caption='this is a test photo', post_date=datetime.utcnow())
        self.waterfall.save_photo(self.vikki)
        self.comment = Comment(comment='this is comment')
        self.comment.save_comment(self.vikki, self.waterfall)

    def tearDown(self):
        Comment.objects.all().delete()

    def test_save_comment(self):
        self.assertTrue(isinstance(self.comment, Comment))

    def test_all_photo_comments(self):
        self.assertTrue(len(Comment.all_photo_comments(self.waterfall.id)) > 0)
