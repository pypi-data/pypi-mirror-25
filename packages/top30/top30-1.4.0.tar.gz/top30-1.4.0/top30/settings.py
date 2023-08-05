###########################################################################
# Top30 is Copyright (C) 2016-2017 Kyle Robbertze <krobbertze@gmail.com>
#
# Top30 is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License version 3 as
# published by the Free Software Foundation.
#
# Top30 is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Top30.  If not, see <http://www.gnu.org/licenses/>.
###########################################################################
"""
Manages the settings that are used while running
"""
import configparser
import os

import top30

class Settings:
    """
    Holds the settings for the top30 module
    """
    def __init__(self):
        self.config = configparser.ConfigParser()
        config_file = top30.find_file("top30.conf")
        self.config.read(config_file)

    def song_length(self):
        """ Returns the length of the song section length """
        return int(self.config['Song']['Length'])

    def song_start_tag(self):
        """ Retuns the tag that indicates the start of the song section """
        return self.config['Song']['StartTag']

    def song_directory(self):
        """ Returns the directory of the songs """
        song_directory = self.config['Song']['Directory']
        if song_directory.startswith("~"):
            return os.path.expanduser(song_directory)
        return song_directory

    def voice_start_overlap(self):
        """ Returns the voice start overlap time """
        return int(self.config['Voice']['StartOverlap'])

    def voice_end_overlap(self):
        """ Returns the voice end overlap time """
        return int(self.config['Voice']['EndOverlap'])

    def voice_directory(self):
        """ Returns the directory of the voice """
        voice_directory = self.config['Voice']['Directory']
        if voice_directory.startswith("~"):
            return os.path.expanduser(voice_directory)
        return voice_directory
