# Read from Geom file
def readGeomFile(fname):
    ## geometry dictionary contains the parameters used to initialize the detector
    geom = {}
    with open(fname) as f:
        content = f.readlines()
        for line in content:
            if line[0] != '#' and line[0] != ';' and len(line) > 1:
                tmp = line.replace('=', ' ').split()
                if tmp[0] == 'geom/d':
                    geom.update({'distance':float(tmp[1])})
                if tmp[0] == 'geom/pix_width':
                    geom.update({'pixel size':float(tmp[1])})
                if tmp[0] == 'geom/px':
                    geom.update({'pixel number': int(tmp[1])})
        
    return geom