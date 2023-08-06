from collections import deque

def flatten_dict(d):
    ''' Completely flatten a dict using an iterative algorithm '''

    new_d = {}
    nested_d = deque()
    nested_d.append(d)
    
    while nested_d:
        for k, v in nested_d.pop().items():
            if isinstance(v, dict):
                nested_d.append(
                    {'{}.{}'.format(k, k2): v2 for k2, v2 in
                v.items() }
                )
            else:
                new_d[k] = v
        
    return new_d