import os
import json

def readfiles(basedir, ftype=None):
    obj = {}

    for path, dirs, files in os.walk(basedir):
        if '.svn' in dirs:
            dirs.remove('.svn')
        o = obj
        if path == basedir:
            path = ""
        else:
            apath = path.split('/')[1:]
            for subdir in apath:
                o = o[subdir]
            path = '/'.join(apath) + '/'

        for filename in files:
            name, ext = os.path.splitext(filename)
            if ftype and ext != '.' + ftype:
                continue

            fpath = path + name
            data = open(basedir + '/' + fpath + ext)
            if ftype == "json":
                try:
                    o[name] = json.load(data)
                except ValueError:
                    print "Could not parse %s!" % name
                    raise
            else:
                o[name] = data.read()

        for name in dirs:
            o[name] = {}

    return obj
    

def collectjson(conf, directory):
    "Collect files and dump the result into a JSON object"
    obj = {}
    cur = os.getcwd()
    os.chdir(directory)

    for d in conf['paths']:
        obj.update(readfiles(d, conf['type']))

    outfile = open(conf['output'], 'w')

    opts = dict([
        (str(key), value)
        for key, value in conf.get('json', {'indent': 4}).items()
    ])

    if 'jsonp' in conf:
        txt = json.dumps(obj, **opts)
        txt = '%s(%s);' % (conf['jsonp'], txt)
        outfile.write(txt)
    else:
        json.dump(obj, outfile, **opts)

    print '%s: %s objects collected from %s' % (conf['output'], len(obj), ', '.join(conf['paths']))

    outfile.close()
    os.chdir(cur)