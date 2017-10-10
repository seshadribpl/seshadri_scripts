import os
import tempfile

tmpdir = tempfile.mkdtemp()
filename = 'myfile'
path = os.path.join(tmpdir, filename)
mymask = os.umask(0077)

print 'The tmpdir, filename and path are {}, {}, and {}'.format(tmpdir, filename, path)


try:
    with open(path, "w") as tmp:
        tmp.write('secret')
except IOError as e:
    print 'IOError'
else: 
    print 'Now removing the dir and file {}'.format(path)
    os.remove(path)
finally:
    os.umask(mymask)
    os.rmdir(tmpdir)
