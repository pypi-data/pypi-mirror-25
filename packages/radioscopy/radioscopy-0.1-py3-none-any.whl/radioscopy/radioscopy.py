#!/usr/bin/env python3
from collections import OrderedDict
import configparser
import os
import signal

import gi
gi.require_version('Gtk', '3.0')
gi.require_version('Gst', '1.0')
from gi.repository import Gtk, Gst


CONFIG_FILE = '~/.config/radioscopy/config.ini'


def get_radios(cfg_file):
    parser = configparser.ConfigParser()
    parser.optionxform = str  # Do not change the case of radio names
    parser.read(cfg_file)
    radios = OrderedDict()
    for section in parser.sections():
        name = section[len('Radio:'):]
        url = parser[section]['url']
        radios[name] = url

    return radios


class TrayIcon(Gtk.StatusIcon):
    def __init__(self):
        Gtk.StatusIcon.__init__(self)
        self.set_from_icon_name('gtk-no')
        self.connect("activate", self.on_click)

        # Radios
        config_path = os.path.expanduser(CONFIG_FILE)
        self.radios = get_radios(config_path)

        # Player
        Gst.init(None)
        self.player = Gst.ElementFactory.make("playbin", "player")

        # Build menu
        self.menu = Gtk.Menu()

        # Add all radios from the config file
        group = None
        for radio_name, _ in self.radios.items():
            item = Gtk.RadioMenuItem(group=group, label=radio_name)
            group = item.get_group()[0]
            item.connect('activate', self.on_play_radio)
            self.menu.append(item)

        # Separator
        self.menu.append(Gtk.SeparatorMenuItem())

        # Stop button
        stop_item = Gtk.RadioMenuItem(group=group, label='Stop')
        stop_item.connect('activate', self.on_stop_radio)
        self.menu.append(stop_item)
        stop_item.set_active(True)

        # Separator
        self.menu.append(Gtk.SeparatorMenuItem())

        # Quit button
        quit_item = Gtk.MenuItem('Quit')
        quit_item.connect('activate', Gtk.main_quit)
        self.menu.append(quit_item)
        self.menu.show_all()

    def on_play_radio(self, data):
        if not data.get_active():
            return
        radio_name = data.get_label()
        self.player.set_state(Gst.State.NULL)
        self.player.set_property('uri', self.radios[radio_name])
        self.player.set_state(Gst.State.PLAYING)
        self.set_from_icon_name('gtk-yes')

    def on_stop_radio(self, data):
        if not data.get_active():
            return
        self.player.set_state(Gst.State.NULL)
        self.set_from_icon_name('gtk-no')

    def on_click(self, data):
        time = Gtk.get_current_event_time()
        self.menu.popup(None, None, Gtk.StatusIcon.position_menu, data, 1, time)


def main():
    # Make sure ^C kills the program
    signal.signal(signal.SIGINT, signal.SIG_DFL)

    # Let's go!
    TrayIcon()
    Gtk.main()


if __name__ == '__main__':
    main()
