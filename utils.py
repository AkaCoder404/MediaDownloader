import os

def get_output_number(dst):
    """Gives the last output folder number

    Returns:
        int: Last output folder number
    """
    data = os.listdir(dst)
    print(data)
    if not data == []:
        last_record = sorted(data)[-1]
        print(last_record)
        hiphen_index = last_record.rfind("-")
        # print(hiphen_index)
        # print(int(last_record[hiphen_index + 1:]))
        return int(last_record[hiphen_index + 1:])
    return 0


def create_dir(dir):
    """Creates a directory if not already exists

    Args:
        dir (String): path of directory
    """
    try:
        if not os.path.exists(dir):
            os.makedirs(dir)
    except OSError:
        print('Error: Cannot create directory named \"' + dir + '\"')
