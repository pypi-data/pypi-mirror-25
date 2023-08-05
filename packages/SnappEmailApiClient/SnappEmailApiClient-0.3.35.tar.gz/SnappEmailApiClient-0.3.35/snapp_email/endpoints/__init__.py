from . import user_campaign
from . import invite
from . import event
from . import appointment
from . import errorlog
from . import group
from . import user_settings
from . import badge
from . import document
from . import api_index
from . import localization
from . import stream
from . import notification
from . import location
from . import drive
from . import post
from . import reminder
from . import board_avatar
from . import group_notification
from . import signature_image
from . import user
from . import action
from . import navigation
from . import search
from . import token
from . import signature
from . import user_session_logon
from . import group_avatar
from . import discussion
from . import document_thumbnail
from . import board
from . import feed
from . import user_device
from . import user_avatar


class ApiEndpoints:

    @property
    def user_campaign(self):
        """
        :return: user_campaign.UserCampaignEndpoint
        """
        return user_campaign.UserCampaignEndpoint(self)
    
    @property
    def invite(self):
        """
        :return: invite.InviteEndpoint
        """
        return invite.InviteEndpoint(self)
    
    @property
    def event(self):
        """
        :return: event.EventEndpoint
        """
        return event.EventEndpoint(self)
    
    @property
    def appointment(self):
        """
        :return: appointment.AppointmentEndpoint
        """
        return appointment.AppointmentEndpoint(self)
    
    @property
    def errorlog(self):
        """
        :return: errorlog.ErrorlogEndpoint
        """
        return errorlog.ErrorlogEndpoint(self)
    
    @property
    def group(self):
        """
        :return: group.GroupEndpoint
        """
        return group.GroupEndpoint(self)
    
    @property
    def user_settings(self):
        """
        :return: user_settings.UserSettingsEndpoint
        """
        return user_settings.UserSettingsEndpoint(self)
    
    @property
    def badge(self):
        """
        :return: badge.BadgeEndpoint
        """
        return badge.BadgeEndpoint(self)
    
    @property
    def document(self):
        """
        :return: document.DocumentEndpoint
        """
        return document.DocumentEndpoint(self)
    
    @property
    def api_index(self):
        """
        :return: api_index.ApiIndexEndpoint
        """
        return api_index.ApiIndexEndpoint(self)
    
    @property
    def localization(self):
        """
        :return: localization.LocalizationEndpoint
        """
        return localization.LocalizationEndpoint(self)
    
    @property
    def stream(self):
        """
        :return: stream.StreamEndpoint
        """
        return stream.StreamEndpoint(self)
    
    @property
    def notification(self):
        """
        :return: notification.NotificationEndpoint
        """
        return notification.NotificationEndpoint(self)
    
    @property
    def location(self):
        """
        :return: location.LocationEndpoint
        """
        return location.LocationEndpoint(self)
    
    @property
    def drive(self):
        """
        :return: drive.DriveEndpoint
        """
        return drive.DriveEndpoint(self)
    
    @property
    def post(self):
        """
        :return: post.PostEndpoint
        """
        return post.PostEndpoint(self)
    
    @property
    def reminder(self):
        """
        :return: reminder.ReminderEndpoint
        """
        return reminder.ReminderEndpoint(self)
    
    @property
    def board_avatar(self):
        """
        :return: board_avatar.BoardAvatarEndpoint
        """
        return board_avatar.BoardAvatarEndpoint(self)
    
    @property
    def group_notification(self):
        """
        :return: group_notification.GroupNotificationEndpoint
        """
        return group_notification.GroupNotificationEndpoint(self)
    
    @property
    def signature_image(self):
        """
        :return: signature_image.SignatureImageEndpoint
        """
        return signature_image.SignatureImageEndpoint(self)
    
    @property
    def user(self):
        """
        :return: user.UserEndpoint
        """
        return user.UserEndpoint(self)
    
    @property
    def action(self):
        """
        :return: action.ActionEndpoint
        """
        return action.ActionEndpoint(self)
    
    @property
    def navigation(self):
        """
        :return: navigation.NavigationEndpoint
        """
        return navigation.NavigationEndpoint(self)
    
    @property
    def search(self):
        """
        :return: search.SearchEndpoint
        """
        return search.SearchEndpoint(self)
    
    @property
    def token(self):
        """
        :return: token.TokenEndpoint
        """
        return token.TokenEndpoint(self)
    
    @property
    def signature(self):
        """
        :return: signature.SignatureEndpoint
        """
        return signature.SignatureEndpoint(self)
    
    @property
    def user_session_logon(self):
        """
        :return: user_session_logon.UserSessionLogonEndpoint
        """
        return user_session_logon.UserSessionLogonEndpoint(self)
    
    @property
    def group_avatar(self):
        """
        :return: group_avatar.GroupAvatarEndpoint
        """
        return group_avatar.GroupAvatarEndpoint(self)
    
    @property
    def discussion(self):
        """
        :return: discussion.DiscussionEndpoint
        """
        return discussion.DiscussionEndpoint(self)
    
    @property
    def document_thumbnail(self):
        """
        :return: document_thumbnail.DocumentThumbnailEndpoint
        """
        return document_thumbnail.DocumentThumbnailEndpoint(self)
    
    @property
    def board(self):
        """
        :return: board.BoardEndpoint
        """
        return board.BoardEndpoint(self)
    
    @property
    def feed(self):
        """
        :return: feed.FeedEndpoint
        """
        return feed.FeedEndpoint(self)
    
    @property
    def user_device(self):
        """
        :return: user_device.UserDeviceEndpoint
        """
        return user_device.UserDeviceEndpoint(self)
    
    @property
    def user_avatar(self):
        """
        :return: user_avatar.UserAvatarEndpoint
        """
        return user_avatar.UserAvatarEndpoint(self)
    