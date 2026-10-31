"""
Command line runner for the Music Recommender Simulation.

This file helps you quickly run and test your recommender.

You will implement the functions in recommender.py:
- load_songs
- score_song
- recommend_songs
"""

from recommender import load_songs, recommend_songs


WIDTH = 72


def print_recommendations(recommendations) -> None:
    """Print each (song, score, explanation) as a ranked card with one reason per line."""
    print()
    print("=" * WIDTH)
    print(f" TOP {len(recommendations)} RECOMMENDATIONS")
    print("=" * WIDTH)

    for rank, (song, score, explanation) in enumerate(recommendations, start=1):
        heading = f"#{rank}  {song['title']}"
        print(f"\n{heading:<{WIDTH - 14}}Score: {score:.2f}")
        print("-" * WIDTH)
        for reason in explanation.split("; "):
            print(f"  - {reason}")

    print("\n" + "=" * WIDTH)


def main() -> None:
    songs = load_songs("C:/Codepath/.venv/ai110-module3show-musicrecommendersimulation-starter/data/songs.csv") 

    # Starter example profile
    user_prefs = {"favorite_genre": "pop", "favorite_mood": "happy", "target_energy": 0.8}

    # user_prefs = {
    #     "favorite_genre": "lofi",
    #     "favorite_mood": "chill",
    #     "target_energy": 0.40,
    #     "pref_tempo": 80,
    #     "target_danceable": 0.60,
    #     "target_acoustic": 0.80,
    # }

    recommendations = recommend_songs(user_prefs, songs, k=5)

    print_recommendations(recommendations)


if __name__ == "__main__":
    main()
