import os
import re

keywords = [
    'snap',
    'amos',
    'sc',
    'insta',
    ' ig',
    ' gram',
    'insta',
    'fb',
    'facebook',
    'tw',
    'twitter',
    '.com',
    '@',
    'add me'
]

profiles_file = './logs/parsed/profiles.log'
picture_file = './logs/parsed/picture_urls.log'


def add_profiles_to_file(input_filename):
    input_file = './logs/raw_data/' + input_filename
    name = ''
    age = ''
    with open(input_file) as in_file, open(profiles_file, 'a') as out_file, open(profiles_file, 'r') as out_file_read:
        for line in in_file:
            if 'name:' in line:
                # remove everything before data
                name = line.encode().decode('unicode_escape').encode(
                    'ascii', 'ignore').decode()
                name = re.sub(r'.*name:', 'name:', name)
                name = name[8:-2]
            if 'age:' in line:
                # remove everything before data
                age = re.sub(r'.*age:', 'age:', line)
                age = age[7:-2]
            if 'bio:' in line:
                for keyword in keywords:
                    if keyword.casefold() in line.casefold():
                        # remove encoded characters
                        bio = line.encode().decode('unicode_escape').encode(
                            'ascii', 'ignore').decode()
                        bio = bio.replace('\n', ' ')
                        # remove everything before data
                        bio = re.sub(r'.*bio:', 'bio:', bio)
                        bio = bio[7:-2]
                        profile = f'{name}|||{age}|||{bio}\n'
                        # check if user is already in the file
                        add_to_file = True
                        for read_line in out_file_read:
                            if bio.casefold() in read_line.casefold():
                                add_to_file = False
                                break
                        if add_to_file == True:
                            out_file.write(profile)
                        # we found something
                        # reset name and age variables
                        # and break loop
                        name = ''
                        age = ''
                        break


def add_images_to_file(input_filename):
    input_file = './logs/raw_data/' + input_filename
    with open(input_file) as in_file:
        for line in in_file:
            if 'picture:' in line:
                # remove everything before "picture:"
                # this is so we can have timestamp in logs if we want.
                url = re.sub(r'.*picture:', 'picture:', line)
                url = url[9:]
                url = url.replace('\n', '')
                # if url is not blank add to file
                if url != '':
                    # check if url is in file already
                    add_to_file = True
                    with open(picture_file, 'a+') as out_file:
                        for read_line in out_file:
                            read_line = read_line.replace('\n', '')
                            if url == read_line:
                                add_to_file = False
                                break
                        # if url not in file add
                        if add_to_file == True:
                            out_file.write(f'{url}\n')


files = os.listdir('./logs/raw_data')
for filename in files:
    add_profiles_to_file(filename)
    add_images_to_file(filename)
