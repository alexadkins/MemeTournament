# Meme Tournament

A single-elimination tournament bracket for end-of-semester meme competitions. Students submit memes, the instructor runs the bracket on a projector, and the class votes by calling out their pick.

---

## Setup

```bash
pip install -r requirements.txt
```

---

## Configuration

All settings live in `settings.py`. Before each run, update the two directory paths:

```python
images_dir = "images"   # folder containing student meme submissions
winners_dir = "winners" # folder where top 4 will be saved (created automatically)
```

The color theme can also be adjusted here. The base palette is defined at the top; `BG`, `LINE_COLOR`, `SELECT`, and `TEXT` control the actual appearance.

---

## Preparing Images

Download student submissions from Canvas as a zip and extract them into a folder. The filenames Canvas generates (`lastnamefirst_userid_submissionid_originalname.ext`) are used as-is — no renaming needed.

Byes are handled automatically. Any number of submissions works; the bracket rounds up to the next power of 2 and distributes byes randomly throughout the first round.

---

## Running

```bash
python3 tournament.py
```

The app opens fullscreen. Matchups are randomized on every run.

---

## Controls

### Bracket view
| Key | Action |
|-----|--------|
| `←` `→` | Navigate between brackets within a round |
| `↑` `↓` | Move between rounds (toward or away from the final) |
| `Enter` | Open the selected bracket in battle mode |

### Battle screen
| Key | Action |
|-----|--------|
| `←` `→` | Select left or right competitor |
| `Enter` | Confirm winner and advance them to the next round |

### Quitting
Close the window or press the window's close button. Quitting early will still attempt to save any finalists determined so far.

---

## Output

When the final battle is confirmed, the top 2 are saved to `winners_dir` with the following filename prefixes:

| Prefix | Place |
|--------|-------|
| `WINNER_` | Champion |
| `RUNNERUP_` | Runner-up |
