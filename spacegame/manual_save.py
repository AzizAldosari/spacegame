# manual_save.py
def manual_save(level, score, kills, skills):
    save_data = f"level:{level}\nscore:{score}\nkills:{kills}\nskills:{skills}"
    with open('manual_save_file.txt', 'w') as save_file:
        save_file.write(save_data)

