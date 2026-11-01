# 🎵 Music Recommender Simulation

## Project Summary

This recommender is a content-based system that reads a catalog of 20 songs from a CSV file and compares each song's attributes to a user's stated preferences. The user profile can include a favorite genre and mood plus target values for energy, tempo, danceability, and acousticness. Each song gets a score between 0 and 1, built from a weighted sum in which mood counts most, genre counts less, and numeric features earn more points the closer they are to the target. Related moods and genres, like chill and relaxed or pop and indie pop, earn partial credit instead of a flat zero, and any field the user leaves out is skipped so partial profiles still work. The top three or five songs are returned, highest score first, with a plain-language reason for each feature so the user can see why a song ranked where it did.

---

## How The System Works

Streaming platforms like Spotify, YouTube, Netflix and TikTok use a multi-stage pipeline that narrows millions of songs to a ranked  shortlist, learning from implicit behavior like skips, replays, and saves. Collaborative filtering recommends songs based on what similar users enjoyed (great for discovery, but it struggles with new songs or users). Content-based filtering recommends songs whose attributes, like tempo, energy, and mood, match your taste profile (it works on day one, but it tends to stay in a bubble). Real systems blend both.  

- What features does each `Song` use in your system - 
  The main features used for each song are Mood, Genre, Energy, Tempo, Danceability, an Acousticness

- What information does your `UserProfile` store - 
  The user profile will store the follwoing, mood: chill   genre: lofi   energy: 0.40   tempo: 80 BPM danceability: 0.60   acousticness: 0.80

- How does your `Recommender` compute a score for each song - 
  The final score is a weighted sum: mood 0.30, genre 0.15, energy 0.20, tempo 0.10, danceability 0.10, acousticness 0.15. This follows a guideline i established: mood outweighs genre, and the energy → tempo and energy → danceability chain which is reflected in the weight ordering.

- How do you choose which songs to recommend - 
  The scoring rule implemented runs on the songs and grades them accordingly then it is soreted and ranked according to the ranking rule logic and keeps the top songs from the list, also filtering out songs already heard.


 Example profile: mood: chill   genre: lofi   energy: 0.40   tempo: 80 BPM danceability: 0.60   acousticness: 0.80
  
  Example result
  | Rank | Song | Mood (sim) | Genre (sim) | Energy | Tempo | Danceability | Acousticness | **Score** |
  |---|---|---|---|---|---|---|---|---|
  | 1 | Midnight Coding | chill (1.0) | lofi (1.0) | 0.98 | 0.98 | 0.98 | 0.91 | **0.98** |
  | 2 | Library Rain | chill (1.0) | lofi (1.0) | 0.95 | 0.91 | 0.98 | 0.94 | **0.97** |
  | 3 | Focus Flow | focused (0.6) | lofi (1.0) | 1.00 | 1.00 | 1.00 | 0.98 | **0.88** |


---


## Sample Recommendation Output

```
# User profile: user_prefs = {"favorite_genre": "pop", "favorite_mood": "happy", "target_energy": 0.8}

========================================================================
 TOP 5 RECOMMENDATIONS
========================================================================

#1  Sunrise City                                          Score: 0.99
------------------------------------------------------------------------
  - mood: wanted happy, got happy (similarity 1.00, +0.46)
  - genre: wanted pop, got pop (similarity 1.00, +0.23)
  - energy: wanted 0.80, got 0.82 (similarity 0.98, +0.30)

#2  Rooftop Lights                                        Score: 0.92
------------------------------------------------------------------------
  - mood: wanted happy, got happy (similarity 1.00, +0.46)
  - genre: wanted pop, got indie pop (similarity 0.70, +0.16)
  - energy: wanted 0.80, got 0.76 (similarity 0.96, +0.30)

#3  Fiesta Sunrise                                        Score: 0.71
------------------------------------------------------------------------
  - mood: wanted happy, got playful (similarity 0.70, +0.32)
  - genre: wanted pop, got latin (similarity 0.40, +0.09)
  - energy: wanted 0.80, got 0.85 (similarity 0.95, +0.29)

#4  Gym Hero                                              Score: 0.64
------------------------------------------------------------------------
  - mood: wanted happy, got intense (similarity 0.30, +0.14)
  - genre: wanted pop, got pop (similarity 1.00, +0.23)
  - energy: wanted 0.80, got 0.93 (similarity 0.87, +0.27)

#5  Neon Overdrive                                        Score: 0.63
------------------------------------------------------------------------
  - mood: wanted happy, got energetic (similarity 0.60, +0.28)
  - genre: wanted pop, got edm (similarity 0.40, +0.09)
  - energy: wanted 0.80, got 0.96 (similarity 0.84, +0.26)

========================================================================
```
---

## Experiments You Tried

Use this section to document the experiments you ran. For example:

- The genre weight was increased from 0.30 to 2.15 to test the algorithm's sensitivity. Sunrise City stayed first in both runs, but Gym Hero rose from third to second because it shares the pop genre, even though its mood (intense) doesn't match the requested happy mood. This shows that a heavy genre weight makes the recommender favor exact genre matches over songs that fit the user's mood and energy better, so the weight needs to be balanced against the other features.

- Valence partly overlaps with mood. Moods like sad, melancholic, and happy already imply a valence level, so a profile that asks for a sad mood and a low valence is partly counting the same thing twice. For those profiles, leaving valence out changes the results very little. It matters more when a profile doesn't specify a mood, or when a mood spans a range of valence values, as intense does (Storm Runner at 0.48 vs. Gym Hero at 0.77).

- For clear, realistic profiles like High-Energy Pop, Chill Lofi, Deep Intense Rock, Rainy Day Folk, Gym EDM, and Sunday Jazz, the system behaved well: the exact-match song came first with a score of 0.96 to 1.0, and partial credit for related moods and genres produced sensible runners-up. Odd or contradictory profiles never crashed it, but they exposed quiet weaknesses: unknown words like "melancholy," "calm," and "k-pop" simply scored zero with no warning, and out-of-range values such as an energy of 1.8 were not validated. When a profile's labels clashed with its audio targets, as in Genre Traitor, the numeric features won because they carry more total weight than mood and genre. The system always returns something even when the best score is only about 0.5, so a low score is the only hint of a poor match, and a small catalog means scores fall off fast after the first result.

---

## Limitations and Risks

- Tiny, invented catalog. There are 20 songs, and many genres and moods have just one, so scores drop off quickly after the first match. The feature values are made up, not measured.

- Silent failure on unknown input. Moods or genres not in the tables, like "melancholy" or "k-pop", score 0 with no warning. Out-of-range values, like energy 1.8, aren't validated.

- Contradictory profiles resolve toward the numbers. Mood and genre carry less total weight than the numeric features, so audio targets can override a stated genre.
---

## Reflection

 The first thing i noticed when attempting this was the potential for bias in the data, for example i weighted mood higher than genre as a personal preference rather than an objective fact. For every kind of algorithm out there that uses mathematical models to make predictions there will be a bias based on what the developers percieve to hold more weight over what can be said to be objective.



