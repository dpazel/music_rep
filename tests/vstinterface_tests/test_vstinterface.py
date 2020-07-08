import sys

from timemodel.tempo_function_event import TempoFunctionEvent
from vstinterface.vst_interface import vst_interface_launch, VstAppUserInterface

from harmoniccontext.harmonic_context import HarmonicContext
from harmoniccontext.harmonic_context_track import HarmonicContextTrack
from harmonicmodel.tertian_chord_template import TertianChordTemplate
from instruments.instrument_catalog import InstrumentCatalog
from structure.score import Score
from structure.instrument_voice import InstrumentVoice
from structure.line import Line
from structure.note import Note
from timemodel.duration import Duration
from timemodel.event_sequence import EventSequence
from timemodel.tempo_event_sequence import TempoEventSequence
from tonalmodel.diatonic_pitch import DiatonicPitch
from timemodel.position import Position

from timemodel.time_signature_event import TimeSignatureEvent
from structure.time_signature import TimeSignature
from timemodel.tempo_event import TempoEvent
from structure.tempo import Tempo

from tonalmodel.diatonic_tone import DiatonicTone
from tonalmodel.modality import ModalityType
from tonalmodel.tonality import Tonality

from midi.score_to_vst_midi_converter import ScoreToVstMidiConverter

from timemodel.time_conversion import TimeConversion

VST3_LIB = '/Library/Application Support/Steinberg/Components/HALion Sonic SE.vst3'
VST3_SAVE_PRESET_FILENAME = '/Users/xxxx/Temp/VST3_PRESET.PRESET'
VST3_LOAD_PRESET_FILENAME = '/Users/xxxx/Temp/VST3_PRESET.PRESET'

def build_vst_midi_list():
    """

    :return: 
    """
    c = InstrumentCatalog.instance()
    violin = c.get_instrument("violin")

    # Add notes to the score
    vnote0 = Note(DiatonicPitch(4, 'a'), Duration(1, 8))
    vnote1 = Note(DiatonicPitch(4, 'b'), Duration(1, 8))
    vnote2 = Note(DiatonicPitch(4, 'c'), Duration(1, 8))
    vnote3 = Note(DiatonicPitch(4, 'd'), Duration(1, 8))
    vnote4 = Note(DiatonicPitch(4, 'e'), Duration(1, 8))
    vnote5 = Note(DiatonicPitch(4, 'f'), Duration(1, 8))

    # Set up a violin voice with 6 8th notes
    vline = Line([vnote0, vnote1, vnote2, vnote3, vnote4, vnote5])

    tempo_seq = TempoEventSequence()
    ts_seq = EventSequence()
    tempo_seq.add(TempoEvent(Tempo(60), Position(0)))
    ts_seq.add(TimeSignatureEvent(TimeSignature(3, Duration(1, 4), 'sww'), Position(0)))

    hc_track = HarmonicContextTrack()
    diatonic_tonality = Tonality.create(ModalityType.Major, DiatonicTone("C"))
    chord_t = TertianChordTemplate.parse('tIV')
    chord = chord_t.create_chord(diatonic_tonality)
    hc_track.append(HarmonicContext(diatonic_tonality, chord, Duration(2)))

    score = Score()

    score.tempo_sequence.add(TempoEvent(Tempo(60), Position(0)))
    score.time_signature_sequence.add(TimeSignatureEvent(TimeSignature(3, Duration(1, 4)), Position(0)))

    violin = c.get_instrument("violin")
    violin_instrument_voice = InstrumentVoice(violin, 1)
    score.add_instrument_voice(violin_instrument_voice)
    violin_instrument_voice.voice(0).pin(vline)

    return ScoreToVstMidiConverter.convert_score(score, {0: 0}), score


class ATestInterface(VstAppUserInterface):
    def __init__(self):
        (self.meta_track, self.tracks), self.score = build_vst_midi_list()
        self.left_buffer = None
        self.right_buffer = None

    def get_library_name(self):
        return VST3_LIB

    def get_save_preset_filename(self):
        return VST3_SAVE_PRESET_FILENAME

    def get_load_preset_filename(self):
        return VST3_LOAD_PRESET_FILENAME

    def get_vst_midi_event_list(self):
        return self.tracks[0]

    def get_time_in_ms(self):
        event_list = self.score.tempo_sequence.sequence_list
        score_len = self.score.length()

        fine_tempo_sequence = TempoEventSequence()

        for event in event_list:
            if isinstance(event, TempoEvent):
                fine_tempo_sequence.add(TempoEvent(event.object, event.time))
            elif isinstance(event, TempoFunctionEvent):
                t1 = event.time
                beat_duration = event.beat_duration if event.beat_duration is None else \
                    ScoreToVstMidiConverter.DEFAULT_BEAT_DURATION
                next_event = self.score.tempo_sequence.successor(event)
                t2 = next_event.time if next_event is not None else Position(score_len.duration)
                while t1 < t2:
                    tempo = int(event.tempo(t1, next_event.time if next_event is not None else Position(score_len)))
                    delta_wnt = (tempo * ScoreToVstMidiConverter.TEMPO_EVENT_DURATION_MS * beat_duration.duration) / \
                                (60.0 * 1000.0)

                    fine_tempo_sequence.add(TempoEvent(Tempo(tempo, beat_duration), t1))

                    t1 += delta_wnt

        conversion = TimeConversion(fine_tempo_sequence, self.score.time_signature_sequence, Position(score_len))
        actual_time = conversion.position_to_actual_time(Position(self.score.duration))
        return actual_time

    def save_generated_buffers(self, left_buffer, right_buffer):
        self.left_buffer = left_buffer
        self.right_buffer = right_buffer

    def get_audio_buffers(self):
        return self.left_buffer, self.right_buffer


vst_interface_launch(ATestInterface(), sys.argv)
