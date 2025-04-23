#!/usr/bin/env python3
"""
flashgen.py: PDF to Anki flashcard generator using GPT-4 Turbo.
Usage:
    python flashgen.py --input INPUT.pdf --output OUTPUT.apkg --model MODEL --chunk-size CHUNK_SIZE --deck-name DECK_NAME
Requirements:
    pip install PyPDF2 openai genanki
"""
import os
import argparse
import json
from PyPDF2 import PdfReader
import openai
import genanki

def extract_text(pdf_path):
    reader = PdfReader(pdf_path)
    text = []
    for page in reader.pages:
        t = page.extract_text()
        if t:
            text.append(t)
    return "\n".join(text)

def chunk_text(text, max_chars):
    paragraphs = text.split('\n\n')
    chunks = []
    current = ""
    for para in paragraphs:
        if len(current) + len(para) + 2 <= max_chars:
            current += para + "\n\n"
        else:
            if current:
                chunks.append(current.strip())
            if len(para) <= max_chars:
                current = para + "\n\n"
            else:
                for i in range(0, len(para), max_chars):
                    chunks.append(para[i:i+max_chars].strip())
                current = ""
    if current:
        chunks.append(current.strip())
    return chunks

def generate_flashcards(chunks, model):
    flashcards = []
    for chunk in chunks:
        messages = [
            {"role": "system", "content": "You are an assistant that transforms text into flashcard Q&A pairs with tags and difficulty."},
            {"role": "user", "content": f"Generate flashcards for the following text. Respond with a JSON list of objects with keys: question, answer, tags (list of strings), difficulty (easy, medium, hard).\n\nText:\n{chunk}"}
        ]
        response = openai.ChatCompletion.create(
            model=model,
            messages=messages,
            temperature=0.7,
            max_tokens=500
        )
        content = response.choices[0].message.content
        try:
            cards = json.loads(content)
            flashcards.extend(cards)
        except json.JSONDecodeError:
            print("Warning: Failed to parse JSON response. Skipping chunk.")
    return flashcards

def build_deck(flashcards, deck_name, deck_id):
    deck = genanki.Deck(deck_id, deck_name)
    anki_model = genanki.Model(
        1607392319,
        'Simple Model',
        fields=[
            {'name': 'Question'},
            {'name': 'Answer'},
            {'name': 'Tags'},
            {'name': 'Difficulty'},
        ],
        templates=[
            {
                'name': 'Card 1',
                'qfmt': '{{Question}}<br><br><small>Tags: {{Tags}}</small>',
                'afmt': '{{FrontSide}}<hr id="answer">{{Answer}}<br><br><small>Difficulty: {{Difficulty}}</small>',
            },
        ])
    for card in flashcards:
        tags = ' '.join(card.get('tags', []))
        difficulty = card.get('difficulty', '')
        note = genanki.Note(
            model=anki_model,
            fields=[card.get('question',''), card.get('answer',''), tags, difficulty]
        )
        deck.add_note(note)
    return deck

def main():
    parser = argparse.ArgumentParser(description="PDF to Anki flashcard generator.")
    parser.add_argument('--input', '-i', required=True, help='Input PDF file path')
    parser.add_argument('--output', '-o', required=True, help='Output Anki .apkg file path')
    parser.add_argument('--model', default='gpt-4-turbo', help='OpenAI model to use')
    parser.add_argument('--chunk-size', type=int, default=1000, help='Max characters per chunk')
    parser.add_argument('--deck-name', default='Flashcards', help='Name of the Anki deck')
    parser.add_argument('--api-key', default=None, help='OpenAI API key (overrides OPENAI_API_KEY env var)')
    args = parser.parse_args()

    api_key = args.api_key or os.getenv('OPENAI_API_KEY')
    if not api_key:
        print("Error: OpenAI API key not provided. Use --api-key or set OPENAI_API_KEY.")
        exit(1)
    openai.api_key = api_key

    print("Extracting text from PDF...")
    text = extract_text(args.input)
    print("Chunking text...")
    chunks = chunk_text(text, args.chunk_size)
    print(f"Generated {len(chunks)} chunks. Generating flashcards...")
    flashcards = generate_flashcards(chunks, args.model)
    print(f"Generated {len(flashcards)} flashcards. Building Anki deck...")
    deck_id = abs(hash(args.deck_name)) % (10**12)
    deck = build_deck(flashcards, args.deck_name, deck_id)
    print(f"Writing deck to {args.output}...")
    genanki.Package(deck).write_to_file(args.output)
    print("Done.")

if __name__ == '__main__':
    main()
