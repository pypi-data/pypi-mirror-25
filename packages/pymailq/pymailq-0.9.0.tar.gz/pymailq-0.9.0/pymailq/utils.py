# coding: utf-8
#
#    Postfix queue control python tool (pymailq)
#
#    Copyright (C) 2014 Denis Pompilio (jawa) <denis.pompilio@gmail.com>
#
#    This file is part of pymailq
#
#    This program is free software; you can redistribute it and/or
#    modify it under the terms of the GNU General Public License
#    as published by the Free Software Foundation; either version 2
#    of the License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program; if not, see <http://www.gnu.org/licenses/>.

import re
from functools import wraps
from collections import Counter


FORMAT_PARSER = re.compile(r'\{[^{}]+\}')
FORMATS = {
    'brief': "{date} {qid} [{status}] {sender} ({size}B)",
    'long': ("{date} {qid} [{status}] {sender} ({size}B)\n"
             "  Rcpt: {recipients}\n"
             "   Err: {errors}")
}


def viewer(function):
    """Result viewer decorator

    :param func function: Function to decorate
    """
    def wrapper(*args, **kwargs):
        args = list(args)  # conversion need for arguments cleaning
        limit = None
        overhead = 0
        try:
            if "limit" in args:
                limit_idx = args.index('limit')
                args.pop(limit_idx)  # pop option, next arg is value
                limit = int(args.pop(limit_idx))
        except (IndexError, TypeError, ValueError):
            raise SyntaxError("limit modifier needs a valid number")

        output = "brief"
        for known in FORMATS:
            if known in args:
                output = args.pop(args.index(known))
                break
        out_format = FORMATS[output]

        elements = function(*args, **kwargs)

        total_elements = len(elements)
        if not total_elements:
            return ["No element to display"]

        # Check for headers and increase limit accordingly
        headers = 0
        if total_elements > 1 and "========" in str(elements[1]):
            headers = 2

        if limit is not None:
            if total_elements > (limit + headers):
                overhead = total_elements - (limit + headers)
            else:
                limit = total_elements
        else:
            limit = total_elements

        out_format_attrs = FORMAT_PARSER.findall(out_format)
        formatted = []
        for element in elements[:limit + headers]:
            # if attr qid exists, assume this is a mail
            if hasattr(element, "qid"):
                attrs = {}
                for att in out_format_attrs:
                    if att == "{recipients}":
                        rcpts = getattr(element, att[1:-1], ["-"])
                        attrs[att[1:-1]] = ", ".join(rcpts)
                    elif att == "{errors}":
                        errors = getattr(element, att[1:-1], ["-"])
                        attrs[att[1:-1]] = "\n".join(errors)
                    else:
                        attrs[att[1:-1]] = getattr(element, att[1:-1], "-")
                formatted.append(out_format.format(**attrs))
            else:
                formatted.append(element)

        if overhead > 0:
            msg = "...Preview of first %d (%d more)..." % (limit, overhead)
            formatted.append(msg)

        return formatted
    wrapper.__doc__ = function.__doc__
    return wrapper


def sorter(function):
    """Result sorter decorator.

    This decorator inspect decorated function arguments and search for
    known keyword to sort decorated function result.
    """
    @wraps(function)
    def wrapper(*args, **kwargs):
        args = list(args)  # conversion need for arguments cleaning
        sortkey = "date"  # default sort by date
        reverse = True  # default sorting is desc
        if "sortby" in args:
            sortby_idx = args.index('sortby')
            args.pop(sortby_idx)  # pop option, next arg is value

            try:
                sortkey = args.pop(sortby_idx)
            except IndexError:
                raise SyntaxError("sortby requires a field")

            # third param may be asc or desc, ignore unknown values
            try:
                if "asc" == args[sortby_idx]:
                    args.pop(sortby_idx)
                    reverse = False
                elif "desc" == args[sortby_idx]:
                    args.pop(sortby_idx)
            except IndexError:
                pass

        elements = function(*args, **kwargs)

        try:
            sorted_elements = sorted(elements,
                                     key=lambda x: getattr(x, sortkey),
                                     reverse=reverse)
        except AttributeError:
            msg = "elements cannot be sorted by %s" % sortkey
            raise SyntaxError(msg)

        return sorted_elements
    wrapper.__doc__ = function.__doc__
    return wrapper


def ranker(function):
    """Result ranker decorator
    """
    @wraps(function)
    def wrapper(*args, **kwargs):
        args = list(args)  # conversion need for arguments cleaning
        rankkey = None
        if "rankby" in args:
            rankby_idx = args.index('rankby')
            args.pop(rankby_idx)  # pop option, next arg is value

            try:
                rankkey = args.pop(rankby_idx)
            except IndexError:
                raise SyntaxError("rankby requires a field")

        elements = function(*args, **kwargs)

        if rankkey is not None:
            try:
                rank = Counter()
                for element in elements:
                    rank[getattr(element, rankkey)] += 1

                # XXX: headers are taken in elements display limit :(
                ranked_elements = ['%-40s  count' % rankkey, '='*48]
                for entry in rank.most_common():
                    key, value = entry
                    ranked_elements.append('%-40s  %s' % (key, value))
                return ranked_elements

            except AttributeError:
                msg = "elements cannot be ranked by %s" % rankkey
                raise SyntaxError(msg)

        return elements
    wrapper.__doc__ = function.__doc__
    return wrapper
