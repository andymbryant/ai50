from copy import deepcopy

def convert_month(month):
    months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'June', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
    return months.index(month)

def convert_types(evidence):
    int_cols_indices = [0,2,4,10,11,12,13,14,15,16]
    evidence_copy = deepcopy(evidence)
    for i, e in enumerate(evidence):
        evidence_copy[i] = [int(val) if j in int_cols_indices else val for j, val in enumerate(e)]
    return evidence_copy
