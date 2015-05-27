# -*- coding: utf-8 -*-
# The software in this module is subject to the license terms in the ZeOmega
# EULA included herewith. (C) 2011-2015 ZeOmega, Inc. All Rights Reserved.

"""
Database backend pagination support.
To support pagination for use by web services code, it's important for the
database backend to support paginated result sets.  Sorting of records needs
to be handled against entire result sets, not just within individual pages.
The same goes for select criteria.
To avoid requiring pagination code in each and every query, this module
provides a generic function for producing a modified query object with a
paginated WHERE clause added.
The idea here is to show how we can wrap the given query around the column(s) on
which we are interested to paginate and generate the paginated query object. The
feature is supported with the dynamic window size selection by the app user.
"""

from sqlalchemy import func, between


def paginate(query, page_num, page_size, order_by_column,
             partition_by_column=None, order_by=None, session=None):
    """
    Modify the `query` object with paginated _row_number and order by clause on
    the specified `column`. The window size is created dynamically based on the
    application user input. This function adds a pagination wrapper around the
    query object on the specified column(s).
    Args:
      query(object): SQLAlchemy query object or Subquery object.
      page_num(int): Page number
      page_size(int): Number of record of per page
      order_by_column(object or list): SQLAlchemy column(s) object(s).
      partition_by_column(object or list): SQLAlchemy column(s) object(s)
                        There is a major assumption that the value in this
                        column should be unique per record (not repeating)
                        in the initial input query.
      order_by(str): Order by clause, 'asc' for ascending or 'desc' for
                       descending. Default is 'asc'.
      session(object): database session connection object.
    Returns:
        An output query object wrapped with paginated where clause based
        on row_number (_row_number), sorted by and partitioned by the respective
        column(s).
    """

    if not hasattr(query, 'session'):
        # subquery object is passed.
        if not session:
            raise AttributeError("query object has no attribute 'session'")
    else:
        # query object is passed.
        session = query.session

    if partition_by_column is not None:
        if order_by:
            partition_by_column = _get_order_by_columns(partition_by_column,
                                                        order_by)

        paginate_column = func.row_number().over(
            partition_by=partition_by_column,
            order_by=order_by_column).label('_row_number')

    else:
        if order_by:
            order_by_column = _get_order_by_columns(order_by_column,
                                                    order_by)

        paginate_column = func.row_number().over(
            order_by=order_by_column).label('_row_number')

    pagination_subquery = _get_paginated_subquery(session,
                                                  query,
                                                  paginate_column)

    start_page = _get_window_top(page_num, page_size)

    end_page = _get_window_bottom(page_num, page_size)

    return _paged_query_object(session,
                               pagination_subquery,
                               start_page,
                               end_page)


def _paged_query_object(session, pagination_subquery, start_page, end_page):
    """
    Generate the paginated query object based on the start and end row number.
    Args:
        session: connection object to database
        paginated_subquery: pagination subquery over which the output
                            query needs to be formed
        start_page(int): starting row number
        end_page(int): ending row number
    Returns:
       Return the paginated query object
    """
    paged_query = session.query(pagination_subquery).filter(between(
        pagination_subquery.c._row_number, start_page, end_page))

    return paged_query


def _get_order_by_columns(column_details, order_by):
    """
    Attach the  order_by clause to the column object.
    Args:
        column_details(column or list): column object(s).
        order_by(str): order_by clause. Default is ascending.
    Returns:
        Column object(s) with order_by clause attached.
    """

    if isinstance(column_details, list):
        return _attach_clause(column_details, order_by)

    else:
        return _query_with_column(column_details, order_by)


def _attach_clause(list_of_columns, order_by):
    """
    Attach the order_by clause to the column and return the list of objects.
    The list containing the objects is used in the order_by clause of row_number
    function.
    Args:
        list_of_columns(list): list containing column names
        order_by(str): order by clause
    Returns:
        List containing the objects formed by attaching the order_by clause
        with the column object.
    """

    attached_column = []
    for column in list_of_columns:
        attached_column.append(_query_with_column(column, order_by))
    return attached_column


def _query_with_column(column, order_by):
    """
    Attach the order_by clause to the column object.
    Raise Exception if column doesnot have the order_by clause attribute.
    """

    try:
        query_column = getattr(column, order_by)()
        return query_column
    except:
        raise AttributeError("Column object has no order_by clause attribute `{0}`"
                             .format(order_by))


def _get_paginated_subquery(session, query, paginate_column):
    """
    Subquery with _row_number column. This query attaches the _row_number
    function to the original query object.
    """

    if hasattr(query, 'session'):
        # query object is passed.
        return query.add_column(paginate_column).subquery()
    else:
        # subquery object is passed.
        return session.query(query, paginate_column).subquery()


def _get_window_top(page_num, page_size):
    """
    Return the start page number
    """

    return (page_num * page_size) - (page_size - 1)


def _get_window_bottom(page_num, page_size):
    """
    Return the end page number
    """

    return page_num * page_size
