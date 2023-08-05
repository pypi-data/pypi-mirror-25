import requests

import yo_client.urls
import yo_client.request_parameters


class YoClient:
    def __init__(self, api_key):
        self.api_key = api_key

    def send_yo(self, username, text=None, link=None, coordinate=None):
        r = requests.post(url=yo_client.urls.SEND_YO_URL,
                          data=yo_client.request_parameters.RequestBodyBuilder.build_send_yo_body(username=username,
                                                                                                  api_token=self.api_key,
                                                                                                  text=text, link=link,
                                                                                                  coordinate=coordinate))

        r.raise_for_status()

        return r.json()

    def send_yo_to_all_subscribers(self, link=None):
        r = requests.post(url=yo_client.urls.SEND_YOS_TO_ALL_SUBSCRIBERS_URL,
                          data=yo_client.request_parameters.RequestBodyBuilder.build_send_yo_to_all_subscribers_body(
                              api_token=self.api_key, link=link
                          ))

        r.raise_for_status()

        return r.json()

    def create_account(self, username, password=None, callback_url=None, email=None, description=None, needs_location=False, welcome_link=None):
        r = requests.post(url=yo_client.urls.CREATE_ACCOUNT_URL,
                          data=yo_client.request_parameters.RequestBodyBuilder.build_account_creation_body(
                              username=username, api_token=self.api_key, password=password, callback_url=callback_url,
                              email=email, description=description, needs_location=needs_location,
                              welcome_link=welcome_link)
                          )

        r.raise_for_status()

        return r.json()

    def username_exists(self, username):
        r = requests.get(url=yo_client.urls.USERNAME_EXISTS_URL,
                         data=yo_client.request_parameters.RequestQueryParametersBuilder.build_username_exists_query_parameters(
                             username=username, api_token=self.api_key)
                         )

        r.raise_for_status()

        return r.json()

    def get_subscribers_count(self):
        r = requests.get(url=yo_client.urls.SUBSCRIBERS_COUNT_URL, data={"api_token": self.api_key})

        r.raise_for_status()

        return r.json()
