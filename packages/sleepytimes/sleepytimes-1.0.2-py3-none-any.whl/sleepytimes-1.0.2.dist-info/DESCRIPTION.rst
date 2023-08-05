Sleepytimes
===========
Package to analyze EEG, ECoG and other electrophysiology formats.
It allows for visualization of the results and for a GUI that can be used to score sleep stages.

Features
--------
- Reader and writer for EDF, EGI MFF, Fieldtrip, FIFF file formats
- Interface for Sleep Scoring
- Computes frequency analysis (spectrogram), time-frequency analysis (Morlet wavelet)
- Spindle detection and analysis
- Pure Python

Installation
------------
Install sleepytimes by running:

    pip install sleepytimes

If you want to scroll recordings and do some sleep scoring (requires PyQt5)

    sleepytimes

Requirements
------------
- Python 3.5
- numpy
- scipy
- (optional for sleep scoring GUI) PyQt5

License
-------
The project is licensed under the GPLv3 license.
Other licenses available upon request.

Note on authorship
------------------
This package is built upon an existing package by Gio Piantoni, available here:
https://github.com/gpiantoni/phypno.git


