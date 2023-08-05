import pandas as pd

def split_data(data_df):
    t_key = 'Temperature (K)'
    data_df = data_df
    data_df[t_key] = data_df[t_key].round(1)
    res = {}
    for temp in set(data_df[t_key].tolist()):
        res[temp] = data_df[data_df[t_key] == temp]

    return res

def compute_chi(m, e_mass, y_mass,
                moles, dmc):
    """
    m', "" value
    eicosane mass
    Y complex mass
    moles
    diamagnetic correction
    """
    return ((m / 4) + (e_mass / 282548) * 0.00024306 +
            (y_mass / 698124) * 0.00040896) / moles - dmc


def calculate_chi(data_df, e_mass, y_mass,
                  moles, dmc):

    # calculate the emulated values
    d1 = compute_chi(data_df["m' (emu)"],
                     e_mass,
                     y_mass,
                     moles,
                     dmc)
    d2 = compute_chi(data_df['m" (emu)'],
                     e_mass,
                     y_mass,
                     moles,
                     dmc)
    data_df["chi' (emu)"] = d1
    data_df['chi" (emu)'] = d2
    return data_df
