def percent_of(percent, whole):
    """Calculates the value of a percent of a number
    ie: 5% of 20 is what --> 1
    
    Args:
        percent (float): The percent of a number
        whole (float): The whole of the number
        
    Returns:
        float: The value of a percent
        
    Example:
    >>> percent_of(25, 100)
    25.0
    >>> percent_of(5, 20)
    1.0
    
    """
    percent = float(percent)
    whole = float(whole)
    return (percent * whole) / 100

def percentage(part, whole, resolution=2):
    """Calculates the percentage of a number, given a part and a whole
    ie: 10 is what percent of 25 --> 40%

    Args:
        part (float): The part of a number
        whole (float): The whole of a number
        resolution (int): Number of decimal places (Default is 2)

    Returns:
        float: The percentage of a number

    Example:
    >>> percentage(10, 25)
    40.0
    >>> percentage(5, 19, 3)
    26.316

    """
    if whole == 0:
        raise ZeroDivisionError

    percent = 100 * float(part)/float(whole)
    
    return round(percent, resolution)