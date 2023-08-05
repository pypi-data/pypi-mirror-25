"""
Auto generated code

"""

import json
from snapp_email.datacontract.classes import MenuItem_21
from snapp_email.datacontract.utils import export_dict, fill


class MenuItem_21Endpoint:
    def __init__(self, api_client):
        self.api_client = api_client
    
    def options(self, impersonate_user_id=None, accept_type=None):
        """
        Retrieve options available for resource 'MenuItem_20'.
        
        :param impersonate_user_id: 
        :type impersonate_user_id: str
        
        :param accept_type: 
        :type accept_type: str
        
        :return: 
        :rtype: MenuItem_21
        """
        url_parameters = {
        }
        endpoint_parameters = {
        }
        endpoint = 'navigation'.format(**endpoint_parameters)
        add_headers = {
            'Content-Type': 'application/vnd.4thoffice.menu.item-v5.17+json',
            'Accept': 'application/vnd.4thoffice.menu.item-v5.17+json' if accept_type is None else accept_type,
        }
        response = self.api_client.api_call('options', endpoint, url_parameters, add_headers, impersonate_user_id=impersonate_user_id)
        
        return fill(MenuItem_21, response.json(), content_type=response.headers['Content-Type'], silence_exceptions=self.api_client.silence_fill_exceptions)
    
    def get(self, streamId, badgeUnreadVersion=None, impersonate_user_id=None, accept_type=None):
        """
        Get menu item.
        
        :param streamId: 
        :type streamId: 
        
        :param badgeUnreadVersion: Version string that defines which logic to use for setting of unread badge count value on menu items and unread separator on feed. Available values are: 'V18', 'V19'.
        :type badgeUnreadVersion: Int32
        
        :param impersonate_user_id: 
        :type impersonate_user_id: str
        
        :param accept_type: 
        :type accept_type: str
        
        :return: 
        :rtype: MenuItem_21
        """
        url_parameters = {
            'badgeUnreadVersion': badgeUnreadVersion,
        }
        endpoint_parameters = {
            'streamId': streamId,
        }
        endpoint = 'navigation/{streamId}'.format(**endpoint_parameters)
        add_headers = {
            'Content-Type': 'application/vnd.4thoffice.menu.item-v5.17+json',
            'Accept': 'application/vnd.4thoffice.menu.item-v5.17+json' if accept_type is None else accept_type,
        }
        response = self.api_client.api_call('get', endpoint, url_parameters, add_headers, impersonate_user_id=impersonate_user_id)
        
        return fill(MenuItem_21, response.json(), content_type=response.headers['Content-Type'], silence_exceptions=self.api_client.silence_fill_exceptions)
