grammar LineGrammar;
/*
  LineGrammer is a lightweight grammer for specifying a combination of melody line and harmonic context track.
  It uses the python module line_constructor.py as an assist to build these items, and the module
  line_grammar_executor as a exposed api to using this grammer to parse strings into lines and harmonic_context_tracks.

  The grammar is relative easy:
    { ... } is how you start
    { ... [ ... [...] ... ] ...} as a way to do nested beams
    { ... (dur, #)[ ... ] ...] } as a way to do tuplets with dur being a unit duration, and # the number of them
                                 dur * # is the full (locked) duration of the tuplet no matter how many notes
    Notes: (duration) (letter) (alteration) : (register), e.g. hEb:5 is half note Eb in register 5
           for convenience:
               1) register may be specified once and assumed in further notes for that level, e.g. line, beam, tuplet.
               2) same for duration, e.g. i is eight note, and further notes on same level are eights.

    Example: '{ C:5 D Eb F (1:8, 2)[C:3 D:4 E] [i@C#:3 sBb D:4 Fbb]}'

    Harmonic Contexts:
    These are:
       < ... >
       < tonality : chord> where tonality is like Db-Major and chord is either say Eb-Min or ii.
       < : chord> means tonality is picked up from where last specified.

    Harmonic contexts are dropped whereever they start to take effect - duration and position are automatically
    calculated.

    Example: '{ <E-Major:iv> C:5 D Eb F (1:8, 2)[C:3 D:4 E] <:v> [i@C#:3 sBb D:4 Fbb]}'

    Secondary chords:
      General notation for the chord:
          <NUMERAL>(ChordType)?/(NUMERAL)('-' MODALITY)

      e.g. <F-Minor: IIIDom7/V-Melodic>, <C-Major, V/V>

    NOTE: Ties are in the syntax but not supported at this time.

    In naming a modality - one can user the shorthands Natural, Melodic, Harmonic for minor keys, and 'minor' for
    MelodicMinor.
    User named keys must have a '!' prefix, e.g. !MyModality
*/

@header {
from structure.LineGrammar.core.line_constructor import LineConstructor
import sys
}

@members {
    self.lc = LineConstructor();
    self._notelist = list()
}

/* This is the entry rule of our parser. */
motif: LINEBEGIN ( motificElement )+ LINEEND;

motificElement:  ( (primitiveNote  {self.lc.add_note($primitiveNote.n)} | harmonicTag)
                  | beam
                  | tuplet)
                  ;

primitiveNote returns [n]
              locals [dots=0, dur=None, ties=False]:
              (duration {$dur = $duration.d} ( DOT {$dots = $dots + 1} )*)?
              pitch
              ( TIE {$ties = True})? {$n = self.lc.construct_note($pitch.p, $dur, $dots, $ties)}
              ;

beam: '[' {self.lc.start_level()}
              ( motificElement )+
              ']' {self.lc.end_level()}
              ;

tuplet:
       '(' duration ',' dur_int=INT ')'
       '[' {self.lc.start_level($duration.d, dur_int=$dur_int.int)}
        ( motificElement )+
        ']' {self.lc.end_level()}
        ;

pitch returns [p]
    locals [tt=None, alert=None, reg=None]:
    tone {$tt = $tone.t}
    (':' INT {$reg = $INT.int})? {$p=self.lc.construct_pitch($tt, $reg)};

tone returns [t=None]:
    (ltrs=NOTELETTERS {$t=LineConstructor.construct_tone_from_tone_letters($ltrs.text)});

duration returns[d]:
     ( DURATIONLETTER {$d = LineConstructor.construct_duration_by_shorthand($DURATIONLETTER.text) }
     | COMMON_DURATION_CHORD_NUMERAL_LETTERS {$d = LineConstructor.construct_duration_by_shorthand($COMMON_DURATION_CHORD_NUMERAL_LETTERS.text) }
     | '(' durationFraction ')' {$d = LineConstructor.construct_duration($durationFraction.f[0], $durationFraction.f[1])});

durationFraction returns [f]:
    numerator=INT ':'  denominator=INT {$f = ($numerator.int, $denominator.int)};

tonality returns [tonal]
    locals [modal_index=0]:
    tone '-' MODALITY ('(' INT {$modal_index = $INT.int}')')? {$tonal = self.lc.construct_tonality($tone.t, $MODALITY.text, $modal_index)};

chordTemplate returns [ctemplate]
    locals [cm=None, secondary_numeral=None, secondary_modality=None]:
    (tone '-' CHORDMODALITY {$ctemplate = self.lc.construct_chord_template($tone.t, None, $CHORDMODALITY.text)})
    | ((CHORDNUMERAL (CHORDMODALITY {$cm=$CHORDMODALITY.text})? {$ctemplate = self.lc.construct_chord_template(None, $CHORDNUMERAL.text, $cm)}
    | COMMON_DURATION_CHORD_NUMERAL_LETTERS (CHORDMODALITY {$cm=$CHORDMODALITY.text})? {$ctemplate = self.lc.construct_chord_template(None, $COMMON_DURATION_CHORD_NUMERAL_LETTERS.text, $cm)})
     ( '/' (CHORDNUMERAL {$secondary_numeral=$CHORDNUMERAL.text} | COMMON_DURATION_CHORD_NUMERAL_LETTERS {$secondary_numeral=$COMMON_DURATION_CHORD_NUMERAL_LETTERS.text})
     ('-' MODALITY {$secondary_modality=$MODALITY.text})? {$ctemplate = self.lc.construct_secondary_chord_template($ctemplate, $secondary_numeral, $secondary_modality)})?
    )
    ;

harmonicTag returns[ht]:
             '<'
             (( tonality ':' chordTemplate {$ht=self.lc.construct_harmonic_tag($tonality.tonal, $chordTemplate.ctemplate)})
                | ( ':' chordTemplate {$ht=self.lc.construct_harmonic_tag(None, $chordTemplate.ctemplate)}))
             '>'
             ;

DOT: '@';
TIE: '-';
INT : [0-9]+ ;
LINEBEGIN : '{';
LINEEND: '}';
WS : [ \t]+ -> skip ; // toss out whitespace
COMMON_DURATION_CHORD_NUMERAL_LETTERS: ('I' | 'i' );
DURATIONLETTER: ('W' | 'w' | 'H' | 'h' | 'Q' | 'q' | 'S' | 's' | 'T' | 't' | 'X' | 'x');
ALTERATION: ('bb' | '#' | '##');
fragment USER_MODALITY: '!'(('A'..'Z') | ('a'..'z'))+;
fragment SYSTEM_MODALITIES: ('Major' | 'Natural' | 'Melodic' | 'Harmonic' | 'Minor' |
                             'NaturalMinor'| 'MelodicMinor'| 'HarmonicMinor' | 'HarmonicMajor' |
                             'Ionian' | 'Dorian' | 'Phrygian' | 'Lydian' | 'Myxolydian' | 'Aeolian' | 'Locrian' |
                             'WholeTone' |
                             'MajorPentatonic' | 'EgyptianPentatonic' | 'MinorBluesPentatonic' | 'MajorBluesPentatonic' | 'MinorPentatonic' |
                             'HWOctatonic' | 'WHOctatonic' | 'MajorBlues' | 'MinorBlues');
MODALITY: (SYSTEM_MODALITIES | USER_MODALITY);

CHORDNUMERAL: ('II' | 'III' | 'IV' | 'V' | 'VI' | 'VII' | 'ii' | 'iii' | 'iv' | 'v' | 'vi' | 'vii');
CHORDMODALITY: ('Maj7' | 'Min7' | 'Dom7' | 'Maj' | 'Min' | 'Aug' | 'Dim' | 'HalfDim7') ;

NOTELETTERS: ('C' | 'D' | 'E' | 'F' | 'G' | 'A' | 'B' | 'c' | 'd' | 'e' | 'f' | 'g' | 'a' | 'b' |
              'Cb' | 'Db' | 'Eb' | 'Fb' | 'Gb' | 'Ab' | 'Bb' | 'cb' | 'db' | 'eb' | 'fb' | 'gb' | 'ab' | 'bb' |
              'Cbb' | 'Dbb' | 'Ebb' | 'Fbb' | 'Gbb' | 'Abb' | 'Bbb' | 'cbb' | 'dbb' | 'ebb' | 'fbb' | 'gbb' | 'abb' | 'bbb' |
              'C#' | 'D#' | 'E#' | 'F#' | 'G#' | 'A#' | 'B#' | 'c#' | 'd#' | 'e#' | 'f#' | 'g#' | 'a#' | 'b#' |
              'C##' | 'D##' | 'E##' | 'F##' | 'G##' | 'A##' | 'B##' | 'c##' | 'd##' | 'e##' | 'f##' | 'g##' | 'a##' | 'b##' | 'R' | 'r'

);


