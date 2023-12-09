import pandas as pd


def run(screen):
    save_file_path = 'save_file.csv'
    try:
        from world1.world1 import run_world1
        df = pd.read_csv(save_file_path)
        level = df['level'].iloc[-1]
        score = df['score'].iloc[-1]
        kills = df['kills'].iloc[-1]
        # Check if skills are empty or NaN, if the auto saved was triggered before a player could level up.
        if pd.isna(df['skills'].iloc[-1]) or df['skills'].iloc[-1] == '':
            skills = []
        else:
            skills = df['skills'].iloc[-1].split(',')  # skills are saved as a comma-separated string

        run_world1(screen, level, score, kills, skills)

    except FileNotFoundError:
        print("Save file not found. Starting new game.")
        import new_game
        new_game.run(screen)
