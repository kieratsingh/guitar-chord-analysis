#!/usr/bin/env python3
"""
Guitar Chord Analysis Tool

This module provides functionality for analyzing guitar chords,
including chord detection, visualization, and analysis.
"""

import numpy as np
import matplotlib.pyplot as plt
from typing import List, Dict, Tuple, Optional
import json
from itertools import product
from collections import Counter

STRINGS = ['E2', 'A2', 'D3', 'G3', 'B3', 'E4']
NOTE_ORDER = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']
FRET_RANGE = 4
MAX_FINGERS = 4
MAX_FRET = 12

# ------------------ helpers: pitch, notes, strings ------------------ #
def parse_note(note):
    for i, ch in enumerate(note):
        if ch.isdigit():
            return note[:i], int(note[i:])
    raise ValueError(f"Invalid note: {note}")

def note_to_semitone(note):
    name, octave = parse_note(note)
    return NOTE_ORDER.index(name) + 12 * octave

def semitone_to_note(semitone):
    return f"{NOTE_ORDER[semitone % 12]}{semitone // 12}"

def get_note_from_string_fret(base_note, fret):
    if fret == 'X':
        return None
    return semitone_to_note(note_to_semitone(base_note) + int(fret))

def get_chord_notes_from_voicing(voicing):
    notes = []
    for string_note, fret in zip(STRINGS, voicing):
        note = get_note_from_string_fret(string_note, fret)
        if note:
            notes.append(note[:-1])  # pitch-class only
    return sorted(set(notes))

def determine_root_note(voicing):
    # prefer an open-string root if present
    for string_note, fret in zip(STRINGS, voicing):
        if fret == 0:
            note = get_note_from_string_fret(string_note, fret)
            return note[:-1] if note else None
    # otherwise the first non-muted string from low to high
    for string_note, fret in zip(STRINGS, voicing):
        if fret != 'X':
            note = get_note_from_string_fret(string_note, fret)
            return note[:-1] if note else None
    return None

def get_fret_positions(string_note, target_notes):
    base_semitone = note_to_semitone(string_note)
    positions = []
    for fret in range(0, MAX_FRET + 1):
        note = semitone_to_note(base_semitone + fret)
        if note[:-1] in target_notes:
            positions.append(fret)
    positions.append('X')  # allow muting
    return positions


class GuitarChordAnalyzer:
    """A class for analyzing guitar chords and their properties."""
    
    def __init__(self):
        """Initialize the guitar chord analyzer."""
        self.chord_database = self._load_chord_database()
    
    def _load_chord_database(self) -> Dict:
        """Load chord database with common guitar chords."""
        return {
            'C': {'notes': ['C', 'E', 'G'], 'positions': ['x32010', 'x35553']},
            'G': {'notes': ['G', 'B', 'D'], 'positions': ['320003', '355433']},
            'D': {'notes': ['D', 'F#', 'A'], 'positions': ['xx0232', 'x54232']},
            'A': {'notes': ['A', 'C#', 'E'], 'positions': ['x02220', 'x02225']},
            'E': {'notes': ['E', 'G#', 'B'], 'positions': ['022100', '022104']},
            'F': {'notes': ['F', 'A', 'C'], 'positions': ['133211', '133111']},
            'Am': {'notes': ['A', 'C', 'E'], 'positions': ['x02210', 'x02213']},
            'Em': {'notes': ['E', 'G', 'B'], 'positions': ['022000', '022003']},
            'Dm': {'notes': ['D', 'F', 'A'], 'positions': ['xx0231', 'x54231']},
        }
    
    def analyze_chord(self, chord_name: str) -> Optional[Dict]:
        """
        Analyze a specific chord.
        
        Args:
            chord_name: Name of the chord to analyze
            
        Returns:
            Dictionary containing chord information or None if not found
        """
        if chord_name in self.chord_database:
            return self.chord_database[chord_name]
        return None
    
    def get_chord_positions(self, chord_name: str) -> List[str]:
        """
        Get all possible finger positions for a chord.
        
        Args:
            chord_name: Name of the chord
            
        Returns:
            List of finger positions
        """
        chord_info = self.analyze_chord(chord_name)
        if chord_info:
            return chord_info.get('positions', [])
        return []
    
    def get_chord_notes(self, chord_name: str) -> List[str]:
        """
        Get the notes that make up a chord.
        
        Args:
            chord_name: Name of the chord
            
        Returns:
            List of notes in the chord
        """
        chord_info = self.analyze_chord(chord_name)
        if chord_info:
            return chord_info.get('notes', [])
        return []
    
    def list_all_chords(self) -> List[str]:
        """
        Get a list of all available chords.
        
        Returns:
            List of chord names
        """
        return list(self.chord_database.keys())
    
    def visualize_chord(self, chord_name: str, position: str = None):
        """
        Create a simple visualization of a chord.
        
        Args:
            chord_name: Name of the chord to visualize
            position: Specific finger position to show
        """
        chord_info = self.analyze_chord(chord_name)
        if not chord_info:
            print(f"Chord '{chord_name}' not found in database.")
            return
        
        print(f"\n=== {chord_name} Chord ===")
        print(f"Notes: {', '.join(chord_info['notes'])}")
        print(f"Available positions: {', '.join(chord_info['positions'])}")
        
        if position and position in chord_info['positions']:
            print(f"\nFinger position: {position}")
            # Here you could add more detailed visualization
            # like ASCII art of the fretboard


def main():
    """Main function to demonstrate the guitar chord analyzer."""
    analyzer = GuitarChordAnalyzer()
    
    print("🎸 Guitar Chord Analysis Tool")
    print("=" * 40)
    
    # List all available chords
    print(f"Available chords: {', '.join(analyzer.list_all_chords())}")
    
    # Analyze a specific chord
    test_chord = "C"
    analyzer.visualize_chord(test_chord)
    
    # Get chord notes
    notes = analyzer.get_chord_notes(test_chord)
    print(f"\n{test_chord} chord consists of: {', '.join(notes)}")
    
    # Get chord positions
    positions = analyzer.get_chord_positions(test_chord)
    print(f"Finger positions for {test_chord}: {', '.join(positions)}")


if __name__ == "__main__":
    main()
