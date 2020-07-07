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
    