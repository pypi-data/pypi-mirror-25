# -*- coding: utf-8 -*-
import os
import traceback


def get_traceback_str():
    lines = traceback.format_exc().strip().split('\n')
    rl = [lines[-1]]
    lines = lines[1:-1]
    lines.reverse()
    nstr = ''
    for i in range(len(lines)):
        line = lines[i].strip()
        if line.startswith('File "'):
            eles = lines[i].strip().split('"')
            basename = os.path.basename(eles[1])
            lastdir = os.path.basename(os.path.dirname(eles[1]))
            eles[1] = '%s/%s' % (lastdir,basename)
            rl.append('^\t%s %s' % (nstr,'"'.join(eles)))
            nstr = ''
        else:
            nstr += line
    return '\n'.join(rl)


def dict_to_single_depth(data, key=None):
    new_dict = {}
    for k, v in data.iteritems():
        if type(v) is dict:
            if key is not None:
                k = "{}.{}".format(key, k)
            new_dict.update(dict_to_single_depth(v, key=k))
        else:
            if key is None:
                # print "{}: {}".format(k, v)
                new_dict.update({k: v})
            else:
                # print "{}.{}: {}".format(key, k, v)
                if type(v) is list:
                    for idx, val in enumerate(v):
                        if type(val) is dict:
                            new_dict.update(dict_to_single_depth(val, "{}.{}.${}".format(key, k, str(idx))))
                        else:
                            new_dict.update({"{}.{}.${}".format(key, k, str(idx)): val})
                else:
                    new_dict.update({"{}.{}".format(key, k): v})

    return new_dict


def is_empty(text):
    emp_str = lambda s: s or ""
    if emp_str(text) == "":
        return True
    else:
        return False

