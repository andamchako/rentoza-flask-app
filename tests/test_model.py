"""
    testing the helper functions to be used within our API.
    Author: Anda Mchako.
    Note:
    ---------------------------------------------------------------------
    Plase follow the instructions provided within the README.md file
    located within this directory for guidance on how to use this script
    correctly.
    Importantly, you will need to modify this file by adding
    your own data preprocessing steps within the `_preprocess_data()`
    function.
    ----------------------------------------------------------------------
    Description:
"""

import pandas as pd
from model import get_products, customer_id, rental_date

# customer_id, rental_date, account_status, process_data


def test_get_products():
    """

    Returns:

    """
    url = "https://rentoza.co.za/collections/electronics"
    assert isinstance(get_products(url), list) is True
    assert len(get_products(url)) == 192

    url = "https://rentoza.co.za/collections/appliances"
    assert isinstance(get_products(url), list) is True
    assert len(get_products(url)) == 99


def test_customer_id():
    """

    Returns:

    """
    assert isinstance(customer_id(), str) is True


def test_rental_date():
    """

    Returns:

    """
    products = pd.read_csv('../utils/data/clean_data.csv')
    print(rental_date(products))


def test_account_status():
    """

    Returns:

    """
    assert False


def test_process_data():
    """

    Returns:

    """
    assert False
