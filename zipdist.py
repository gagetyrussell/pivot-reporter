# -*- coding: utf-8 -*-
"""
Created on Sun Apr  5 22:14:53 2020

@author: GRussell
"""

import os
import zipfile

def zipdir(path, ziph):
    # ziph is zipfile handle
    for root, dirs, files in os.walk(path):
        for file in files:
            ziph.write(os.path.join(root, file))

if __name__ == '__main__':
    zipf = zipfile.ZipFile('GTR-Spreadsheet-Viewer.zip', 'w', zipfile.ZIP_DEFLATED)
    zipdir('./dist', zipf)
    zipf.close()