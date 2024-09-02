import datetime

def convert_to_words(year: str, month: str, day: str) -> str:
    #print(year)
    #print(month)
    word_month = calc_month_name(year, month)

    hebrew_date_words = f"{day} {word_month} {year}"

    return hebrew_date_words


# Fortunately, the leap year cycle is easily calculated. Leap years occur in years 3, 6, 8, 11, 14, 17 and 19 of
# a 19-year cycle, and the 19-year cycle begins in the year 1, so you can simply divide the year number by 19 and
# examine the remainder. If the remainder is 3, 6, 8, 11, 14, 17 or 0 (the 19th year of the cycle) then the year is a
# leap year. Otherwise, it is not.
def calc_month_name(year, month) -> str:
    """Returns the hebrew month name from the provided year and month."""
    match int(month):
        case 1:
            return "Nisan"
        case 2:
            return "Iyar"
        case 3:
            return "Sivan"
        case 4:
            return "Tammuz"
        case 5:
            return "Av"
        case 6:
            return "Elul"
        case 7:
            return "Tishrei"
        case 8:
            return "Cheshvan"
        case 9:
            return "Kislev"
        case 10:
            return "Tevet"
        case 11:
            return "Shevat"
        case 12:
            if is_leap_year(year):
                return "Adar I"
            else:
                return "Adar"
        case 13:
            return "Adar II"
        case _:
            return ""


def is_leap_year(year: str | int | float) -> bool:
    year = int(year)
    rem = round(year % 19)
    #print(rem)
    if rem == 3 or rem == 6 or rem == 8 or rem == 11 or rem == 14 or rem == 17 or rem == 0:
        return True

    return False
