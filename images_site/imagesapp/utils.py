def get_thumbnail_sizes(str):
    heights = str.split(';')
    heights = [int(x) for x in heights]
    return heights