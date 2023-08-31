from flask import Flask, render_template, request, send_from_directory
from tensorflow.keras.models import model_from_json
import numpy as np
import os
from music21 import *
import sys
import warnings
warnings.filterwarnings("ignore")
warnings.simplefilter("ignore")
np.random.seed(42)
from collections import Counter
app = Flask(__name__)


#Helping function
def extract_notes(file):
    notes = []
    pick = None
    for j in file:
        songs = instrument.partitionByInstrument(j)
        for part in songs.parts:
            pick = part.recurse()
            for element in pick:
                if isinstance(element, note.Note):
                    notes.append(str(element.pitch))
                elif isinstance(element, chord.Chord):
                    notes.append(".".join(str(n) for n in element.normalOrder))

    return notes

def chords_n_notes(Snippet):
    Melody = []
    offset = 0 #Incremental
    for i in Snippet:
        #If it is chord
        if ("." in i or i.isdigit()):
            chord_notes = i.split(".") #Seperating the notes in chord
            notes = []
            for j in chord_notes:
                inst_note=int(j)
                note_snip = note.Note(inst_note)
                notes.append(note_snip)
                chord_snip = chord.Chord(notes)
                chord_snip.offset = offset
                Melody.append(chord_snip)
        # pattern is a note
        else:
            note_snip = note.Note(i)
            note_snip.offset = offset
            Melody.append(note_snip)
        # increase offset each iteration so that notes do not stack
        offset += 1
    Melody_midi = stream.Stream(Melody)
    return Melody_midi


def Malody_Generator(model, X_seed, Note_Count, length):
    seed = X_seed[np.random.randint(0, len(X_seed)-1)]
    Music = ""
    Notes_Generated = []
    # *********************************************************************
    #Loading the list of chopin's midi files as stream
    filepath = "classical-music-midi/chopin/"
    #Getting midi files
    all_midis= []
    for i in os.listdir(filepath):
        if i.endswith(".mid"):
            tr = filepath+i
            midi = converter.parse(tr)
            all_midis.append(midi)

    #Getting the list of notes as Corpus
    Corpus= extract_notes(all_midis)

    count_num = Counter(Corpus)

    #Getting a list of rare chords
    rare_note = []
    for index, (key, value) in enumerate(count_num.items()):
        if value < 100:
            m =  key
            rare_note.append(m)

    #Eleminating the rare notes
    for element in Corpus:
        if element in rare_note:
            Corpus.remove(element)

    # Storing all the unique characters present in my corpus to bult a mapping dic.
    symb = sorted(list(set(Corpus)))

    L_symb = len(symb) #length of total unique characters

    #Building dictionary to access the vocabulary from indices and vice versa
    reverse_mapping = dict((i, c) for i, c in enumerate(symb))

    # *********************************************************************
    for i in range(Note_Count):
        seed = seed.reshape(1, length, 1)
        prediction = model.predict(seed, verbose=0)[0]
        prediction = np.log(prediction) / 1.0  # diversity
        exp_preds = np.exp(prediction)
        prediction = exp_preds / np.sum(exp_preds)
        index = np.argmax(prediction)
        index_N = index / float(L_symb)
        Notes_Generated.append(index)
        print(Notes_Generated)
        Music = [reverse_mapping[char] for char in Notes_Generated]
        seed = np.insert(seed[0], len(seed[0]), index_N)
        seed = seed[1:]
    Melody = chords_n_notes(Music)
    Melody_midi = stream.Stream(Melody)
    # Save generated melody to MIDI file
    Melody.write('midi', 'generated_midi/Melody_Generated.mid')
    return Melody_midi



@app.route('/')
def index():
    return render_template('index.html')

@app.route('/generate', methods=['POST'])
def generate_music():
    # Load the model architecture from JSON file
    with open('content/model_architecture.json', 'r') as json_file:
        loaded_model_architecture = json_file.read()

    loaded_model = model_from_json(loaded_model_architecture)

    # Load the trained weights
    loaded_model.load_weights('content/final_model_weights.h5')

    # Load X_seed from your saved data
    X_seed = np.load('content/X_seed.npy')

    # Generate music
    Melody = Malody_Generator(loaded_model, X_seed, 200, length = 40)
    
    # Save generated melody to MIDI file
    generated_midi_path = 'generated_midi/Melody_Generated.mid'
    Melody.write('midi', generated_midi_path)

    return render_template('index.html', generated_midi_path=generated_midi_path)

@app.route('/download/<path:filename>', methods=['GET', 'POST'])
def download(filename):
    return send_from_directory(directory='generated_midi', filename=filename)

if __name__ == '__main__':
    app.run(debug=True)
