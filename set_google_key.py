import argparse

parser = argparse.ArgumentParser()

parser.add_argument("-n", "--nfile", type=str, help="Гугл api ключ")

args = parser.parse_args()

with open('GOOGLE_KEY.txt', mode="w", encoding="utf-8") as file: 
        file.write(args.nfile)
        print('Key has been successfully written')