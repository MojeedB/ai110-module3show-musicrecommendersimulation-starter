# 🎵 Music Recommender Simulation

## Project Summary

In this project you will build and explain a small music recommender system.

Your goal is to:

- Represent songs and a user "taste profile" as data
- Design a scoring rule that turns that data into recommendations
- Evaluate what your system gets right and wrong
- Reflect on how this mirrors real world AI recommenders

Replace this paragraph with your own summary of what your version does.

---

## How The System Works

- What features does each `Song` use in your system
  The main features used for each song are Mood, Genre, Energy, Tempo, Danceability, an Acousticness

- What information does your `UserProfile` store
  The user profile will store the follwoing, mood: chill   genre: lofi   energy: 0.40   tempo: 80 BPM danceability: 0.60   acousticness: 0.80

- How does your `Recommender` compute a score for each song
  The final score is a weighted sum: mood 0.30, genre 0.15, energy 0.20, tempo 0.10, danceability 0.10, acousticness 0.15. This follows a guideline i established: mood outweighs genre, and the energy → tempo and energy → danceability chain which is reflected in the weight ordering.

- How do you choose which songs to recommend
  The scoring rule implemented runs on the songs and grades them accordingly then it is soreted and ranked according to the ranking rule logic and keeps the top songs from the list, also filtering out songs already heard.

You can include a simple diagram or bullet list if helpful.
  Example profile: mood: chill   genre: lofi   energy: 0.40   tempo: 80 BPM danceability: 0.60   acousticness: 0.80
  
  Example result
  | Rank | Song | Mood (sim) | Genre (sim) | Energy | Tempo | Danceability | Acousticness | **Score** |
  |---|---|---|---|---|---|---|---|---|
  | 1 | Midnight Coding | chill (1.0) | lofi (1.0) | 0.98 | 0.98 | 0.98 | 0.91 | **0.98** |
  | 2 | Library Rain | chill (1.0) | lofi (1.0) | 0.95 | 0.91 | 0.98 | 0.94 | **0.97** |
  | 3 | Focus Flow | focused (0.6) | lofi (1.0) | 1.00 | 1.00 | 1.00 | 0.98 | **0.88** |


---

## Getting Started

### Setup

1. Create a virtual environment (optional but recommended):

   ```bash
   python -m venv .venv
   source .venv/bin/activate      # Mac or Linux
   .venv\Scripts\activate         # Windows

2. Install dependencies

```bash
pip install -r requirements.txt
```

3. Run the app:

```bash
python -m src.main
```

### Running Tests

Run the starter tests with:

```bash
pytest
```

You can add more tests in `tests/test_recommender.py`.

---

## Sample Recommendation Output

Paste a sample of your recommender's output here as a text block so a reader can see what it produces:

```
# e.g.:
# User profile: genre=indie, mood=chill, energy=low
# Recommendations:
#   1. ...
#   2. ...
#   3. ...
```

**Screenshot or video** *(optional)*: <!-- Insert a screenshot or demo video link here -->

---

## Experiments You Tried

Use this section to document the experiments you ran. For example:

- What happened when you changed the weight on genre from 2.0 to 0.5
- What happened when you added tempo or valence to the score
- How did your system behave for different types of users

---

## Limitations and Risks

Summarize some limitations of your recommender.

Examples:

- It only works on a tiny catalog
- It does not understand lyrics or language
- It might over favor one genre or mood

You will go deeper on this in your model card.

---

## Reflection

Read and complete `model_card.md`:

[**Model Card**](model_card.md)

Write 1 to 2 paragraphs here about what you learned:

- about how recommenders turn data into predictions
- about where bias or unfairness could show up in systems like this



