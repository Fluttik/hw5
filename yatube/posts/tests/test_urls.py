from django.contrib.auth import get_user_model
from django.test import TestCase, Client
from http import HTTPStatus
from datetime import date
from posts.models import Group, Post, User


User = get_user_model()


class StaticURLTests(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = User.objects.create_user(username='TestUser')
        cls.group = Group.objects.create(
            title='Тестовая группа',
            slug='test-slug',
            description='test desc'
        )
        cls.post = Post.objects.create(
            text='Тестовый текст',
            pub_date=date.today(),
            author=cls.user,
            group=cls.group
            #group=Group.objects.create(title='Тестовая группа',
            #                          slug='test-slug',
            #                           description='test desc')
        )

    def setUp(self):
        self.guest_client = Client()
        self.user = User.objects.get(username='TestUser')
        self.authorized_client = Client()
        self.authorized_client.force_login(self.user)

    def test_home_url_exists_at_desired_location(self):
        """Страница / """
        response = self.guest_client.get('/')
        self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_group_url_exists_at_desired_location(self):
        """ Страница /group/slug """
        response = self.guest_client.get(f'/group/{self.group.slug}')
        self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_profile_url_exists_at_desired_location(self):
        """ Страница /profile/<username> """
        response = self.guest_client.get('/profile/TestUser')
        self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_post_detail_url_exists_at_desired_location(self):
        """ Страница /posts/<post_id> """
        response = self.guest_client.get(f'/posts/{self.post.id}')
        self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_author_post_edit(self):
        """ Изменение поста авторизованным пользователем являющимся автором """
        response = self.authorized_client.get(f'/posts/{self.post.id}/edit')
        self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_create_redirect_anonymous(self):
        """ Создание поста анономом """
        response = self.guest_client.get('/create', follow=True)
        self.assertRedirects(response, '/auth/login/?next=/create/')

    def test_author_post_edit_redirect_anonymous(self):
        """ Изменение поста анонимом """
        response = self.guest_client.get(f'/posts/{self.post.id}/edit', follow=True)
        self.assertRedirects(response, f'/auth/login/?next=/posts/{self.post.id}/edit/')

    def test_author_post_edit_redirect_notauthor(self):
        """ Изменение поста не автором поста """
        ...

    def test_404(self):
        """ Запрос несуществуюзей страницы """
        response = self.guest_client.get('/unxexisting_page/')
        self.assertEquals(response.status_code, HTTPStatus.NOT_FOUND)

    def test_urls_uses_correct_template(self):
        templates_url_names = {
            '/': 'posts/index.html',
            f'/group/{self.group.slug}': 'posts/group_list.html',
            f'/profile/{self.user}': 'posts/profile.html',
            f'/posts/{self.post.id}': 'posts/post_detail.html',
            f'/posts/{self.post.id}/edit': 'posts/create_post.html',
            '/create': 'posts/create_post.html',
        }
        for address, template in templates_url_names:
            with self.subTest(address=address):
                response = self.authorized_client.get(address)
                self.assertTemplateUsed(response, template)
