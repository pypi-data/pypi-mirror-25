"""
GUI for collecting inputs
NEEDS REFACTOR BADLY
"""

import tkinter as tk
from tkinter import simpledialog

class InputDialog:
    def __init__(self, fields, disabled=set(), header=None, prefill=None,
                 geometry=None):
        self.geometry = geometry
        self.res = {}
        self.root = tk.Tk()
        self.root.wm_protocol('WM_DELETE_WINDOW', self.quit)
        self.root.title = "Input form"
        self.inputs = {}
        self.fields = fields
        
        # Generate the header
        if header:
            print(header)
            row = tk.Frame(self.root)
            text = tk.Label(row, text=header, fg='red',
                            font='Arial 12 bold')
            row.pack(side=tk.TOP, fill=tk.X, padx=5, pady=5)
            text.pack(side=tk.TOP)

        # If previous values were saved to prefill
        # the fields
        if not prefill:
            prefill = ["" for i in fields]

        # Generate the entry fields and their labels
        for target, prefill in zip(fields, prefill):
            row = tk.Frame(self.root)
            lab = tk.Label(row, width=18, text=target, anchor=tk.W)
            if target in disabled:
                ent = tk.Entry(row)
                ent.insert(0, prefill)
                ent.configure(state='disabled')
            else:
                ent = tk.Entry(row)
                ent.insert(0, prefill)
            row.pack(side=tk.TOP, fill=tk.X, padx=5, pady=5)
            lab.pack(side=tk.LEFT)
            ent.pack(side=tk.RIGHT, expand=tk.YES, fill=tk.X)
            self.inputs[target] = ent
        b1 = tk.Button(self.root, text="Submit",
                       command=lambda: self.submit(lambda: self.submit(self.root, self.inputs)) )
        b1.pack(side=tk.LEFT, padx=5, pady=5)
        b2 = tk.Button(self.root, text="Quit",
                       command= self.quit)
        b2.pack(side=tk.LEFT, padx=5, pady=5)
        self.root.withdraw()
        self.root.update()
        # Set the coordinates
        if geometry:
            g = self.root.geometry().split('+')[:1]
            g = '+'.join((g + geometry.split('+')[1:]))
            print(g)

            self.root.geometry(g)
        self.root.deiconify()

    
    def run(self):
        self.root.mainloop()

    def submit(self, inputs):
        print(self.res)
        print(self.inputs.items())
        for key, entry in self.inputs.items():
            text = entry.get()
            self.res[key] = text
        self.geometry = self.root.geometry()
        print(self.geometry)
        self.root.quit()
   
    def quit(self):
        print("TRIGGERED")
        self.res['quit'] = True
        self.root.quit()
        self.root.destroy()


def mass_event(event, root):
    mass = root.inputs['Mass']
    mol_mass = root.inputs['Molecular_mass']
    moles = root.inputs['moles']
    try:

        m_val = float(mass.get())
        mm_val = float(mol_mass.get())
        mol_val = m_val / mm_val
        moles.configure(state='normal')
        moles.delete(0, tk.END)
        moles.insert(0, mol_val)
        moles.configure(state='disabled')
        print(1 )
    except (TypeError, ValueError) as e:
        print("2")
        moles.configure(state='normal')
        moles.delete(0, tk.END)
        moles.insert(0, "<INVALID INPUT>")
        moles.configure(state='disabled')

    print(mass.get())


param_targets = ['Mass', 'Molecular_mass', 'Mass_E', 'moles', 'Diamagnetic_corr', 'Mass_y']


def param_input(header=None, prefill=None, geometry=None):
    targets = param_targets
    a = InputDialog(targets, disabled='moles', header=header, prefill=prefill,
                    geometry=geometry)
    a.inputs["Mass"].bind('<KeyRelease>', lambda e: mass_event(e, a))
    a.inputs["Molecular_mass"].bind('<KeyRelease>', lambda e: mass_event(e, a))
    a.inputs["moles"].insert(0, "TESTING")
    a.run()

    res = a.res
    # a.root.withdraw()
    return (res, a.geometry)


def check_param(param):
    """
    Attempts to check if all parameters are correct
    """
    res = {}
    # print(param)
    if 'quit' in param and param['quit']:
        print("Quitting")
        quit()
    if all(item =='' for key, item in param.items()):
        return -2
    try:
        for key, item in param.items():
            res[key] = float(item)
        return res
    except ValueError:
        return -1


def param_input_loop(prefill = None):
    """
    Displays an input box for the collection of certain parameters
    """
    val = 0
    header = None
    geometry = None
    while True:
        print("prefill: ", prefill)
        res, geometry = param_input(header=header, prefill=prefill,
                                    geometry=geometry)
        # print(geometry)
        val = check_param(res)
        if val == -1:
            header = 'Invalid input'
            prefill = [res[i] for i in param_targets]
        elif val == -2:
            header = 'No params provided'
            prefill = None
        else:
            break
    return res

if __name__ == '__main__':
    param_input_loop()