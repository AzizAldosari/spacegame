
def run(screen):
    try:
        from world1.world1 import run_world1
        with open('manual_save_file.txt', 'r') as save_file:
            game_state = {}
            for line in save_file:
                key, value = line.strip().split(':', 1)
                game_state[key.strip()] = value.strip()
        level = int(game_state.get('level', 1))
        score = int(game_state.get('score', 0))
        kills = int(game_state.get('kills', 0))
        skills = game_state.get('skills', '').split(',')

        run_world1(screen, level, score, kills, skills)
    except FileNotFoundError:
        print("Save file not found. Starting new game.")
        import new_game
        new_game.run(screen)
