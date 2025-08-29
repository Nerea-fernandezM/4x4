import random

def read_used()->dict:
    result:dict = {"D":[],"O":[]}
    file = open('used.csv', 'r', encoding="utf-8")
    for line in file:
        fields = line.split(":")
        words = fields[2].split(",")
        title = str(fields[1])
        result[fields[0]].append({title:words})
    file.close()
    return result

def read_words(used:dict)->dict:
    result:dict = {"D":[],"O":[]}
    file = open('connections.csv', 'r', encoding="utf-8")
    for line in file:
        fields = line.strip().split(":")
        words = fields[2].split(",")
        title = str(fields[1])
        if fields[1] not in used[fields[0]]:
            result[fields[0]].append({title:words})
    file.close()
    return result

def check(words:dict)->bool:
    keys = words.keys()
    if len(keys) < 1 :
        return False
    else:
        return True
    
def clean_used():
    file = open('used.csv', 'w', encoding="utf-8")
    file.close()

def select_categories(words:dict)->dict:
    result={}
    count={"D":1,"O":3}
    file = open('used.csv', 'a', encoding="utf-8")
    for key in words:
        while count[key] > 0:
            sel= random.choice(words[key])
            clave= list(sel.keys())[0]
            text = sel[clave]
            new_data = {clave:text}
            result.update(new_data)
            string = ""
            for word in text:
                string += f"{word},"
            string.strip(",")
            file.write(f"{key}:{clave}:{string}\n")
            count[key] -= 1
    file.close()
    return result

def select_words(words:dict)->dict:
    result = {}
    for key in words:
        sel = []
        for i in range(4):
            word = random.choice(words[key])
            words[key].remove(word)
            sel.append(word)
        choice = {key:sel}
        result.update(choice)
    return result

def generate()->dict:
    used = read_used()
    words = read_words(used)
    val = check(words)
    if val == False:
        clean_used()
        used = read_used()
        words = read_words(used)
    categories = select_categories(words)
    return select_words(categories)

def write(words:dict):
    file = open('final.csv', 'w', encoding="utf-8")
    count = 3
    for key in words:
        text = words[key]
        list = ""
        for word in text:
            list += f"{word},"
        list.strip(",")
        file.write(f"{key}:{list[:-1]}")
        if count > 0: 
            file.write(f"\n")
            count -= 1
    file.close()

def main():
    write(generate())

if __name__ == "__main__":
    main()

