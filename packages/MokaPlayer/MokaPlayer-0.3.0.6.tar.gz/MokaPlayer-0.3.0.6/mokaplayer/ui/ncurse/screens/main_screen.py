import logging
import curses

from gi.repository import GObject

from mokaplayer.core.helpers import time_helper


class MainScreen():
    def __init__(self, appconfig, userconfig, player):
        self.logger = logging.getLogger('MainWindow')
        self.appconfig = appconfig
        self.userconfig = userconfig
        self.player = player

        self.player.state_changed.subscribe(self.on_player_state_changed)
        self.player.audio_changed.subscribe(self.on_audio_changed)
        self.player.volume_changed.subscribe(self.on_volume_changed)

        self.__set_current_song_info()
        self.on_volume_changed()

        GObject.timeout_add(750, self.on_tick, None)

        self.stdscr = curses.initscr()
        curses.noecho()
        self.stdscr.keypad(True)

        self.logger.info('Screen loaded')

    def __set_current_song_info(self):
        self.logger.debug("Setting currrent song info")

    def show(self):
        pass

    def on_audio_changed(self):
        GObject.idle_add(self.__set_current_song_info)

    def on_player_state_changed(self):
        GObject.idle_add(self.__set_current_song_info)

    def on_volume_changed(self):
        pass

    def on_tick(self, data):
        position = self.player.streamer.position
        duration = self.player.streamer.duration
        fraction = position / duration if duration else 0
        position_text = time_helper.seconds_to_string(position)
        duration_text = time_helper.seconds_to_string(duration)

        # self.lbl_current_time.set_text(f'{position_text} / {duration_text}')
        # self.prb_current_time.set_fraction(fraction)

        return True