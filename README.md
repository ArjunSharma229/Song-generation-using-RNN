# Song generation using RNN
To get this project. pip install the music21 library of python.

music21 is a Python library for computer-aided musicology, music theory, and composition analysis. It provides a set of tools for working with music notation, including the ability to read and write various file formats (such as MIDI, MusicXML, and ABC), analyze and manipulate musical data, and generate new compositions.

The library includes modules for working with musical elements such as notes, chords, and scales, as well as for building complex musical structures such as musical phrases and sections. It also provides functionality for creating and manipulating musical scores, conducting musical analyses, and visualizing musical data.

File descriptions:
 
1)data_preprocessing.ipynb:
performing data preprocessing on the given dataset which includes several steps:
a)converting 'krn' files to 'musicxml' format
  
b)accepting the songs only in acceptable duarations (in this case: Quarter Note)
  
c)transposing the song. transposing means to change the key of the song without changing the pitch differences between the notes. all the songs in a major key transposed to C major and all the songs in a minor key were transposed to A minor.
  
d)encoding the song. mapping the notes to their midi values and denoting the rests by a symbol
  
e)combining all these enocoded songs in a single file

2) test.ipynb:
Training the model using RNN LSTM on the training sequences generated during the data preprocessing.

3)generator.ipynb:
takes a seed and generates a melody based on that and saves the generated melody in a midi format.

4)mapping.json:
key value pairs of notes and rests and their midi values

5)file_dataset:
single file dataset of all the encoded songs

6)mel.midi:
This is final generated melody. this can be seen as a score in sheet music using musescore4


