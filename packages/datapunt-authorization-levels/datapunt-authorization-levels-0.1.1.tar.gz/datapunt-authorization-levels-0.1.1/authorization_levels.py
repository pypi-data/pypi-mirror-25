"""
    authorization_levels
    ~~~~~~~~~~~~~~~~~~~~

    This module defaines all authorization levels we know.

    Code of conduct
    ---------------

    Other Datapunt services depend on these levels. When editing this file,
    keep in mind that:

    - the LEVEL_* prefix has significance and is used to fetch all supported
      levels from this module (i.e.
      `{level for level in dir(authorization_levels) if level[:6] == 'LEVEL'}`)
    - LEVEL_DEFAULT has special significance, and its value nor its name can be
      changed without breaking downstream projects.

"""

LEVEL_DEFAULT = 0b0
""" All users have at least this level
"""

LEVEL_EMPLOYEE = 0b1
LEVEL_EMPLOYEE_PLUS = 0b11


# Scopes

# BRP Basis Register Personen
SCOPE_BRP_R = 'BRP/R'

# TLLS Tellus leesrechten
SCOPE_TLLS_R = 'TLLS/R'

# Kadaster
# Bevragen niet-natuurlijke Kadastrale Subjecten. Is included in RSN
SCOPE_BRK_RS = 'BRK/RS'
#  Bevragen alle Kadastrale Subjecten. Includes RS
SCOPE_BRK_RSN = 'BRK/RSN'
# Zakelijke rechten
SCOPE_BRK_RZR = 'BRK/RZR'
# Aantekeningen
SCOPE_BRK_RAT = 'BRK/RAT'
# Lezen alle WKPB details van Kadastrale Objecten
SCOPE_BRK_RW = 'BRK/RW'

# WKPB
# name: Wet Kenbaarheid Publiekrechtelijke Beperkingen
# described_by: 'https://www.amsterdam.nl/stelselpedia/wkpb-index/'
SCOPE_WKPB_RBDU = 'WKPB/RBDU'

# Handelsregister
SCOPE_HR_R = 'HR/R'

# Monumenten
# Lezen beschrijvingen van Complexen
SCOPE_MON_RBC = 'MON/RBC'
SCOPE_MON_RDM = 'MON/RBM'

SCOPES_EMPLOYEE = frozenset({SCOPE_HR_R, SCOPE_MON_RBC, SCOPE_MON_RDM, SCOPE_BRK_RS, SCOPE_BRK_RZR,
                             SCOPE_TLLS_R, SCOPE_WKPB_RBDU})
SCOPES_EMPLOYEE_PLUS = frozenset({SCOPE_BRP_R, SCOPE_BRK_RSN}.union(SCOPES_EMPLOYEE))


def is_authorized(granted, needed, level=LEVEL_DEFAULT):
    """ Authorization function, checks whether the user's `granted` authz level
    is sufficient for that `needed`.

    If sets of scopes are give checks whether the user's `granted` scopes
    are sufficient for the `needed` scopes.

    Both are sets of scopes. If the needed - granted is empty it is sufficient

    level is added for backwards compatibility. If a level is given we can still check if
    this level authorizez for the needed scopes.

    :return bool: True is sufficient, False otherwise
    """
    if isinstance(granted, int) and isinstance(needed, int):
        return needed & granted == needed
    else:
        result = needed.issubset(granted)

        # For backwards compatibility with the levels the following lines have been added
        if not result:
            if level == LEVEL_EMPLOYEE:
                result = needed.issubset(SCOPES_EMPLOYEE)
            elif level == LEVEL_EMPLOYEE_PLUS:
                result = needed.issubset(SCOPES_EMPLOYEE_PLUS)
        return result
