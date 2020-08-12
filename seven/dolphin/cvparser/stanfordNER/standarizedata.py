from dateutil.parser import parse

def capitalizeinput(inputparameter):
    '''
    This will take the raw input text and
    tokenize the string and capitalize all
    the token and returns the formatted
    capitalized text.
    :param inputparameter :type str
    :return: string(text will all the tokens capitalized)
    '''
    formatted_output = inputparameter.title()
    return formatted_output


def comparedates(datelist):
    '''
    this function takes the list of the date
    parse them and compares them and provide
    larger date and smaller date
    :param datelist:type list of str
    :return: sorted dates
    '''
    try:
        date1 = parse(datelist[0][0])
        date2 = parse(datelist[1][0])
        if date2> date1:
            return datelist[1][0],datelist[0][0]
        else:
            return datelist[0][0],datelist[1][0]
    except:
        return datelist[0][0],datelist[1][0]
