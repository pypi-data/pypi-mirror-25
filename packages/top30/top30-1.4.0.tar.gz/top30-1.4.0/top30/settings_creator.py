from PyQt5.QtCore import QSettings, QPoint

settings = QSettings("UCTRadio", "Top30")

settings.beginGroup("songs")
settings.setValue("length", 10000)
settings.setValue("start_tag", "description")
settings.setValue("directory", "~/uct-radio/rundowns/songs")
settings.endGroup()
settings.beginGroup("voice")
settings.setValue("voice_start_overlap", 300)
settings.setValue("voice_end_overlap", 1400)
settings.setValue("voice_directory", "~/uct-radio/rundowns/voice")
settings.endGroup()

del settings
