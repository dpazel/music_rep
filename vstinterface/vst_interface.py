import sys

from abc import ABC, abstractmethod

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QWidget, QMainWindow, QAction
from PyQt5 import QtCore, QtGui
from PyQt5.QtGui import QColor, QPainter, QPen, QFontMetrics
import pyaudio
import struct

from midi.score_to_vst_midi_converter import MidiMessage, NoteMessage, MetaMessage, ExpressionVelocityMessage

from ctypes import CDLL, Structure, c_int, c_char_p, c_int32, py_object
import os

LIBRARY = 'lib/libvst23host'

class PyEvent(Structure):
    _fields_ = [('msg_type', c_int32),
                ('channel', c_int32),
                ('data1', c_int32),
                ('data2', c_int32),
                ('rel_frame_time', c_int32),
                ('abs_frame_time', c_int32)
               ]

CHUNK = 1024
SAMPLE_RATE = 44100  # samples per second


class VstAppUserInterface(ABC):
    @abstractmethod
    def get_library_name(self):
        pass

    @abstractmethod
    def get_vst_midi_event_list(self):
        pass

    @abstractmethod
    def get_time_in_ms(self):
        pass

    @abstractmethod
    def save_generated_buffers(self, left_buffer, right_buffer):
        pass

    @abstractmethod
    def get_audio_buffers(self):
        pass

    @abstractmethod
    def get_save_preset_filename(self):
        pass

    @abstractmethod
    def get_load_preset_filename(self):
        pass


class VstInterfaceApp(QMainWindow):
    def __init__(self, vst_app_user_interface, alt_lib_path):
        QMainWindow.__init__(self)
        self.vst_app_user_interface = vst_app_user_interface
        self.title = 'VST/QT5 player interface.'
        self.help_menu = None
        self.exit_act = None
        self.vst_library = None
        self.error = None
        self.vst_lib_path_name = None
        self.is_vst2 = False

        self.lib_path = alt_lib_path
        if self.lib_path is None:
            path = os.path.abspath(sys.modules[VstInterfaceApp.__module__].__file__)
            end_index = path.rindex('/')
            self.lib_path = path[0: end_index + 1] + LIBRARY

        try:
            self.vst_library = CDLL(os.path.abspath(self.lib_path), mode=1)
        except Exception as e:
            self.error = 'Could not load library={0}: {1}'.format(self.lib_path, e)
            print(self.error, file=sys.stderr, flush=True)
            return

        self.init_ui()

    def init_ui(self):
        self.create_actions()
        self.create_menus()

        self.setWindowTitle(self.title)
        self.setGeometry(50, 20, 640, 480)
        self.statusBar().showMessage('Message in Status Bar.')

        widget = DrawingWidget()
        self.setCentralWidget(widget)

    def error(self):
        return self.error

    def create_actions(self):
        self.load_library_act = QAction("Load &Library", self, shortcut='Ctrl+L', statusTip='Load Vst Library',
                                triggered=self.load_library)
        self.load_instruments_act = QAction("Load &Instruments", self, shortcut='Ctrl+I', statusTip='Load Instruments',
                                triggered=self.load_instruments)
        self.load_preset = QAction("L&oad Preset", self, shortcut="Ctrl+o", statusTip="Load Preset",
                                triggered=self.load_preset)
        self.save_preset = QAction("&Save Preset", self, shortcut="Ctrl+S", statusTip="Save Preset",
                                triggered=self.save_preset)
        self.generate_audio_act = QAction("&Generate Audio", self, shortcut='Ctrl+G', statusTip='Generate Audio',
                                            triggered=self.generate_audio)
        self.play_audio_act = QAction("&Play Audio", self, shortcut='Ctrl+P', statusTip='Play Audio',
                                            triggered=self.play)
        self.exit_act = QAction("E&xit", self, shortcut='Ctrl+Q', statusTip='Exit application',
                                triggered=self.close)

    def create_menus(self):
        self.menuBar().setNativeMenuBar(False)
        primary_actions = self. menuBar().addMenu('&Actions')
        primary_actions.addAction(self.load_library_act)
        primary_actions.addAction(self.load_instruments_act)
        primary_actions.addAction(self.load_preset)
        primary_actions.addAction(self.save_preset)
        primary_actions.addAction(self.generate_audio_act)
        primary_actions.addAction(self.play_audio_act)

        self.help_menu = self.menuBar().addMenu("&Help")
        primary_actions.addAction(self.exit_act)

    def load_library(self):
        self.vst_lib_path_name = self.vst_app_user_interface.get_library_name()
        print(self.vst_lib_path_name)
        if self.vst_lib_path_name[-1] == '3':
            self.vst_library.connect_vst3(self.vst_lib_path_name.encode('ascii'))
        else:
            self.vst_library.connect_vst2(self.vst_lib_path_name.encode('ascii'))
            self.is_vst2 = True

        # Important to set up to get return values properly from these called methods.
        self.vst_library.process_events.restype = py_object
        self.vst_library.process_events2.restype = py_object

    def load_instruments(self):
        if self.vst_library is None:
            self.statusBar().showMessage('Cannot load instrument before loading vst.')
            return

        if not self.is_vst2:
            self.vst_library.view_and_show()
        else:
            self.vst_library.view_and_show2()

    def load_preset(self):
        if not self.is_vst2:
            self.vst_library.load_preset(self.vst_app_user_interface.get_load_preset_filename().encode('ascii'))
        else:
            self.vst_library.load_bank(self.vst_app_user_interface.get_load_preset_filename().encode('ascii'))

    def save_preset(self):
        if not self.is_vst2:
            self.vst_library.save_preset(self.vst_app_user_interface.get_save_preset_filename().encode('ascii'))
        else:
            self.vst_library.save_bank(self.vst_app_user_interface.get_save_preset_filename().encode('ascii'))

    def feed_events(self, midi_message_list):
        midi_message_array = VstInterfaceApp.convert_midi_message_list_to_py_event(midi_message_list)
        if not self.is_vst2:
            self.vst_library.feed_events(midi_message_array, len(midi_message_list))
        else:
            self.vst_library.feed_events2(midi_message_array, len(midi_message_list))
        return

    def generate_audio(self, play_time_in_ms):
        if self.is_vst2:
            self.vst_library.begin_event_rendering2()

        midi_message_list = self.vst_app_user_interface.get_vst_midi_event_list()
        if midi_message_list is not None:
            self.feed_events(midi_message_list)

        if not self.is_vst2:
            (left_buffer, right_buffer) = self.vst_library.process_events(
                int(self.vst_app_user_interface.get_time_in_ms()))
        else:
            (left_buffer, right_buffer) = self.vst_library.process_events2(
                int(self.vst_app_user_interface.get_time_in_ms()))
            self.vst_library.end_event_rendering2()

        self.vst_app_user_interface.save_generated_buffers(left_buffer, right_buffer)

    def play(self):
        print('playing ...')
        (left_audio_buffer, right_audio_buffer) = self.vst_app_user_interface.get_audio_buffers()
        self.num_samples = len(left_audio_buffer)

        p = pyaudio.PyAudio()

        stream = p.open(format=pyaudio.paFloat32,
                        channels=2,
                        rate=SAMPLE_RATE,
                        output=True)

        sample_number = 0;
        data_a = bytearray(CHUNK * 2 * 4)
        while sample_number < len(left_audio_buffer):
            num_samples_to_get = min(CHUNK, self.num_samples - sample_number)
            for i in range(0, num_samples_to_get):
                ba1 = bytearray(struct.pack("f", left_audio_buffer[sample_number]))
                ba2 = bytearray(struct.pack("f", right_audio_buffer[sample_number]))
                pos = 2 * 4 * i
                data_a[pos: pos + len(ba1)] = ba1
                data_a[pos + len(ba1): pos + len(ba1) + len(ba2)] = ba2
                sample_number += 1

            d = bytes(data_a)
            stream.write(d)

        print('finished playing')

    def disconnect(self):
        if not self.is_vst2:
            self.vst_library.close_vst()
        else:
            self.vst_library.close_vst2()
        self.vst_library = None

    def close(self):
        self.disconnect()
        super().close()

    @staticmethod
    def convert_midi_message_list_to_py_event(message_list):
        event_array = (PyEvent * len(message_list))()
        for i in range(0, len(message_list)):
            message = message_list[i]
            event_array[i].msg_type = message.msg_type
            event_array[i].channel = message.channel
            event_array[i].rel_frame_time = message.rel_frame_time
            event_array[i].abs_frame_time = message.abs_frame_time
            event_array[i].data1 = 0
            event_array[i].data2 = 0
            if isinstance(message, NoteMessage):
                event_array[i].data1 = message.note_value
                event_array[i].data2 = message.velocity
            elif isinstance(message, MetaMessage):
                event_array[i].data1 = message.value
            elif isinstance(message, ExpressionVelocityMessage):
                event_array[i].data1 = message.velocity
        return event_array


class DrawingWidget(QWidget):

    def __init__(self, parent=None):
        QWidget.__init__(self, parent)
        self.pen = QtGui.QPen(QColor(200, 0, 0))
        self.pen.setWidth(3)
        self.brush = QtGui.QBrush(QColor(0, 255, 255, 255))

        self.setAutoFillBackground(True)

        p = self.palette()
        p.setColor(self.backgroundRole(), Qt.green)
        self.setPalette(p)

    def paintEvent(self, event):
        # painter = QPainter(self)
        pass

    def mouse_pressed(self, event):
        # p = QtGui.QCursor.pos()
        return

    def mouse_moved(self, event):
        return

    def mouse_released(self, event):
        return


def vst_interface_launch(vst_app_user_interface, args=None, alt_lib_path=None):
    app = QApplication(args)
    window = VstInterfaceApp(vst_app_user_interface, alt_lib_path)
    if window.error is not None:
        sys.exit(1)
    window.show()
    sys.exit(app.exec())
