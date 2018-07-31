import csv
import errno
import shutil
import simplejson as json


def copy_directory(src, dest):
    # Copy a directory
    try:
        shutil.copytree(src, dest)
    except OSError as e:
        if e.errno == errno.ENOTDIR:
            shutil.copy(src, dest)
        else:
            print('Directory not copied. Error: %s' % e)


def dictionnary_to_string(dictionnary):
    # Transform dictionnary to string
    name = ''
    dictionnary_columns, dictionnary_values = dictionnary_to_lists(dictionnary)
    for i in range(len(dictionnary_columns)):
        name += dictionnary_columns[i] + '=' + dictionnary_values[i]
        if i != len(dictionnary_columns) - 1:
            name += '_'
    return name


def dictionnary_to_lists(dictionnary):
    # Put the keys in dictionnary_columns and the values in dictionnary_values
    dictionnary_columns, dictionnary_values = [], []
    for i in dictionnary:
        if type(dictionnary[i]) == dict:
            tmp_columns, tmp_values = dictionnary_to_lists(dictionnary[i])
            dictionnary_columns += tmp_columns
            dictionnary_values += tmp_values
        else:
            dictionnary_columns.append(str(i))
            dictionnary_values.append(str(dictionnary[i]))
    return dictionnary_columns, dictionnary_values


def json_to_dictionnary(json_file_path):
    # Adjust json.loads
    return json.loads(open(json_file_path, 'r').read())


def csv_update(dictionnary, csv_path):
    # Update csv
    dictionnary_columns, dictionnary_values = dictionnary_to_lists(dictionnary)
    csv_columns, csv_values = csv_to_lists(csv_path)
    reoganised_values = []
    for i in range(len(csv_columns)):
        reoganised_values.append('')
    for dictionnary_column in dictionnary_columns:
        if dictionnary_column in csv_columns:
            reoganised_values[csv_columns.index(dictionnary_column)] = \
                dictionnary_values[dictionnary_columns.index(dictionnary_column)]
        else:
            csv_columns.append(dictionnary_column)
            reoganised_values.append(dictionnary_values[dictionnary_columns.index(dictionnary_column)])
    csv_values.append(reoganised_values)
    write_csv(csv_path, csv_columns, csv_values)


def csv_to_lists(csv_path):
    # Transform csv into lists
    csv_columns, csv_values = [], []
    csv_reader = csv.reader(open(csv_path, 'rb'), delimiter=';')
    first_row = True
    for row in csv_reader:
        if first_row:
            first_row = False
            csv_columns = row
        else:
            csv_values.append(row)
    return csv_columns, csv_values


def write_csv(csv_path, csv_columns, csv_values):
    # Fill a csv file
    with open(csv_path, 'wb') as csvfile:
        csv_writer = csv.writer(csvfile, delimiter=';')
        csv_writer.writerow(csv_columns)
        for row in csv_values:
            csv_writer.writerow(row)


def save_json(dictionnary, json_path):
    with open(json_path, 'wb') as json_file:
        json_content = json.dumps(dictionnary)
        json_content.replace(',', ',\n')
        json_file.write(json_content)
