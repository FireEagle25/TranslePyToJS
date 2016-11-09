MIN_LENGTH = 0

def get_max(dict_of_couples):

    max_item = ["", MIN_LENGTH]

    for item in dict_of_couples:
        if item:
            if item[1] > max_item[1]:
                max_item = item

    if max_item[1] != MIN_LENGTH:
        return max_item
    return False