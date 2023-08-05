class BaseWithoutLoginMixin(object):
    url = None

    def test_url_open(self):
        # self.client.logout()
        self.client.get(self.url)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
