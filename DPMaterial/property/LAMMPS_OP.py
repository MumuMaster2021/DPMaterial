import matplotlib.pyplot as plt
import json
from typing import List
import subprocess, os, shutil, glob
from pathlib import Path
from typing import List
import numpy as np
from dflow.python import (
    PythonOPTemplate,
    OP,
    OPIO,
    OPIOSign,
    Artifact,
    Slices)

class den_Cal(OP):
    def __init__(self):
        pass

    @classmethod
    def get_input_sign(cls):
        return OPIOSign({
            "input": Artifact(Path)
        })

    @classmethod
    def get_output_sign(cls):
        return OPIOSign({
            "output": Artifact(Path)
        })

    @OP.exec_sign_check
    def execute(self, op_in: OPIO) -> OPIO:
        cwd = os.getcwd()
        os.chdir(op_in["input"])
        os.system("lmp -i in.lmp")
        os.chdir(op_in["input"])
        # os.system("pwd && ls")
        os.system("pip3 install matplotlib -i https://pypi.tuna.tsinghua.edu.cn/simple")
        import matplotlib.pyplot as plt
        x = []
        y = []
        k = 0
        m = 0
        fp = open("log.lammps")
        for i in fp:
            if "Step          Time           Temp          KinEng         TotEng         Press          Volume        Density" in i:
                k = 1
                continue
            if k == 1:
                if "Loop" not in i:
                    x.append( float(i.split()[0]) )
                    y.append( float(i.split()[7]) )
                else:
                    k = 0
        plt.plot(x, y, 'b-')
        plt.grid()
        plt.ylabel('density (g/cm^3)')
        plt.xlabel('time (ps)')
        plt.savefig("density.png")
        m = int(len(x)*0.1)
        yy = np.array(y)
        den = np.mean(yy[-m:-1])
        print(f"density (g/cm^3): {den}")

        return OPIO({
            "output": Path(op_in["input"])
        })