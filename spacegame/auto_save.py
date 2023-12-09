import pandas as pd


def auto_save(level, score, kills, skills):
    # Gather the game state from your game object
    game_state = {
        'level': [level],
        'score': [score],
        'kills': [kills],
        'skills': [','.join(skills)]
    }

    # Convert the dictionary to a pandas DataFrame
    df = pd.DataFrame(game_state)

    # Save the DataFrame to a CSV file
    df.to_csv('save_file.csv', index=False)

    print("Game has been auto-saved.")
