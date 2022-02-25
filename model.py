"""

    Helper functions to be used within our API.
    Author: Anda Mchako.
    Note:
    ---------------------------------------------------------------------
    Please follow the instructions provided within the README.md file
    located within this directory for guidance on how to use this script
    correctly.

    ----------------------------------------------------------------------
    Description: This file contains several functions used to abstract aspects within the API.
    This includes scraping data from Rentoza site, data preprocessing, and data storage.

"""
from random import randint, choices
from datetime import datetime, timedelta
import pandas as pd  # pylint: disable=import-error
import requests  # pylint: disable=import-error
import pandas as pd
import requests
from bs4 import BeautifulSoup  # pylint: disable=import-error


def get_products(url):
    """

    Args:
        url:

    Returns:

    """
    products = []

    # Loop to go over all pages
    for page in range(1, 5, 1):

        page = url + '?page=' + str(page)
        source = requests.get(page)
        soup = BeautifulSoup(source.content, 'html.parser')
        my_table = soup.find_all(
            class_=['ProductItem__Title Heading', 'ProductItem__Price Price Text--subdued',
                    'ProductItem__Vendor Heading'])

        # data=[tag.get_text() for tag in my_table]
        for tag in my_table:
            products.append(tag.get_text())
    return products


def customer_id():
    """

    Returns:

    """

    # generate a list of len 9 with random integers ranging from 0 to 10
    random_ints = [randint(0, 15) for _ in range(0, 10)]

    # Convert each integer to a string
    string_ints = [str(num) for num in random_ints]

    # Combine each string with a comma
    str_of_ints = int("".join(string_ints))

    chars = "0123456789ACEFHJKLMNPRTUVWXY"
    length = len(chars)

    result = ""
    while str_of_ints > 0:
        pos = str_of_ints % length
        str_of_ints = str_of_ints // length
        result = chars[pos] + result
    return result


def rental_date(products):
    """

    Args:
        products:

    Returns:

    """

    # initializing dates ranges
    start_date, end_date = datetime(2021, 12, 1), datetime(2022, 1, 30)

    res_dates = []

    # loop to get each date till end date
    while start_date != end_date:
        start_date += timedelta(days=1)
        res_dates.append(start_date.strptime(str(start_date), '%Y-%m-%d %X').strftime('%Y-%m-%d'))

    # random K dates from pack
    rental_dates = choices(res_dates, k=len(products))
    #rental_dates = [datetime.strptime(date, "%Y-%m-%d").date() for date in rental_dates]
    return rental_dates


def account_status(products):
    """

    Args:
        products:

    Returns:

    """
    # Create an empty list
    row_list = []

    # Iterate over each row
    for _, rows in products.iterrows():
        # Create list for the current row
        my_list = [rows.December, rows.January, rows.February]

        # append the list to the final list
        row_list.append(my_list)

    labels = []
    for row in row_list:
        if row.count(0) >= 2:
            labels.append('Flag')
        else:
            labels.append('Safe')

    # Print the list
    return labels


def process_data(data):
    """

    Args:
        data:

    Returns:

    """
    # transform into products

    products = pd.DataFrame({'Brand': data[0::3],
                             'Item': [item.strip('\n') for item in data if item.startswith('\n')],
                             'Price': [int(item.strip('From R ').replace(',', '')) for item in data if
                                       item.startswith('From')]})

    products['CustomerID'] = [customer_id() for _ in range(1, len(products) + 1)]
    products['CustomerMail'] = '****@gmail.com'
    products['RentalDate'] = rental_date(products)

    products['RentalDate'] = [datetime.strptime(date, "%Y-%m-%d").date() for date in products['RentalDate']]
    products['December'] = choices(range(0, 2), k=len(products))
    products['January'] = choices(range(0, 2), k=len(products))
    products['February'] = choices(range(0, 2), k=len(products))
    products['SubStatus'] = account_status(products)

    return products
