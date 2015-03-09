import httplib

for code, name in httplib.responses.iteritems():
    const_name = '_'.join( name.split() )
    globals()[const_name] = code
