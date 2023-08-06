from collections import namedtuple


class CypherReference(object):
    """Object to store cypher specific information"""

    PARAM_FINDING_REGEX = (
        # e.g. { param }
        '{ *'
        '([^\p{Sc}\p{Sm}\p{So}\p{Sk}\p{C}\p{Z}\p{P}\p{M}]'
        '[^\p{Sm}\p{So}\p{Sk}\p{C}\p{Z}\p{Pd}\p{Pe}\p{Pf}'
        '\p{Pi}\p{Po}\p{Ps}\p{M}]*)'
        ' *}'
        '|'
        # e.g. $param
        '\$'
        '([^\p{Sc}\p{Sm}\p{So}\p{Sk}\p{C}\p{Z}\p{P}\p{M}]'
        '[^\p{Sm}\p{So}\p{Sk}\p{C}\p{Z}\p{Pd}\p{Pe}\p{Pf}'
        '\p{Pi}\p{Po}\p{Ps}\p{M}]*)'
        '|'
        # e.g. { `silly param` }
        '{ *`'
        '([^\p{Sc}\p{Zl}\p{Zp}}]'
        '[^\p{Zl}\p{Zp}]*)'
        '` *}'
        '|'
        # e.g. $`why would you even name a param like this?`
        '\$`'
        '([^\p{Sc}\p{Zl}\p{Zp}}]'
        '[^\p{Zl}\p{Zp}]*)'
        '`'
        )
    """Regex to pull out params from a query"""
