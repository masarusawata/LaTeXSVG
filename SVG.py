import subprocess
import os
import hashlib
import glob
import re


path = __file__[:__file__.rfind('\\')]

def modSVG(inputfile, outputfile, ptincrement=1):
    with open(inputfile, 'r') as f:
        lines = f.readlines()
    with open(outputfile, 'w') as g:
        fl = True
        for i, line in enumerate(lines):
            if 'height=' in line and fl:
                tmp = line.split()
                for j, t in enumerate(tmp):
                    if 'height=' in t:
                        tmp2 = re.sub(r'[^\d.]', '', t)
                        tmp2 = float(tmp2) + ptincrement
                        tmp[j] = f"height='{tmp2}pt'"
                        break
                g.write(' '.join(tmp) + '\n')
                fl = False
            else:
                g.write(line)


def clearcache():
    pass


class Equation:
    def __init__(self, eq):
        self.eq = eq
        id_str = eq
        hasher = hashlib.sha256()
        hasher.update(id_str.encode())
        self.filename = hasher.hexdigest()[:16]
        texfilename = self.filename + '.tex'
        texfiles = glob.glob(path + '/cache/*.tex')
        
        if not(any([self.filename + '.tex' in te for te in texfiles])):
            with open(path + '/template.tex', 'r') as f:
                lines = f.readlines()
            with open(path + '/cache/' + texfilename, 'w') as f:
                for line in lines:
                    if 'python_key' in line:
                        f.write(eq + '\n')
                    else:
                        f.write(line)


    
    def export_svg(self, modheight=True, outputfilename='LaTeXSVGEq.svg'):
        svgfiles = glob.glob(path + '/cache/*.svg')
        dvifiles = glob.glob(path + '/cache/*.dvi')
        svgfilename = self.filename + '.svg'
        dvifilename = self.filename + '.dvi'
        if not(any([svgfilename in sv for sv in svgfiles])):
            if not(any([dvifilename in dv for dv in dvifiles])):
                subprocess.call(["latex", f'-output-directory={path}/cache',path + '/cache/' + self.filename + '.tex'])
            subprocess.call(["dvisvgm", path + '/cache/' + self.filename + ".dvi", "-n", "-o", f'{path}/cache/{self.filename}.svg'])
        

        svgoutfiles = list(map(os.path.normpath, glob.glob('./**/*.svg', recursive=True)))
        i = 0
        
        if outputfilename[-4:]!='.svg':
            outputfilename += '.svg'
        tmp = outputfilename
        while any([os.path.normpath(tmp) == so for so in svgoutfiles]):
            i += 1
            tmp = outputfilename[:-4] + '_' + str(i) + '.svg'
        outputfilename = tmp
        if modheight:
            modSVG(f'{path}/cache/{self.filename}.svg', outputfilename)
        else:
            modSVG(f'{path}/cache/{self.filename}.svg', outputfilename, ptincrement=0)
    

