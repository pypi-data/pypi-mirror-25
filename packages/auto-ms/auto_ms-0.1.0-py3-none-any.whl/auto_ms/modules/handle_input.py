import os
from collections import defaultdict

def ika_in(args):
    """
    Process the argparse args object containing ika arguments, 
    checking types and generating values if needed
    """
    def getattr_float(obj, key):
        return float(getattr(obj, key))

    holder = defaultdict(str)
    params = ["e_mass", "y_mass", "diamagnetic_correction"]
    for i in params:
        try:
            holder[i] = getattr_float(args, i)
        except ValueError:
            holder[i] = ''
    # Certain params (moles, mol_mass, mass) can be derived from others
    if args.moles:
        try:
            holder['moles'] = float(args.moles)
        except ValueError:
            holder['moles'] = ''
        
    else:
        for key in ['mol_mass', 'mass']:
            try:

                holder[key] = getattr_float(args, key)
            except ValueError as e:
                print(e)
                holder[key] = ''
        if args.mol_mass and args.mass:
            holder['moles'] = holder['mass'] / holder['mol_mass']
    return  holder
