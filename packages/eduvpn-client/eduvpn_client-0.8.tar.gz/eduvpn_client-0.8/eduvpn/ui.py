# python-eduvpn-client - The GNU/Linux eduVPN client and Python API
#
# Copyright: 2017, The Commons Conservancy eduVPN Programme
# SPDX-License-Identifier: GPL-3.0+

import gi
import logging
import os
import webbrowser
import base64
from datetime import datetime

from eduvpn.util import error_helper, thread_helper

gi.require_version('Gtk', '3.0')
gi.require_version('GdkPixbuf', '2.0')
gi.require_version('Notify', '0.7')

from gi.repository import GObject, Gtk, GLib, GdkPixbuf

# this need to be one of the first to import
import dbus.mainloop.glib
dbus.mainloop.glib.DBusGMainLoop(set_as_default=True)
from dbus.exceptions import DBusException

from eduvpn.config import secure_internet_uri, institute_access_uri, verify_key
from eduvpn.crypto import make_verifier, gen_code_verifier
from eduvpn.oauth2 import get_open_port, create_oauth_session, get_oauth_token_code, oauth_from_token
from eduvpn.managers import connect_provider, list_providers, store_provider, delete_provider, disconnect_provider, \
    is_provider_connected, update_config_provider, update_keys_provider
from eduvpn.remote import get_instances, get_instance_info, get_auth_url, list_profiles, create_keypair, \
    get_profile_config, system_messages, user_messages
from eduvpn.notify import notify
from eduvpn.io import get_metadata
from eduvpn.util import bytes2pixbuf

import NetworkManager

logger = logging.getLogger(__name__)


class EduVpnApp:
    def __init__(self, here):
        self.here = here

        # hack to make the reopen url button work
        self.auth_url = None

        self.selected_uuid = None

        handlers = {
            "delete_window": Gtk.main_quit,
            "add_config": self.selection_connection_step,
            "del_config": self.delete,
            "select_config": self.select_config,
            "connect_set": self.connect_set,
        }

        NetworkManager.NetworkManager.connect_to_signal('PropertiesChanged', self.connection_state_change)

        self.builder = Gtk.Builder()
        self.builder.add_from_file(os.path.join(self.here, "../share/eduvpn/eduvpn.ui"))
        self.builder.connect_signals(handlers)

        self.window = self.builder.get_object('eduvpn-window')
        self.verifier = make_verifier(verify_key)

        self.window.set_position(Gtk.WindowPosition.CENTER)
        self.window.show_all()

        logo = os.path.join(self.here, '../share/eduvpn/eduvpn.png')
        self.icon_placeholder = GdkPixbuf.Pixbuf.new_from_file_at_scale(logo, 70, 30, True)

        self.update_providers()

    def connect(self, selection):
        logger.info("connect pressed")
        model, treeiter = selection.get_selected()
        if treeiter is not None:
            uuid, display_name = model[treeiter]
            notify("Connecting to {}".format(display_name))
            connect_provider(uuid)

    def disconnect(self, selection):
        logger.info("disconnect pressed")
        model, treeiter = selection.get_selected()
        if treeiter is not None:
            uuid, display_name = model[treeiter]
            notify("Disconnecting to {}".format(display_name))
            disconnect_provider(uuid)

    def update_providers(self):
        logger.info("composing list of current eduVPN configurations")
        config_list = self.builder.get_object('configs-model')
        introduction = self.builder.get_object('introduction')
        config_list.clear()
        providers = list(list_providers())

        if len(providers) > 0:
            logger.info("hiding introduction")
            introduction.hide()
            for meta in providers:
                uuid = meta['uuid']
                display_name = meta['display_name']
                icon_data = meta['icon_data']
                connection_type = display_name + "\n" + meta['connection_type']
                if icon_data:
                    icon = bytes2pixbuf(base64.b64decode(icon_data.encode()))
                else:
                    icon = self.icon_placeholder
                config_list.append((uuid, display_name, icon, connection_type))
        else:
            logger.info("showing introduction")
            introduction.show()

    def selection_connection_step(self, _):
        logger.info("add configuration clicked")
        dialog = self.builder.get_object('connection-type-dialog')
        dialog.show_all()
        response = dialog.run()
        dialog.hide()

        if response == 0:  # cancel
            logger.info("cancel button pressed")
            return
        elif response == 1:
            logger.info("secure button pressed")
            self.fetch_instance_step(discovery_uri=secure_internet_uri, connection_type='Secure Internet')
        elif response == 2:
            logger.info("institute button pressed")
            self.fetch_instance_step(discovery_uri=institute_access_uri, connection_type='Institute Access')

        elif response == 3:
            logger.info("custom button pressed")
            self.custom_url()

    def custom_url(self):
        dialog = self.builder.get_object('custom-url-dialog')
        entry = self.builder.get_object('custom-url-entry')
        dialog.show_all()
        while True:
            response = dialog.run()
            if response == 0:  # cancel
                logger.info("cancel button pressed")
                dialog.hide()
                return
            else:
                custom_url = entry.get_text()
                logger.info("ok pressed, entry text: {}".format(custom_url))
                if not custom_url.startswith('https://'):
                    GLib.idle_add(error_helper, dialog, "Invalid URL", "URL should start with https://")
                else:
                    GLib.idle_add(dialog.hide)
                    display_name = custom_url[8:].split('/')[0]
                    logger.info("using {} for display name".format(display_name))
                    GLib.idle_add(self.browser_step, display_name, custom_url, 'Custom Instance', 'local', None)
                    break

    def fetch_instance_step(self, discovery_uri, connection_type):
        logger.info("fetching instances step")
        dialog = self.builder.get_object('fetch-dialog')
        dialog.show_all()

        def background():
            try:
                authorization_type, instances = get_instances(discovery_uri=discovery_uri, verify_key=self.verifier)
            except Exception as e:
                GLib.idle_add(error_helper, dialog, "can't fetch instances", "{} {}".format(type(e), str(e)))
                GLib.idle_add(dialog.hide)
                raise
            else:
                GLib.idle_add(dialog.hide)
                GLib.idle_add(self.select_instance_step, connection_type, authorization_type, instances)

        thread_helper(background())

    def select_instance_step(self, connection_type, authorization_type, instances):
        logger.info("presenting instances to user")
        dialog = self.builder.get_object('instances-dialog')
        model = self.builder.get_object('instances-model')
        selection = self.builder.get_object('instances-selection')
        model.clear()
        dialog.show_all()

        for instance in instances:
            display_name, url, icon_data = instance
            try:
                icon = bytes2pixbuf(icon_data)
            except GLib.Error as e:
                print(icon_data)
                logger.error("can't process icon for {}: {}".format(display_name, str(e)))
                icon = None

            model.append((display_name, url, icon, base64.b64encode(icon_data).decode('ascii')))

        response = dialog.run()
        dialog.hide()

        if response == 0:  # cancel
            logging.info("cancel button pressed")
        else:
            model, treeiter = selection.get_selected()
            if treeiter:
                display_name, instance_base_uri, icon_pixbuf, icon_data = model[treeiter]
                self.browser_step(display_name=display_name, instance_base_uri=instance_base_uri,
                                  connection_type=connection_type,
                                  authorization_type=authorization_type, icon_data=icon_data)
            else:
                logger.info("nothing selected")

    def browser_step(self, display_name, instance_base_uri, connection_type, authorization_type, icon_data):
        logger.info("opening token dialog")
        dialog = self.builder.get_object('token-dialog')
        url_dialog = self.builder.get_object('redirecturl-dialog')
        dialog.show_all()

        def update(token, api_base_uri, oauth):
            logger.info("hiding url dialog")
            GLib.idle_add(url_dialog.hide)
            logger.info("hiding token dialog")
            GLib.idle_add(dialog.hide)
            self.fetch_profile_step(token, api_base_uri, oauth, display_name, connection_type, authorization_type,
                                    icon_data)

        def background():
            try:
                logger.info("starting token obtaining in background")
                api_base_uri, authorization_endpoint, token_endpoint = get_instance_info(instance_base_uri,
                                                                                         self.verifier)
                code_verifier = gen_code_verifier()
                port = get_open_port()
                oauth = create_oauth_session(port)
                self.auth_url = get_auth_url(oauth, code_verifier, authorization_endpoint)
                logger.info("opening browser with url {}".format(self.auth_url))
                webbrowser.open(self.auth_url)
                code = get_oauth_token_code(port)
                token = oauth.fetch_token(token_endpoint, code=code, code_verifier=code_verifier)
            except Exception as e:
                GLib.idle_add(error_helper, dialog, "can't obtain token", "{} {}".format(type(e).__name__, str(e)))
                GLib.idle_add(dialog.hide)
                raise
            else:
                GLib.idle_add(update, token, api_base_uri, oauth)


        thread_helper(background)

        while True:
            response = dialog.run()
            if response == 0:  # cancel
                logger.info("token dialog: cancel button pressed")
                dialog.hide()
                break
            elif response == 1:
                logger.info("token dialog: reopen browser button pressed, opening {} again".format(self.auth_url))
                webbrowser.open(self.auth_url)
            elif response == 2:
                logger.info("token dialog: show redirect URL button pressed")
                url_field = self.builder.get_object('redirect-url-entry')
                url_field.set_text(self.auth_url)
                url_dialog.run()
                logger.info("token dialog: url popup closed")
                url_dialog.hide()
            else:
                logger.info("token dialog: window closed")
                dialog.hide()
                break

    def fetch_profile_step(self, token, api_base_uri, oauth, display_name, connection_type, authorization_type,
                           icon_data):
        logger.info("fetching profile step")
        dialog = self.builder.get_object('fetch-dialog')
        dialog.show_all()

        def background():
            try:
                profiles = list_profiles(oauth, api_base_uri)
                if len(profiles) > 1:
                    GLib.idle_add(dialog.hide)
                    GLib.idle_add(self.select_profile_step, token, profiles, api_base_uri, oauth, display_name,
                                  connection_type, authorization_type, icon_data)
                elif len(profiles) == 1:
                    profile_display_name, profile_id, two_factor = profiles[0]
                    self.finalizing_step(oauth, api_base_uri, profile_id, display_name, token, connection_type,
                                         authorization_type, profile_display_name, two_factor, icon_data)
                else:
                    raise Exception("Either there are no VPN profiles defined, or this account does not have the "
                                    "required permissions to create a new VPN configurations for any of the "
                                    "available profiles.")

            except Exception as e:
                GLib.idle_add(error_helper, dialog, "can't fetch profile", "{}: {}".format(type(e).__name__, str(e)))
                GLib.idle_add(dialog.hide)
                raise

        thread_helper(background)

    def select_profile_step(self, profiles, token, api_base_uri, oauth, display_name, connection_type,
                            authorization_type, icon_data):
        logger.info("opening profile dialog")

        dialog = self.builder.get_object('profiles-dialog')
        model = self.builder.get_object('profiles-model')
        selection = self.builder.get_object('profiles-selection')
        dialog.show_all()

        model.append(profiles)

        response = dialog.run()
        dialog.hide()

        if response == 0:  # cancel
            logging.info("cancel button pressed")
            return
        else:
            model, treeiter = selection.get_selected()
            if treeiter:
                profile_display_name, profile_id, two_factor = model[treeiter]
                self.finalizing_step(oauth, api_base_uri, profile_id, display_name, token, connection_type,
                                     authorization_type, profile_display_name, two_factor, icon_data)
            else:
                logger.error("nothing selected")
                return

    def finalizing_step(self, oauth, api_base_uri, profile_id, display_name, token, connection_type, authorization_type,
                        profile_display_name, two_factor, icon_data):
        logger.info("finalizing step")
        dialog = self.builder.get_object('fetch-dialog')
        dialog.show_all()

        def background():
            try:
                cert, key = create_keypair(oauth, api_base_uri)
                config = get_profile_config(oauth, api_base_uri, profile_id)
            except Exception as e:
                GLib.idle_add(error_helper, dialog, "can't finalize configuration", "{}: {}".format(type(e).__name__,
                                                                                                   str(e)))
                GLib.idle_add(dialog.hide)
                raise
            else:
                try:
                    store_provider(api_base_uri, profile_id, display_name, token, connection_type, authorization_type,
                                   profile_display_name, two_factor, cert, key, config, icon_data)
                    notify("Added eduVPN configuration {}".format(display_name))
                except Exception as e:
                    GLib.idle_add(error_helper, dialog, "can't store configuration", "{} {}".format(type(e).__name__,
                                                                                                    str(e)))
                    GLib.idle_add(dialog.hide)
                    raise
                else:
                    GLib.idle_add(dialog.hide)
                    GLib.idle_add(self.update_providers)

        thread_helper(background)

    def delete(self, selection):
        logger.info("delete provider clicked")
        model, treeiter = selection.get_selected()
        if not treeiter:
            logger.info("nothing selected")
            return

        uuid, display_name, _, _ = model[treeiter]

        dialog = Gtk.MessageDialog(self.window, Gtk.DialogFlags.MODAL, Gtk.MessageType.QUESTION,
                                   Gtk.ButtonsType.YES_NO, "Are you sure you want to remove '{}'?".format(display_name))
        dialog.format_secondary_text("This action can't be undone.")
        response = dialog.run()
        if response == Gtk.ResponseType.YES:
            logger.info("deleting provider config")
            try:
                delete_provider(uuid)
                notify("Deleted eduVPN configuration {}".format(display_name))
            except Exception as e:
                GLib.idle_add(error_helper, self.window, "can't delete profile", "{}: {}".format(type(e).__name__, str(e)))
            GLib.idle_add(self.update_providers)
        elif response == Gtk.ResponseType.NO:
            logger.info("not deleting provider config")
        dialog.destroy()
        
    def fetch_messages(self, api_base_uri, token):
        logger.info("fetching user and system messages from {}".format(api_base_uri))

        def background(buffer, token):
            oauth = oauth_from_token(token)
            text = ""
            for message in user_messages(oauth, api_base_uri):
                logger.info(message)
                date_time = message['date_time']
                content = message['message']
                type = message['notification']
                text += date_time + "\n"
                text += content + "\n\n"
            for message in system_messages(oauth, api_base_uri):
                logger.info(message)
                date_time = message['date_time']
                content = message['message']
                type = message['type']
                text += date_time + "\n"
                text += content + "\n\n"
            GLib.idle_add(buffer.set_text, text)

        buffer = self.builder.get_object('messages-buffer')
        thread_helper(lambda: background(buffer, token))

    def select_config(self, list):
        notebook = self.builder.get_object('outer-notebook')
        switch = self.builder.get_object('connect-switch')
        ipv4_label = self.builder.get_object('ipv4-label')
        ipv6_label = self.builder.get_object('ipv6-label')
        name_label = self.builder.get_object('name-label')
        profile_label = self.builder.get_object('profile-label')
        profile_image = self.builder.get_object('profile-image')
        model, treeiter = list.get_selected()
        if not treeiter:
            logger.info("no configuration selected, showing main logo")
            notebook.set_current_page(0)
            return
        else:
            uuid, display_name, icon, _ = model[treeiter]
            self.selected_uuid = uuid
            logger.info("{} ({}) configuration was selected".format(display_name, uuid))
            self.selected_metadata = get_metadata(uuid)
            name_label.set_text(display_name)
            if self.selected_metadata['icon_data']:
                icon = bytes2pixbuf(base64.b64decode(self.selected_metadata['icon_data'].encode()),
                                    width=140, height=60)
            else:
                icon = self.icon_placeholder
            profile_image.set_from_pixbuf(icon)
            profile_label.set_text(self.selected_metadata['connection_type'])
            connected = is_provider_connected(uuid=uuid)
            switch.set_state(bool(connected))
            if connected:
                ipv4, ipv6 = connected
                ipv4_label.set_text(ipv4)
                ipv6_label.set_text(ipv6)
            else:
                ipv4_label.set_text("")
                ipv6_label.set_text("")
            notebook.show_all()
            notebook.set_current_page(1)
            if 'api_base_uri' in self.selected_metadata and 'token' in self.selected_metadata:
                self.fetch_messages(self.selected_metadata['api_base_uri'],
                                    self.selected_metadata['token'])
            else:
                logger.info("metadata doesnt contain api_base_uri and/or token data")

    def connection_state_change(self, *args, **kwargs):
        """Called when a networkmanager status change is emitted"""

        # this is VERY messy, but it is close to impossible to support the various networkmanager signals floating
        #around.

        def we_have_active_connections(active_conns):
            switch = self.builder.get_object('connect-switch')
            ipv4_label = self.builder.get_object('ipv4-label')
            ipv6_label = self.builder.get_object('ipv6-label')
            active = False
            for conn in active_conns:
                try:
                    if conn.Vpn and conn.Uuid == self.selected_uuid:
                        active = True
                        ipv4_label.set_text(conn.Ip4Config.AddressData[0]['address'])
                        ipv6_label.set_text(conn.Ip6Config.AddressData[0]['address'])
                except (DBusException, AttributeError) as e:
                    pass
            if not active:
                logger.info("selected VPN {} is NOT active!".format(self.selected_uuid))
                ipv4_label.set_text("")
                ipv6_label.set_text("")

        if type(args[0]) == dict:
            # Old API
            if 'ActiveConnections' in args[0]:
                logger.info("old type signal from network manager")
                we_have_active_connections(args[0]['ActiveConnections'])
            else:
                logger.info("ignoring useless signal event")
        elif args[0] != u'org.freedesktop.NetworkManager':
            # new api
            logger.info("new type signal from network manager")
            we_have_active_connections(args[0].ActiveConnections)

    def activate_connection(self, uuid, display_name):
        """do the actual connecting action"""
        notify("Connecting to {}".format(display_name))
        try:
            if ('profile_id' in self.selected_metadata and
                        'api_base_uri' in self.selected_metadata and
                        'token' in self.selected_metadata):
                profile_id = self.selected_metadata['profile_id']
                api_base_uri = self.selected_metadata['api_base_uri']
                oauth = oauth_from_token(self.selected_metadata['token'])
                config = get_profile_config(oauth, api_base_uri, profile_id)
                update_config_provider(uuid=uuid, display_name=display_name, config=config)

                if datetime.now() > datetime.fromtimestamp(self.selected_metadata['token']['expires_at']):
                    logger.info("key pair is expired")
                    cert, key = create_keypair(oauth, api_base_uri)
                    update_keys_provider(uuid, cert, key)

            else:
                logger.error("metadata missing for uuid {}, can't update config".format(uuid))
            connect_provider(uuid)
        except Exception as e:
            error_helper(self.window, "can't enable connection", "{}: {}".format(type(e).__name__, str(e)))
            raise

    def connect_set(self, selection, _):
        switch = self.builder.get_object('connect-switch')
        state = switch.get_active()
        logger.info("switch activated, state {}".format(state))
        model, treeiter = selection.get_selected()
        if treeiter is not None:
            uuid, display_name, _, _ = model[treeiter]
            if not state:
                self.activate_connection(uuid, display_name)
            else:
                notify("Disconnecting from {}".format(display_name))
                try:
                    disconnect_provider(uuid)
                except Exception as e:
                    error_helper(self.window, "can't disconnect", "{}: {}".format(type(e).__name__, str(e)))


def main(here):
    GObject.threads_init()
    logging.basicConfig(level=logging.INFO)
    eduVpnApp = EduVpnApp(here)
    Gtk.main()

