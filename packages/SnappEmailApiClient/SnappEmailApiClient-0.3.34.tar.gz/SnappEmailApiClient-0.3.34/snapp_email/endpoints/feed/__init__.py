from .Feed_22Endpoint import Feed_22Endpoint
from .Feed_20Endpoint import Feed_20Endpoint
from .Feed_19Endpoint import Feed_19Endpoint
from .DiscussionSeparatorUnread_18Endpoint import DiscussionSeparatorUnread_18Endpoint


class FeedEndpoint:
    def __init__(self, api_client):
        self._api_client = api_client

    @property
    def Feed_22(self):
        """
        :return: Feed_22Endpoint
        """
        return Feed_22Endpoint(self._api_client)
        
    @property
    def Feed_20(self):
        """
        :return: Feed_20Endpoint
        """
        return Feed_20Endpoint(self._api_client)
        
    @property
    def Feed_19(self):
        """
        :return: Feed_19Endpoint
        """
        return Feed_19Endpoint(self._api_client)
        
    @property
    def DiscussionSeparatorUnread_18(self):
        """
        :return: DiscussionSeparatorUnread_18Endpoint
        """
        return DiscussionSeparatorUnread_18Endpoint(self._api_client)
        