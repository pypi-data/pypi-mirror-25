"""
Auto generated code

"""

import json
from snapp_email.datacontract.classes import Feed_19
from snapp_email.datacontract.utils import export_dict, fill


class Feed_19Endpoint:
    def __init__(self, api_client):
        self.api_client = api_client
    
    def options(self, impersonate_user_id=None, accept_type=None):
        """
        Retrieve options available for resource 'Feed_19'.
        
        :param impersonate_user_id: 
        :type impersonate_user_id: str
        
        :param accept_type: 
        :type accept_type: str
        
        :return: 
        :rtype: Feed_19
        """
        url_parameters = {
        }
        endpoint_parameters = {
        }
        endpoint = 'feed'.format(**endpoint_parameters)
        add_headers = {
            'Content-Type': 'application/vnd.4thoffice.feed-5.12+json',
            'Accept': 'application/vnd.4thoffice.feed-5.12+json' if accept_type is None else accept_type,
        }
        response = self.api_client.api_call('options', endpoint, url_parameters, add_headers, impersonate_user_id=impersonate_user_id)
        
        return fill(Feed_19, response.json(), content_type=response.headers['Content-Type'], silence_exceptions=self.api_client.silence_fill_exceptions)
    
    def get(self, feedscope, feedidentity, size, offset, badgeUnreadVersion=None, returnChatAsCard=None, returnForwardedCopyPosts=None, impersonate_user_id=None, accept_type=None):
        """
        Retrieve feed resource.
        
        :param feedscope: Specify feed scope.
            Available values:
            - Stream
            - Others
            - All
        :type feedscope: String
        
        :param feedidentity: Specify feed id.
        :type feedidentity: String
        
        :param size: Specify size of requested page.
        :type size: Int32
        
        :param offset: Specify offset of requested page.
        :type offset: Int32
        
        :param badgeUnreadVersion: Version string that defines which logic to use for setting of unread badge count value on menu items and unread separator on feed. Available values are: 'V18', 'V19'.
        :type badgeUnreadVersion: String
        
        :param returnChatAsCard: Return all the chat posts of a given stream packed into one discussion card.
        :type returnChatAsCard: Boolean
        
        :param returnForwardedCopyPosts: Return copied posts on forwarded discussion card.
        :type returnForwardedCopyPosts: Boolean
        
        :param impersonate_user_id: 
        :type impersonate_user_id: str
        
        :param accept_type: 
        :type accept_type: str
        
        :return: 
        :rtype: Feed_19
        """
        url_parameters = {
            'feedscope': feedscope,
            'feedidentity': feedidentity,
            'badgeUnreadVersion': badgeUnreadVersion,
            'returnChatAsCard': returnChatAsCard,
            'returnForwardedCopyPosts': returnForwardedCopyPosts,
            'size': size,
            'offset': offset,
        }
        endpoint_parameters = {
        }
        endpoint = 'feed'.format(**endpoint_parameters)
        add_headers = {
            'Content-Type': 'application/vnd.4thoffice.feed-5.12+json',
            'Accept': 'application/vnd.4thoffice.feed-5.12+json' if accept_type is None else accept_type,
        }
        response = self.api_client.api_call('get', endpoint, url_parameters, add_headers, impersonate_user_id=impersonate_user_id)
        
        return fill(Feed_19, response.json(), content_type=response.headers['Content-Type'], silence_exceptions=self.api_client.silence_fill_exceptions)
    
    def get_2(self, feedscope, feedidentity, sinceId, size, offset, sortDirection=None, badgeUnreadVersion=None, returnChatAsCard=None, returnForwardedCopyPosts=None, impersonate_user_id=None, accept_type=None):
        """
        Retrieve feed resource incrementally since arbitrary post id.
        
        :param feedscope: Specify feed scope.
            Available values:
            - Stream
            - Others
            - All
        :type feedscope: String
        
        :param feedidentity: Specify feed id.
        :type feedidentity: String
        
        :param sinceId: Specify since id. That is an id of a resource from which incremental list load should take place.
        :type sinceId: String
        
        :param size: Specify size of requested page.
        :type size: Int32
        
        :param offset: Specify offset of requested page.
        :type offset: Int32
        
        :param sortDirection: Specify sort direction.
            Available values:
            - Ascending
            - Descending
        :type sortDirection: String
        
        :param badgeUnreadVersion: Version string that defines which logic to use for setting of unread badge count value on menu items and unread separator on feed. Available values are: 'V18', 'V19'.
        :type badgeUnreadVersion: String
        
        :param returnChatAsCard: Return all the chat posts of a given stream packed into one discussion card.
        :type returnChatAsCard: Boolean
        
        :param returnForwardedCopyPosts: Return copied posts on forwarded discussion card.
        :type returnForwardedCopyPosts: Boolean
        
        :param impersonate_user_id: 
        :type impersonate_user_id: str
        
        :param accept_type: 
        :type accept_type: str
        
        :return: 
        :rtype: Feed_19
        """
        url_parameters = {
            'feedscope': feedscope,
            'feedidentity': feedidentity,
            'sinceId': sinceId,
            'sortDirection': sortDirection,
            'badgeUnreadVersion': badgeUnreadVersion,
            'returnChatAsCard': returnChatAsCard,
            'returnForwardedCopyPosts': returnForwardedCopyPosts,
            'size': size,
            'offset': offset,
        }
        endpoint_parameters = {
        }
        endpoint = 'feed'.format(**endpoint_parameters)
        add_headers = {
            'Content-Type': 'application/vnd.4thoffice.feed-5.12+json',
            'Accept': 'application/vnd.4thoffice.feed-5.12+json' if accept_type is None else accept_type,
        }
        response = self.api_client.api_call('get', endpoint, url_parameters, add_headers, impersonate_user_id=impersonate_user_id)
        
        return fill(Feed_19, response.json(), content_type=response.headers['Content-Type'], silence_exceptions=self.api_client.silence_fill_exceptions)
