# coding=utf-8
import os
import subprocess

out = subprocess.getstatusoutput("pytest -s {0} --tavern-merge-ext-function-values".format(r"C:\Users\lq\Desktop\api\api\cloud-v2.0\case\a_zone"))
print(out[1])

