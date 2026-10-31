import csv
import heapq
from operator import itemgetter
from typing import List, Dict, Tuple, Optional
from dataclasses import dataclass, asdict

@dataclass
class Song:
    """
    Represents a song and its attributes.
    Required by tests/test_recommender.py
    """
    id: int
    title: str
    artist: str
    genre: str
    mood: str
    energy: float
    tempo_bpm: float
    valence: float
    danceability: float
    acousticness: float

@dataclass
class UserProfile:
    """
    Represents a user's taste preferences.
    Required by tests/test_recommender.py
    """
    # Every field is optional; a field left as None is skipped when scoring.
    favorite_genre: Optional[str] = None
    favorite_mood: Optional[str] = None
    target_energy: Optional[float] = None
    target_acoustic: Optional[float] = None
    # likes_acoustic: bool
    pref_tempo: Optional[int] = None
    target_danceable: Optional[float] = None


class Recommender:
    """
    OOP implementation of the recommendation logic.
    Required by tests/test_recommender.py
    """
    def __init__(self, songs: List[Song]):
        self.songs = songs

    def recommend(self, user: UserProfile, k: int = 5) -> List[Song]:
        """Return the k songs that best match the user's profile, highest score first."""
        prefs = asdict(user)
        scored = [(song, *score_song(prefs, asdict(song))) for song in self.songs]
        top = heapq.nlargest(k, scored, key=itemgetter(1))
        return [song for song, _, _ in top]

    def explain_recommendation(self, user: UserProfile, song: Song) -> str:
        """Explain a song's score as one line, one entry per scored feature."""
        score, reasons = score_song(asdict(user), asdict(song))
        return f"Score {score:.2f}: " + "; ".join(reasons)

def load_songs(csv_path: str) -> List[Dict]:
    """
    Loads songs from a CSV file.
    Required by src/main.py
    """
    print(f"Loading songs from {csv_path}...")
    songs: List[Dict] = []
    with open(csv_path, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for line_no, row in enumerate(reader, start=2):  # line 1 is the header
            try:
                songs.append({
                    "id": int(row["id"]),
                    "title": row["title"].strip(),
                    "artist": row["artist"].strip(),
                    "genre": row["genre"].strip().lower(),
                    "mood": row["mood"].strip().lower(),
                    "energy": float(row["energy"]),
                    "tempo_bpm": int(float(row["tempo_bpm"])),
                    "valence": float(row["valence"]),
                    "danceability": float(row["danceability"]),
                    "acousticness": float(row["acousticness"]),
                })
            except (KeyError, ValueError, AttributeError) as e:
                raise ValueError(f"{csv_path}, line {line_no}: bad row {row!r} ({e})") from e
    print(f"Loaded {len(songs)} songs.")
    return songs

WEIGHTS = {
    "mood": 0.30,
    "genre": 0.15,
    "energy": 0.20,
    "tempo": 0.10,
    "danceability": 0.10,
    "acousticness": 0.15,
}

# Fixed bounds (min/max tempo_bpm in songs.csv) so one song can be scored without the catalog.
TEMPO_MIN, TEMPO_MAX = 60, 168

MOOD_FAMILY = {
    "chill": "A", "relaxed": "A", "focused": "A",
    "sad": "B", "melancholic": "B", "soulful": "B",
    "nostalgic": "C", "romantic": "C", "uplifting": "C",
    "happy": "D", "playful": "D", "energetic": "D", "confident": "D",
    "intense": "E", "angry": "E", "moody": "E",
}
MOOD_FAMILY_SIM = {("A", "B"): 0.2, ("A", "C"): 0.3, ("B", "C"): 0.3,
                   ("C", "D"): 0.3, ("D", "E"): 0.2, ("B", "E"): 0.2}
MOOD_OVERRIDE = {
    ("chill", "relaxed"): 0.8, ("chill", "focused"): 0.6,
    ("chill", "happy"): 0.2, ("chill", "moody"): 0.3,
    ("relaxed", "happy"): 0.3, ("relaxed", "moody"): 0.3,
    ("focused", "happy"): 0.1, ("focused", "intense"): 0.2,
    ("focused", "moody"): 0.3, ("happy", "intense"): 0.3,
    ("intense", "moody"): 0.4, ("happy", "moody"): 0.0,
    ("chill", "intense"): 0.0, ("relaxed", "intense"): 0.0,
    ("sad", "melancholic"): 0.8, ("melancholic", "soulful"): 0.4,
    ("nostalgic", "romantic"): 0.5, ("nostalgic", "uplifting"): 0.4,
    ("romantic", "uplifting"): 0.4, ("happy", "playful"): 0.7,
    ("happy", "energetic"): 0.6, ("playful", "energetic"): 0.6,
    ("happy", "uplifting"): 0.6, ("playful", "uplifting"): 0.5,
    ("intense", "angry"): 0.7, ("angry", "moody"): 0.4,
    ("energetic", "intense"): 0.5, ("confident", "intense"): 0.3,
    ("nostalgic", "melancholic"): 0.4, ("moody", "melancholic"): 0.5,
    ("moody", "sad"): 0.4, ("romantic", "soulful"): 0.4,
    ("relaxed", "romantic"): 0.4, ("angry", "sad"): 0.1,
}

GENRE_FAMILY = {
    "lofi": 1, "jazz": 1, "ambient": 1, "classical": 1,
    "folk": 2, "country": 2, "blues": 2,
    "pop": 3, "indie pop": 3, "r&b": 3,
    "edm": 4, "synthwave": 4,
    "rock": 5, "metal": 5,
    "hip hop": 6, "reggae": 6, "latin": 6,
}
GENRE_OVERRIDE = {
    ("pop", "indie pop"): 0.7, ("pop", "r&b"): 0.5,
    ("lofi", "jazz"): 0.6, ("lofi", "ambient"): 0.6,
    ("classical", "ambient"): 0.6, ("classical", "lofi"): 0.3,
    ("folk", "country"): 0.7, ("country", "blues"): 0.5,
    ("synthwave", "edm"): 0.6, ("rock", "metal"): 0.6,
    ("blues", "jazz"): 0.6, ("blues", "rock"): 0.3,
    ("folk", "indie pop"): 0.4, ("country", "pop"): 0.3,
    ("rock", "pop"): 0.3, ("rock", "indie pop"): 0.3,
    ("rock", "synthwave"): 0.2, ("pop", "edm"): 0.4,
    ("pop", "synthwave"): 0.4, ("indie pop", "synthwave"): 0.4,
    ("synthwave", "lofi"): 0.3, ("indie pop", "lofi"): 0.1,
    ("r&b", "hip hop"): 0.6, ("r&b", "jazz"): 0.3,
    ("hip hop", "pop"): 0.3, ("hip hop", "edm"): 0.2,
    ("latin", "pop"): 0.4, ("reggae", "pop"): 0.2,
}


def _pair(table: Dict, a, b):
    """Look up a value for the pair (a, b) in either order, or None if it isn't listed."""
    return table.get((a, b), table.get((b, a)))


def mood_sim(a: str, b: str) -> float:
    """Partial-credit similarity between two moods (1.0 exact, 0.0 unrelated or unknown)."""
    if a == b:
        return 1.0
    s = _pair(MOOD_OVERRIDE, a, b)
    if s is not None:
        return s
    fa, fb = MOOD_FAMILY.get(a), MOOD_FAMILY.get(b)
    if fa is None or fb is None:
        return 0.0
    if fa == fb:
        return 0.5
    return _pair(MOOD_FAMILY_SIM, fa, fb) or 0.0


def genre_sim(a: str, b: str) -> float:
    """Partial-credit similarity between two genres (1.0 exact, 0.0 unrelated or unknown)."""
    if a == b:
        return 1.0
    s = _pair(GENRE_OVERRIDE, a, b)
    if s is not None:
        return s
    fa, fb = GENRE_FAMILY.get(a), GENRE_FAMILY.get(b)
    return 0.4 if fa is not None and fa == fb else 0.0


def _closeness(song_value: float, target: float) -> float:
    """Return 1.0 when a song's value equals the target, falling toward 0 as they differ."""
    return 1.0 - abs(song_value - target)


def _normalize_tempo(bpm: float) -> float:
    """Scale a tempo in BPM to 0-1 using TEMPO_MIN and TEMPO_MAX, clamping out-of-range values."""
    return min(max((bpm - TEMPO_MIN) / (TEMPO_MAX - TEMPO_MIN), 0.0), 1.0)


def score_song(user_prefs: Dict, song: Dict) -> Tuple[float, List[str]]:
    """
    Scores a single song against user preferences.
    Required by recommend_songs() and src/main.py

    user_prefs keys (all optional; missing or None fields are skipped and the
    remaining weights are rescaled so the score stays between 0 and 1):
      favorite_mood, favorite_genre, target_energy, pref_tempo,
      target_danceable, target_acoustic
    Returns (score, reasons), where each reason shows one feature's contribution.
    """
    # (feature, preference label, song label, similarity)
    terms: List[Tuple[str, str, str, float]] = []

    mood = user_prefs.get("favorite_mood")
    if mood and mood.strip():  # None or a blank string means "no preference"
        mood = mood.strip().lower()
        terms.append(("mood", mood, song["mood"], mood_sim(mood, song["mood"])))

    genre = user_prefs.get("favorite_genre")
    if genre and genre.strip():
        genre = genre.strip().lower()
        terms.append(("genre", genre, song["genre"], genre_sim(genre, song["genre"])))

    energy = user_prefs.get("target_energy")
    if energy is not None:
        terms.append(("energy", f"{energy:.2f}", f"{song['energy']:.2f}",
                      _closeness(song["energy"], energy)))

    tempo = user_prefs.get("pref_tempo")
    if tempo is not None:
        terms.append(("tempo", f"{tempo} bpm", f"{song['tempo_bpm']} bpm",
                      _closeness(_normalize_tempo(song["tempo_bpm"]), _normalize_tempo(tempo))))

    dance = user_prefs.get("target_danceable")
    if dance is not None:
        terms.append(("danceability", f"{dance:.2f}", f"{song['danceability']:.2f}",
                      _closeness(song["danceability"], dance)))

    acoustic = user_prefs.get("target_acoustic")
    if acoustic is not None:
        terms.append(("acousticness", f"{acoustic:.2f}", f"{song['acousticness']:.2f}",
                      _closeness(song["acousticness"], acoustic)))

    total_weight = sum(WEIGHTS[name] for name, _, _, _ in terms)
    if total_weight == 0:
        return 0.0, ["no preferences given"]

    score = 0.0
    reasons: List[str] = []
    for name, wanted, actual, sim in terms:
        points = WEIGHTS[name] * sim / total_weight
        score += points
        reasons.append(f"{name}: wanted {wanted}, got {actual} (similarity {sim:.2f}, +{points:.2f})")
    return score, reasons

def recommend_songs(user_prefs: Dict, songs: List[Dict], k: int = 5) -> List[Tuple[Dict, float, str]]:
    """
    Functional implementation of the recommendation logic.
    Required by src/main.py
    """
    # Previous loop-based version, kept for reference:
    # scored = []
    # for song in songs:
    #     score, reasons = score_song(user_prefs, song)
    #     scored.append((song, score, "; ".join(reasons)))
    # # Highest score first; ties fall back to song id so the order is stable.
    # scored.sort(key=lambda item: (-item[1], item[0]["id"]))
    # return scored[:k]

    scored = [(song, *score_song(user_prefs, song)) for song in songs]  # (song, score, reasons)
    # nlargest keeps equal scores in input order, so ties resolve by song order.
    top = heapq.nlargest(k, scored, key=itemgetter(1))
    return [(song, score, "; ".join(reasons)) for song, score, reasons in top]
