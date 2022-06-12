import argparse
from passlib.hash import md5_crypt

parser = argparse.ArgumentParser()
parser.add_argument('--wordlist', help="the wordlist of passwords to use")
parser.add_argument('--shadow', help="shadow file to attempt to crack")
args = parser.parse_args()

wordlist_path = args.wordlist
shadow_path = args.shadow


def get_wordlist():
    print('Hashing wordlist')

    with open(wordlist_path, encoding="utf8") as wordlist_file:
        wordlist = wordlist_file.readlines()

    print(f'There are {len(wordlist)} entries, this may take a few minutes')

    hash = list()
    for word in wordlist:
        wordpair = {
        "encrypted" : md5_crypt.hash(word),
        "decrpyted" : word
        }
        hash.append(wordpair)

    print('Wordlist successfully hashed')
    return hash


def get_shadow_file():
    print("Getting shadow file")

    with open(shadow_path, encoding="utf8") as shadow_file:
        data = shadow_file.readlines()

    users = list()

    for user in data:
        user_string = user.split(':')
        username = user_string[0].strip()
        password = user_string[1].strip()
        user_dict = {'username' : username,
                     'password' : password}

        users.append(user_dict)
    print(f'Found {len(user_dict)} users')
    return users


def compare_hash(users, hashed_wordlist):
    print('Comparing users')
    cracked_passwords = list()
    for user in users:
        print(f'User {user["username"]}')
        print(hashed_wordlist)
        if user["password"] in hashed_wordlist:
            print(f'Password cracked as {user["password"]}')
            successful_result = {
                "username" : user["username"],
                "encrypted_pass" : user["password"],
            }
            cracked_passwords.append(successful_result)
        else:
            print(f'No crack for "{user["password"]}"')


if __name__ == '__main__':
    wordlist = get_wordlist()
    users = get_shadow_file()
    compare_hash(users, wordlist)
