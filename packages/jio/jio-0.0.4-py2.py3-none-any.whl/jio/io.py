import glob
import json
import os


def jio_log(text, *args, **kwargs):
    '''logging wrapper'''
    print('[jio] '.join(text.splitlines(True)), *args, **kwargs)


def fexist(path):
    '''checks if the file exists'''
    return os.path.isfile(path)


def force_utf8(raw):
    '''Will force the string to convert to valid utf8'''
    string = raw
    try:
        string = string.decode('utf-8', 'ignore')
    except Exception:
        pass
    return string


def get_file(filename, limit=1000000):
    '''
    Attempts to read the first 'limit' characters of a file and returns it.
    If unreadable, return error reading file
    If limit is negative, will read without limit.
    '''
    if fexist(filename):
        try:
            with open(filename, 'rb') as file_to_read:
                if limit < 0:
                    return force_utf8(file_to_read.read())
                return force_utf8(file_to_read.read(limit))
        except Exception:
            jio_log('get_file failed: couldn\'t read')
            return 'ER303: trouble reading the file'
    else:
        jio_log('get_file failed: file does not exist')
        return 'ERR304: file doesn\'t exist'


def convert_line_ends(text):
    '''Converts newlines in text from \r\n to \n'''
    return text.replace('\r\n', '\n') if text else ''


def put_file(filename, content):
    '''Puts the given text content into the specified filename'''
    if not content:
        content = ''
    content = convert_line_ends(content)
    try:
        with open(filename, 'w') as file_to_write:
            file_to_write.write(content)
        return True
    except Exception as exception_text:
        jio_log('put_file failed: {}'.format(exception_text))
        return False


def uglob(directory, unix_glob):
    '''performs a file glob in the given directory, and returns just the filenames'''
    raw_glob = glob.glob('{}{}'.format(directory, unix_glob))
    file_names = [x.split('/')[-1] for x in raw_glob]
    return file_names


def json_dump(filename, obj, raw=False):
    '''tries to dump a given obj to json in the given filename'''
    try:
        if raw:
            put_file(filename, json.dumps(obj))
        else:
            put_file(filename, json.dumps(obj, sort_keys=True, indent=4))
        return True
    except Exception:
        return False


def json_load(filename):
    '''loads json from a file into a python dict object'''
    if fexist(filename):
        return json.loads(get_file(filename))
    return None


def to_case_insensitive_regex(filename):
    '''Converts a string into a case insensitive regex by bruteforcing each char'''
    regex = ''
    for char in filename:
        if char.isalpha():
            new_char = char.lower()
            regex += '[{}{}]'.format(new_char, new_char.upper())
        else:
            regex += '[{}]'.format(char)
    return regex


def strip_extension(filename):
    '''Strips the extension off of a filename'''
    try:
        split_filename = filename.split('.')
        return '.'.join(split_filename[:-1])
    except Exception:
        return ''


def mkdir(name):
    '''makes a directory if it doesn't exist'''
    try:
        os.mkdir(name)
    except Exception:
        pass
