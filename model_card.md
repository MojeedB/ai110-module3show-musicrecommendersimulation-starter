# 🎧 Model Card: Music Recommender Simulation

## 1. Model Name  

    Music Match

---

## 2. Intended Use  

The recommender produces content-based, song-level recommendations: a short ranked list from the 20-song catalog, each with a 0–1 match score and a plain-language explanation. It scores songs by how closely their mood, genre, and audio features match a profile the user fills in, and it skips any field the user leaves out. It assumes the user has one fixed, explicitly stated taste, that closer to a target is always better, that every user weights features the same way and shares the designer's idea of related moods and genres, and that they want songs matching their profile, with no novelty or variety.

---

## 3. How the Model Works  

Each song gets a score from 0 to 1 that says how well it fits what the user asked for. The higher the score, the better the match.
If the song's mood or genre is exactly what the user wanted, it gets full credit. If it's a close cousin, it gets partial credit. For example, "relaxed" counts as 80% of "chill," and "indie pop" counts as 70% of "pop." Unrelated ones get nothing.  
The closer the song's value is to the user's target, the more credit it gets. A perfect hit earns 1.0, and the credit shrinks as the gap grows. 
All songs are ranked by score, and the top few are shown with a line explaining what earned each point.


---

## 4. Data  

The dataset is a small CSV file of 20 made-up songs, where each song has a title, artist, genre, and mood plus numbers from 0 to 1 for energy, valence (how happy it sounds), danceability, and acousticness, and a tempo in BPM. It covers 17 genres (such as pop, lofi, rock, jazz, and metal) and 16 moods (such as happy, chill, sad, and angry), but most appear only once, so the catalog is varied but very thin. Ten more data sets were added from the initial 10.

---

## 5. Strengths  

The system works best for clear, consistent profiles like Chill Lofi, Deep Intense Rock, Gym EDM, and Sunday Jazz, where the exact-match song comes first with a score of 0.96 to 1.0. Its partial credit for related moods and genres also produces sensible runners-up, and its per-feature explanations make it easy to see why each song ranked where it did.

---

## 6. Limitations and Bias 


The system struggles with unusual or contradictory profiles: words outside its tables, like "melancholy" or "k-pop," silently score zero, out-of-range values are not validated, and when labels clash with audio targets (as in Genre Traitor) the numbers win and the stated genre is overridden. It can behave unfairly toward users whose tastes don't fit its assumptions, since it treats every user's taste as one fixed profile, applies the same weights and the designer's idea of "related" moods and genres to everyone, and has only one or two songs for many genres and moods, so niche listeners get thin results. It also always returns a list even when the best match is poor, so a low score is the only hint that nothing fit well. 

---

## 7. Evaluation  

We tested the recommender with 14 user profiles: six realistic ones (High-Energy Pop, Chill Lofi, Deep Intense Rock, Rainy Day Folk, Gym EDM, Sunday Jazz), eight edge cases (conflicting signals, an unknown genre, all-zero and out-of-range values, an all-average profile, messy capitalization, a genre-only profile, and a genre that contradicts the audio targets), plus several partial profiles with fields missing. We checked that the best-fitting song came first with a score near 1.0, that related moods and genres filled the next spots, that the explanations added up to the final score, and that odd input didn't crash anything. We also hand-calculated the chill-lofi scores and compared them with the program's output, compared rankings at three genre weights, and ran the two unit tests, which pass.

The results were mostly sensible, but some surprises showed where the system is fragile. A mismatch between the starter profile's keys and the scorer's keys gave every song 0.00, a blank mood string dragged scores down until we treated it as missing, and raising the genre weight to 2.15 pushed a mood-mismatched song (Gym Hero) up to second place. Contradictory profiles resolved toward the numeric features, so a metal fan with very low energy got classical and folk, and typos like "melancholy" scored zero without any warning.


### SAMPLE TEST PROFILES


```
### PROFILE: High-Energy Pop

========================================================================
 TOP 5 RECOMMENDATIONS
========================================================================

#1  Sunrise City                                          Score: 0.96
------------------------------------------------------------------------
  - mood: wanted happy, got happy (similarity 1.00, +0.30)
  - genre: wanted pop, got pop (similarity 1.00, +0.15)
  - energy: wanted 0.90, got 0.82 (similarity 0.92, +0.18)
  - tempo: wanted 128 bpm, got 118 bpm (similarity 0.91, +0.09)
  - danceability: wanted 0.85, got 0.79 (similarity 0.94, +0.09)
  - acousticness: wanted 0.15, got 0.18 (similarity 0.97, +0.15)

#2  Rooftop Lights                                        Score: 0.89
------------------------------------------------------------------------
  - mood: wanted happy, got happy (similarity 1.00, +0.30)
  - genre: wanted pop, got indie pop (similarity 0.70, +0.11)
  - energy: wanted 0.90, got 0.76 (similarity 0.86, +0.17)
  - tempo: wanted 128 bpm, got 124 bpm (similarity 0.96, +0.10)
  - danceability: wanted 0.85, got 0.82 (similarity 0.97, +0.10)
  - acousticness: wanted 0.15, got 0.35 (similarity 0.80, +0.12)

#3  Gym Hero                                              Score: 0.76
------------------------------------------------------------------------
  - mood: wanted happy, got intense (similarity 0.30, +0.09)
  - genre: wanted pop, got pop (similarity 1.00, +0.15)
  - energy: wanted 0.90, got 0.93 (similarity 0.97, +0.19)
  - tempo: wanted 128 bpm, got 132 bpm (similarity 0.96, +0.10)
  - danceability: wanted 0.85, got 0.88 (similarity 0.97, +0.10)
  - acousticness: wanted 0.15, got 0.05 (similarity 0.90, +0.14)

#4  Fiesta Sunrise                                        Score: 0.76
------------------------------------------------------------------------
  - mood: wanted happy, got playful (similarity 0.70, +0.21)
  - genre: wanted pop, got latin (similarity 0.40, +0.06)
  - energy: wanted 0.90, got 0.85 (similarity 0.95, +0.19)
  - tempo: wanted 128 bpm, got 100 bpm (similarity 0.74, +0.07)
  - danceability: wanted 0.85, got 0.92 (similarity 0.93, +0.09)
  - acousticness: wanted 0.15, got 0.25 (similarity 0.90, +0.14)

#5  Neon Overdrive                                        Score: 0.75
------------------------------------------------------------------------
  - mood: wanted happy, got energetic (similarity 0.60, +0.18)
  - genre: wanted pop, got edm (similarity 0.40, +0.06)
  - energy: wanted 0.90, got 0.96 (similarity 0.94, +0.19)
  - tempo: wanted 128 bpm, got 128 bpm (similarity 1.00, +0.10)
  - danceability: wanted 0.85, got 0.91 (similarity 0.94, +0.09)
  - acousticness: wanted 0.15, got 0.03 (similarity 0.88, +0.13)

========================================================================

### PROFILE: Chill Lofi

========================================================================
 TOP 5 RECOMMENDATIONS
========================================================================

#1  Midnight Coding                                       Score: 0.98
------------------------------------------------------------------------
  - mood: wanted chill, got chill (similarity 1.00, +0.30)
  - genre: wanted lofi, got lofi (similarity 1.00, +0.15)
  - energy: wanted 0.40, got 0.42 (similarity 0.98, +0.20)
  - tempo: wanted 80 bpm, got 78 bpm (similarity 0.98, +0.10)
  - danceability: wanted 0.60, got 0.62 (similarity 0.98, +0.10)
  - acousticness: wanted 0.80, got 0.71 (similarity 0.91, +0.14)

#2  Library Rain                                          Score: 0.97
------------------------------------------------------------------------
  - mood: wanted chill, got chill (similarity 1.00, +0.30)
  - genre: wanted lofi, got lofi (similarity 1.00, +0.15)
  - energy: wanted 0.40, got 0.35 (similarity 0.95, +0.19)
  - tempo: wanted 80 bpm, got 72 bpm (similarity 0.93, +0.09)
  - danceability: wanted 0.60, got 0.58 (similarity 0.98, +0.10)
  - acousticness: wanted 0.80, got 0.86 (similarity 0.94, +0.14)

#3  Focus Flow                                            Score: 0.88
------------------------------------------------------------------------
  - mood: wanted chill, got focused (similarity 0.60, +0.18)
  - genre: wanted lofi, got lofi (similarity 1.00, +0.15)
  - energy: wanted 0.40, got 0.40 (similarity 1.00, +0.20)
  - tempo: wanted 80 bpm, got 80 bpm (similarity 1.00, +0.10)
  - danceability: wanted 0.60, got 0.60 (similarity 1.00, +0.10)
  - acousticness: wanted 0.80, got 0.78 (similarity 0.98, +0.15)

#4  Spacewalk Thoughts                                    Score: 0.86
------------------------------------------------------------------------
  - mood: wanted chill, got chill (similarity 1.00, +0.30)
  - genre: wanted lofi, got ambient (similarity 0.60, +0.09)
  - energy: wanted 0.40, got 0.28 (similarity 0.88, +0.18)
  - tempo: wanted 80 bpm, got 60 bpm (similarity 0.81, +0.08)
  - danceability: wanted 0.60, got 0.41 (similarity 0.81, +0.08)
  - acousticness: wanted 0.80, got 0.92 (similarity 0.88, +0.13)

#5  Coffee Shop Stories                                   Score: 0.85
------------------------------------------------------------------------
  - mood: wanted chill, got relaxed (similarity 0.80, +0.24)
  - genre: wanted lofi, got jazz (similarity 0.60, +0.09)
  - energy: wanted 0.40, got 0.37 (similarity 0.97, +0.19)
  - tempo: wanted 80 bpm, got 90 bpm (similarity 0.91, +0.09)
  - danceability: wanted 0.60, got 0.54 (similarity 0.94, +0.09)
  - acousticness: wanted 0.80, got 0.89 (similarity 0.91, +0.14)

========================================================================

### PROFILE: Deep Intense Rock

========================================================================
 TOP 5 RECOMMENDATIONS
========================================================================

#1  Storm Runner                                          Score: 0.99
------------------------------------------------------------------------
  - mood: wanted intense, got intense (similarity 1.00, +0.30)
  - genre: wanted rock, got rock (similarity 1.00, +0.15)
  - energy: wanted 0.92, got 0.91 (similarity 0.99, +0.20)
  - tempo: wanted 150 bpm, got 152 bpm (similarity 0.98, +0.10)
  - danceability: wanted 0.65, got 0.66 (similarity 0.99, +0.10)
  - acousticness: wanted 0.08, got 0.10 (similarity 0.98, +0.15)

#2  Gym Hero                                              Score: 0.85
------------------------------------------------------------------------
  - mood: wanted intense, got intense (similarity 1.00, +0.30)
  - genre: wanted rock, got pop (similarity 0.30, +0.05)
  - energy: wanted 0.92, got 0.93 (similarity 0.99, +0.20)
  - tempo: wanted 150 bpm, got 132 bpm (similarity 0.83, +0.08)
  - danceability: wanted 0.65, got 0.88 (similarity 0.77, +0.08)
  - acousticness: wanted 0.08, got 0.05 (similarity 0.97, +0.15)

#3  Iron Requiem                                          Score: 0.80
------------------------------------------------------------------------
  - mood: wanted intense, got angry (similarity 0.70, +0.21)
  - genre: wanted rock, got metal (similarity 0.60, +0.09)
  - energy: wanted 0.92, got 0.98 (similarity 0.94, +0.19)
  - tempo: wanted 150 bpm, got 168 bpm (similarity 0.83, +0.08)
  - danceability: wanted 0.65, got 0.45 (similarity 0.80, +0.08)
  - acousticness: wanted 0.08, got 0.04 (similarity 0.96, +0.14)

#4  Neon Overdrive                                        Score: 0.64
------------------------------------------------------------------------
  - mood: wanted intense, got energetic (similarity 0.50, +0.15)
  - genre: wanted rock, got edm (similarity 0.00, +0.00)
  - energy: wanted 0.92, got 0.96 (similarity 0.96, +0.19)
  - tempo: wanted 150 bpm, got 128 bpm (similarity 0.80, +0.08)
  - danceability: wanted 0.65, got 0.91 (similarity 0.74, +0.07)
  - acousticness: wanted 0.08, got 0.03 (similarity 0.95, +0.14)

#5  Sunrise City                                          Score: 0.61
------------------------------------------------------------------------
  - mood: wanted intense, got happy (similarity 0.30, +0.09)
  - genre: wanted rock, got pop (similarity 0.30, +0.05)
  - energy: wanted 0.92, got 0.82 (similarity 0.90, +0.18)
  - tempo: wanted 150 bpm, got 118 bpm (similarity 0.70, +0.07)
  - danceability: wanted 0.65, got 0.79 (similarity 0.86, +0.09)
  - acousticness: wanted 0.08, got 0.18 (similarity 0.90, +0.14)

========================================================================

### PROFILE: Conflicted Sad Raver

========================================================================
 TOP 5 RECOMMENDATIONS
========================================================================

#1  Neon Overdrive                                        Score: 0.55
------------------------------------------------------------------------
  - mood: wanted melancholy, got energetic (similarity 0.00, +0.00)
  - genre: wanted edm, got edm (similarity 1.00, +0.15)
  - energy: wanted 0.95, got 0.96 (similarity 0.99, +0.20)
  - tempo: wanted 140 bpm, got 128 bpm (similarity 0.89, +0.09)
  - danceability: wanted 0.90, got 0.91 (similarity 0.99, +0.10)
  - acousticness: wanted 0.95, got 0.03 (similarity 0.08, +0.01)

#2  Gym Hero                                              Score: 0.46
------------------------------------------------------------------------
  - mood: wanted melancholy, got intense (similarity 0.00, +0.00)
  - genre: wanted edm, got pop (similarity 0.40, +0.06)
  - energy: wanted 0.95, got 0.93 (similarity 0.98, +0.20)
  - tempo: wanted 140 bpm, got 132 bpm (similarity 0.93, +0.09)
  - danceability: wanted 0.90, got 0.88 (similarity 0.98, +0.10)
  - acousticness: wanted 0.95, got 0.05 (similarity 0.10, +0.02)

#3  Night Drive Loop                                      Score: 0.45
------------------------------------------------------------------------
  - mood: wanted melancholy, got moody (similarity 0.00, +0.00)
  - genre: wanted edm, got synthwave (similarity 0.60, +0.09)
  - energy: wanted 0.95, got 0.75 (similarity 0.80, +0.16)
  - tempo: wanted 140 bpm, got 110 bpm (similarity 0.72, +0.07)
  - danceability: wanted 0.90, got 0.73 (similarity 0.83, +0.08)
  - acousticness: wanted 0.95, got 0.22 (similarity 0.27, +0.04)

#4  Sunrise City                                          Score: 0.44
------------------------------------------------------------------------
  - mood: wanted melancholy, got happy (similarity 0.00, +0.00)
  - genre: wanted edm, got pop (similarity 0.40, +0.06)
  - energy: wanted 0.95, got 0.82 (similarity 0.87, +0.17)
  - tempo: wanted 140 bpm, got 118 bpm (similarity 0.80, +0.08)
  - danceability: wanted 0.90, got 0.79 (similarity 0.89, +0.09)
  - acousticness: wanted 0.95, got 0.18 (similarity 0.23, +0.03)

#5  Rooftop Lights                                        Score: 0.40
------------------------------------------------------------------------
  - mood: wanted melancholy, got happy (similarity 0.00, +0.00)
  - genre: wanted edm, got indie pop (similarity 0.00, +0.00)
  - energy: wanted 0.95, got 0.76 (similarity 0.81, +0.16)
  - tempo: wanted 140 bpm, got 124 bpm (similarity 0.85, +0.09)
  - danceability: wanted 0.90, got 0.82 (similarity 0.92, +0.09)
  - acousticness: wanted 0.95, got 0.35 (similarity 0.40, +0.06)

========================================================================

### PROFILE: Minimal Profile

========================================================================
 TOP 5 RECOMMENDATIONS
========================================================================

#1  Storm Runner                                          Score: 1.00
------------------------------------------------------------------------
  - genre: wanted rock, got rock (similarity 1.00, +1.00)

#2  Iron Requiem                                          Score: 0.60
------------------------------------------------------------------------
  - genre: wanted rock, got metal (similarity 0.60, +0.60)

#3  Sunrise City                                          Score: 0.30
------------------------------------------------------------------------
  - genre: wanted rock, got pop (similarity 0.30, +0.30)

#4  Gym Hero                                              Score: 0.30
------------------------------------------------------------------------
  - genre: wanted rock, got pop (similarity 0.30, +0.30)

#5  Rooftop Lights                                        Score: 0.30
------------------------------------------------------------------------
  - genre: wanted rock, got indie pop (similarity 0.30, +0.30)

========================================================================

### PROFILE: Genre Traitor

========================================================================
 TOP 5 RECOMMENDATIONS
========================================================================

#1  Winter Nocturne                                       Score: 0.56
------------------------------------------------------------------------
  - mood: wanted intense, got melancholic (similarity 0.20, +0.06)
  - genre: wanted metal, got classical (similarity 0.00, +0.00)
  - energy: wanted 0.05, got 0.18 (similarity 0.87, +0.17)
  - tempo: wanted 50 bpm, got 62 bpm (similarity 0.98, +0.10)
  - danceability: wanted 0.10, got 0.25 (similarity 0.85, +0.09)
  - acousticness: wanted 0.95, got 0.97 (similarity 0.98, +0.15)

#2  Hollow Pines                                          Score: 0.50
------------------------------------------------------------------------
  - mood: wanted intense, got sad (similarity 0.20, +0.06)
  - genre: wanted metal, got folk (similarity 0.00, +0.00)
  - energy: wanted 0.05, got 0.30 (similarity 0.75, +0.15)
  - tempo: wanted 50 bpm, got 84 bpm (similarity 0.78, +0.08)
  - danceability: wanted 0.10, got 0.40 (similarity 0.70, +0.07)
  - acousticness: wanted 0.95, got 0.91 (similarity 0.96, +0.14)

#3  Storm Runner                                          Score: 0.50
------------------------------------------------------------------------
  - mood: wanted intense, got intense (similarity 1.00, +0.30)
  - genre: wanted metal, got rock (similarity 0.60, +0.09)
  - energy: wanted 0.05, got 0.91 (similarity 0.14, +0.03)
  - tempo: wanted 50 bpm, got 152 bpm (similarity 0.15, +0.01)
  - danceability: wanted 0.10, got 0.66 (similarity 0.44, +0.04)
  - acousticness: wanted 0.95, got 0.10 (similarity 0.15, +0.02)

#4  Spacewalk Thoughts                                    Score: 0.47
------------------------------------------------------------------------
  - mood: wanted intense, got chill (similarity 0.00, +0.00)
  - genre: wanted metal, got ambient (similarity 0.00, +0.00)
  - energy: wanted 0.05, got 0.28 (similarity 0.77, +0.15)
  - tempo: wanted 50 bpm, got 60 bpm (similarity 1.00, +0.10)
  - danceability: wanted 0.10, got 0.41 (similarity 0.69, +0.07)
  - acousticness: wanted 0.95, got 0.92 (similarity 0.97, +0.15)

#5  Iron Requiem                                          Score: 0.45
------------------------------------------------------------------------
  - mood: wanted intense, got angry (similarity 0.70, +0.21)
  - genre: wanted metal, got metal (similarity 1.00, +0.15)
  - energy: wanted 0.05, got 0.98 (similarity 0.07, +0.01)
  - tempo: wanted 50 bpm, got 168 bpm (similarity 0.00, +0.00)
  - danceability: wanted 0.10, got 0.45 (similarity 0.65, +0.07)
  - acousticness: wanted 0.95, got 0.04 (similarity 0.09, +0.01)

========================================================================
```
---

## 8. Future Work  

- Improved dataset
- Addition data points to calculate, 
- Better ways to explain recommendations  
- Improving diversity among the top results  
- Handling more complex user tastes  
- Let users set their own weights

---

## 9. Personal Reflection  

The most interesting finding was how much one weight can change the results, and how convincing a bad result can look. When the genre weight went from 0.30 to 2.15, Gym Hero moved from third to second for a happy pop listener. Gym Hero is a pop song, but its mood is intense. At first that looked like the system correctly favoring a genre match. Looking closer, a happy listener was better served by Rooftop Lights (happy, indie pop), which had been second.

A related surprise came from the Genre Traitor profile, which asked for metal and intense but with very low energy and high acousticness. The recommender returned classical and folk songs and ignored the stated genre. The cause is the weight split: the audio features carry 0.55 of the score and mood plus genre carry 0.45, so when they disagree the numbers win. The system has no way to flag that the profile contradicts itself.




