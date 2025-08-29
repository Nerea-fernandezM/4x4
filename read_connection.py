def read()->dict:
    result:dict = {}
    file = open('final.csv', 'r', encoding="utf-8")
    for line in file:
        fields = line.split(":")
        words = fields[1].split(",")
        title = str(fields[0])
        choice = {title:words}
        result.update(choice)
    file.close()
    return result

def main():
    choices = read()
    print(choices)

if __name__ == "__main__":
    main()
