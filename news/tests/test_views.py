# from django.test import TestCase
# from django.urls import reverse
# from unittest.mock import patch
# from news.services import load_mock_news
#
#
# class NewsViewTests(TestCase):
#     def setUp(self):
#         # Mock the news data for testing
#         self.mock_data = load_mock_news()
#
#     @patch('news.services.get_news', return_value=None)
#     def test_articles_view_no_news(self, mock_get_news):
#         """
#         Test the articles view when no news is available.
#         """
#         response = self.client.get(reverse('news:articles'))
#
#         # Check that we get a 200 OK response
#         self.assertEqual(response.status_code, 200)
#
#         # Check that the 'No news available' message is in the response
#         self.assertContains(response, 'No news available')
#
#     @patch('news.services.get_news', return_value=[])
#     def test_articles_view_empty_news(self, mock_get_news):
#         """
#         Test the articles view when the fetched news data is empty.
#         """
#         response = self.client.get(reverse('news:articles'))
#
#         # Check that we get a 200 OK response
#         self.assertEqual(response.status_code, 200)
#
#         # Check that the 'No news available' message is in the response
#         self.assertContains(response, 'No news available')
#
#     @patch('news.services.get_news', return_value=[{
#         'title': 'Test News 1',
#         'text': 'Text for Test News 1',
#         'date': '2024-12-15',
#         'source': 'Source 1',
#         'url': 'http://example.com/news1',
#         'summary': 'Summary of news 1',
#         'image': 'http://example.com/image1.jpg',
#     }, {
#         'title': 'Test News 2',
#         'text': 'Text for Test News 2',
#         'date': '2024-12-15',
#         'source': 'Source 2',
#         'url': 'http://example.com/news2',
#         'summary': 'Summary of news 2',
#         'image': 'http://example.com/image2.jpg',
#     }, {
#         'title': 'Test News 3',
#         'text': 'Text for Test News 3',
#         'date': '2024-12-15',
#         'source': 'Source 3',
#         'url': 'http://example.com/news3',
#         'summary': 'Summary of news 3',
#         'image': 'http://example.com/image3.jpg',
#     }, {
#         'title': 'Test News 4',
#         'text': 'Text for Test News 4',
#         'date': '2024-12-15',
#         'source': 'Source 4',
#         'url': 'http://example.com/news4',
#         'summary': 'Summary of news 4',
#         'image': 'http://example.com/image4.jpg',
#     }])
#     def test_articles_view_with_news(self, mock_get_news):
#         """
#         Test the articles view when news data is available.
#         """
#         response = self.client.get(reverse('news:articles'))
#
#         # Check that we get a 200 OK response
#         self.assertEqual(response.status_code, 200)
#
#         # Check that the page contains articles
#         for article in self.mock_data:
#             self.assertContains(response, article['title'])
#
#     @patch('news.services.get_news', return_value=[{
#         'title': 'Test News 1',
#         'text': 'Text for Test News 1',
#         'date': '2024-12-15',
#         'source': 'Source 1',
#         'url': 'http://example.com/news1',
#         'summary': 'Summary of news 1',
#         'image': 'http://example.com/image1.jpg',
#     }, {
#         'title': 'Test News 2',
#         'text': 'Text for Test News 2',
#         'date': '2024-12-15',
#         'source': 'Source 2',
#         'url': 'http://example.com/news2',
#         'summary': 'Summary of news 2',
#         'image': 'http://example.com/image2.jpg',
#     }, {
#         'title': 'Test News 3',
#         'text': 'Text for Test News 3',
#         'date': '2024-12-15',
#         'source': 'Source 3',
#         'url': 'http://example.com/news3',
#         'summary': 'Summary of news 3',
#         'image': 'http://example.com/image3.jpg',
#     }, {
#         'title': 'Test News 4',
#         'text': 'Text for Test News 4',
#         'date': '2024-12-15',
#         'source': 'Source 4',
#         'url': 'http://example.com/news4',
#         'summary': 'Summary of news 4',
#         'image': 'http://example.com/image4.jpg',
#     }])
#     def test_articles_view_pagination(self, mock_get_news):
#         """
#         Test pagination when there are more than 3 articles.
#         """
#         response = self.client.get(reverse('news:articles') + '?page=1')
#
#         # Check that we get a 200 OK response
#         self.assertEqual(response.status_code, 200)
#
#         # Check that the correct number of articles is shown
#         self.assertContains(response, 'Test News 1')
#         self.assertContains(response, 'Test News 2')
#         self.assertContains(response, 'Test News 3')
#         self.assertContains(response, 'Test News 4')
#
#         # Check pagination
#         self.assertContains(response, 'page=2')  # Ensure that pagination exists
