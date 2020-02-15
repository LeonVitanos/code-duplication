'''
Script clones each version of jQuery in the input csv
file into its own directory.
'''

import csv
import os

releases = []

if __name__ == "__main__":
    with open('jquery_releases.csv', mode='r') as csv_file:
        csv_reader = csv.DictReader(csv_file)
        line_count = 0
        for row in csv_reader:
            if line_count == 0:
                print(f'Column names are {", ".join(row)}')
                line_count += 1
            else:
                releases.append(row)
            line_count += 1


        print(f'Processed {line_count} lines.')

    for release in releases:
        command = f"git clone -b '{release['tag']}' --single-branch --depth 1 https://github.com/jquery/jquery.git {release['tag']}"

        print(f"Executing {command}")
        os.system(command)