def convert_date(date_str):
    """
    Convert a date_str in the format 'DD.MM.YYYY' into mysql
    format 'YYYY-MM-DD'.
    """
    date_li = date_str.split('.')
    return '-'.join(reversed(date_li))