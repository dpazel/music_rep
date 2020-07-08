# music_rep
Companion software to "Music Representation: A Software Approach" by Donald Pazel


Dependencies:
  - Python: 3.x
  - Mido: https://mido.readthedocs.io/en/latest/installing.html
  - Mock: https://pypi.python.org/pypi/mock
  - Antlr4: http://www.antlr.org/download.html
         (pip3 install antlr4-python3-runtime)
  - PyQt5 (https://pypi.org/project/PyQt5/)
  - PyAudio (https://people.csail.mit.edu/hubert/pyaudio/)
  - Be sure to use pip3 for 3.x Python installations if dependencies
  
If you plan to change resource/LineGrammar.g4, ensure you install antlr4 support, and direct the generated files 
to structure/LineGrammar.  Pycharm users should install antlr plugin.

Make sure to generate the altlr4 parser files.
    
 ### VST Interface
 We support link to vst2/3 host as found in 
    github.com/dpazel/vst23host.
 The Python support file is found in vstinterface/vst_interface. As currently implemented,
 libvst23host must be in installed at vstinterface/lib.
 Examples of how to use this interface are found in test/vstinterface_tests.