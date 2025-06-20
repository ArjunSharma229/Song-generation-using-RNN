import streamlit as st
import numpy as np
import tensorflow as tf
import music21 as m21
import keras
import subprocess
import json

st.title("Text-to-Music Generator")
SEQUENCE_LENGTH = 64
MAPPING_PATH = "mapping.json"
class MelodyGenerator:
    """A class that wraps the LSTM model and offers utilities to generate melodies."""

    def __init__(self, model_path="model.h5"):
        """Constructor that initialises TensorFlow model"""

        self.model_path = model_path
        self.model = keras.models.load_model(model_path)

        with open(MAPPING_PATH, "r") as fp:
            self._mappings = json.load(fp)

        self._start_symbols = ["/"] * SEQUENCE_LENGTH


    def generate_melody(self, seed, num_steps, max_sequence_length, temperature):
        # create seed with start symbols
        seed = seed.split()
        melody = seed
        seed = self._start_symbols + seed

        # map seed to int
        seed = [self._mappings[symbol] for symbol in seed]

        for _ in range(num_steps):

            # limit the seed to max_sequence_length
            seed = seed[-max_sequence_length:]

            # one-hot encode the seed
            onehot_seed = keras.utils.to_categorical(seed, num_classes=len(self._mappings))
            # (1, max_sequence_length, num of symbols in the vocabulary)
            onehot_seed = onehot_seed[np.newaxis, ...]

            # make a prediction
            probabilities = self.model.predict(onehot_seed)[0]
            # [0.1, 0.2, 0.1, 0.6] -> 1
            output_int = self._sample_with_temperature(probabilities, temperature)

            # update seed
            seed.append(output_int)

            # map int to our encoding
            output_symbol = [k for k, v in self._mappings.items() if v == output_int][0]

            # check whether we're at the end of a melody
            if output_symbol == "/":
                break

            # update melody
            melody.append(output_symbol)

        return melody


    def _sample_with_temperature(self, probabilites, temperature):
        predictions = np.log(probabilites) / temperature
        probabilites = np.exp(predictions) / np.sum(np.exp(predictions))

        choices = range(len(probabilites)) # [0, 1, 2, 3]
        index = np.random.choice(choices, p=probabilites)

        return index
    def save_melody(self, melody, step_duration=1, format="midi", file_name="mel.mid"):

        # create a music21 stream
        stream = m21.stream.Stream()

        start_symbol = None
        step_counter = 1

        # parse all the symbols in the melody and create note/rest objects
        for i, symbol in enumerate(melody):

            # handle case in which we have a note/rest
            if symbol != "_" or i + 1 == len(melody):

                # ensure we're dealing with note/rest beyond the first one
                if start_symbol is not None:

                    quarter_length_duration = step_duration * step_counter # 0.25 * 4 = 1

                    
                    if start_symbol == "r":
                        m21_event = m21.note.Rest(quarterLength=quarter_length_duration)

                    
                    else:
                        m21_event = m21.note.Note(int(start_symbol), quarterLength=quarter_length_duration)

                    stream.append(m21_event)

                    
                    step_counter = 1

                start_symbol = symbol

          
            else:
                step_counter += 1

        
        stream.write(format, file_name)

def open_musescore():
    midi_path = "mel.mid"
    midi_stream = m21.converter.parse(midi_path)
    musicxml_path = 'result.musicxml'
    midi_stream.write('musicxml',musicxml_path)
    musescore_exe  =   r'C:\Program Files\MuseScore 4\bin\MuseScore4.exe'
    subprocess.Popen('musescore_exe', musicxml_path)



# Text input for the user

user_input = st.text_input("Enter text for music generation (MIDI Values and / for Rests):")


if st.button("Generate Music"):
    if user_input:
        try:

            # Generate music based on user input
            mg = MelodyGenerator()
            generated_music = mg.generate_melody(user_input, 500, SEQUENCE_LENGTH, 1)
            mg.save_melody(generated_music)

            if generated_music is not None:
                # Save the generated music as a MIDI file
                output_filename = "mel.mid"
                st.success("Music generated successfully!")

                # Provide a link to download the generated music
            # Open the generated music in MuseScore
                if st.button("Click Here to View the Sheet Music"):
                    try:
                        midi_path = "mel.mid"
                        midi_stream = m21.converter.parse(midi_path)
                        musicxml_path = 'result.musicxml'
                        midi_stream.write('musicxml',musicxml_path)
                        musescore_exe  =   r'C:\Program Files\MuseScore 4\bin\MuseScore4.exe'
                        subprocess.Popen('musescore_exe', musicxml_path)
                    except FileNotFoundError:
                        st.error("MuseScore not found. Make sure it's installed and in your system's PATH.")
            else:
                st.warning("No music generated for the given input.")

        except Exception as e:
            st.error(f"Error generating music: {str(e)}")
    else:
        st.warning("Please enter text input for music generation.")
