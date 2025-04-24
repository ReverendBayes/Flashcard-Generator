# PDF Flashcard Generator

**PDF → Anki flashcards** in under 10 seconds with GPT-4 Turbo.  
Stop wrestling with highlights and manual Q/A—AutoFlash does the heavy lifting.

# Why you need it 
Convert PDFs into Anki flashcards using GPT-4 Turbo. Drop in any PDF (lecture slides, paper, textbook chapter). It generates flashcards.

---

## Overview

AutoFlash is a single-file Google Colab (flashcard_generator.ipynb) or Python script (`flashgen.py`) that:

1. **Extracts** text from any PDF (papers, slides, textbooks).  
2. **Chunks** it intelligently to respect concept boundaries.  
3. **Calls GPT-4 Turbo** to generate JSON-only flashcards:  
   - **Question**  
   - **Answer**  
   - **Tags**  
   - **Difficulty** (easy/medium/hard)  
4. **Builds** an Anki `.apkg` deck via Genanki.

All you need is one script—no Docker, no multi-repo spaghetti.  

---

## Features

- **Single-file CLI**: drop in `flashgen.py` and go.  
- **Smart chunking**: minimizes concept splits and avoids token limits.  
- **Zero-temp JSON-only LLM prompt**: deterministic, parse-friendly output.  
- **Genanki integration**: ready-to-import `.apkg` deck.  
- **Tags & Difficulty**: automates metadata for targeted review.  
- **Configurable**: adjust model, chunk size, deck name via flags.

---

## Requirements

- Python 3.7+  
- [PyPDF2](https://pypi.org/project/PyPDF2/)  
- [openai](https://pypi.org/project/openai/) v0.28.0  
- [genanki](https://pypi.org/project/genanki/)  

Install with:

```bash
pip install PyPDF2 openai==0.28.0 genanki
```
## Quickstart
```bash
python flashgen.py \
  --input your_document.pdf \
  --output your_flashcards.apkg
```
