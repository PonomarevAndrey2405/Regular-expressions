import csv
import re

pattern1 = r'(\+7|8)+[\s(]*(\d{3,3})[\s)-]*(\d{3})[\s-]*(\d{2})[\s-]*(\d{2})'
pattern2 = r'(\+7|8)+[\s(]*(\d{3,3})[\s)-]*(\d{3})[\s-]*(\d{2})[\s-]*(\d{2})[\s]*[(доб.\s]*(\d+)[)]*'


with open("phonebook_raw.csv", encoding='utf-8') as f:
    rows = csv.reader(f, delimiter=",")
    contacts_list = list(rows)


def name_correction(rows):
    result = [' '.join(worker[0:3]).split(' ')[0:3] + worker[3:7] for worker in rows]

    return result


def remove_duplicates(correct_listname):
    no_duplicates = []
    for checked in correct_listname:
        for worker in correct_listname:
            if checked[0:2] == worker[0:2]:
                list_worker = checked
                checked = list_worker[0:2]
                for i in range(2, 7):
                    if list_worker[i] == '':
                        checked.append(worker[i])
                    else:
                        checked.append(list_worker[i])
        if checked not in no_duplicates:
                no_duplicates.append(checked)

    return no_duplicates


def modified_phone_numbers(rows, pattern1, new):
    phonebook = []
    pattern = re.compile(pattern1)
    phonebook = [[pattern.sub(new, string) for string in strings] for strings in rows]

    return phonebook


correct_listname = name_correction(contacts_list)
new_list = remove_duplicates(correct_listname)
correct_list = modified_phone_numbers(new_list, pattern1, r'+7(\2)\3-\4-\5')
corrected = modified_phone_numbers(correct_list, pattern2, r'+7(\2)\3-\4-\5 доб.\6')


with open("phonebook.csv", "w", encoding='utf-8') as f:
  datawriter = csv.writer(f, delimiter=',')
  datawriter.writerows(corrected)