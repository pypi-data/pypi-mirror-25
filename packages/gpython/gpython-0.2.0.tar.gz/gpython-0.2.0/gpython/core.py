import os
import shutil
import subprocess
import tempfile
from distutils import sysconfig
from distutils._msvccompiler import MSVCCompiler
from distutils.util import get_platform

CVARS = sysconfig.get_config_vars()

CPP = '''
#include <Windows.h>
#include <Python.h>

extern "C" {
#ifdef _MSC_VER
	_declspec(dllexport) DWORD NvOptimusEnablement = 0x00000001;
	_declspec(dllexport) int AmdPowerXpressRequestHighPerformance = 0x00000001;
#else
	__attribute__((dllexport)) DWORD NvOptimusEnablement = 0x00000001;
	__attribute__((dllexport)) int AmdPowerXpressRequestHighPerformance = 0x00000001;
#endif
}

int main() {
	int argc = 0;
	LPWSTR * argv = CommandLineToArgvW(GetCommandLineW(), &argc);
	Py_Main(argc, argv);
}
'''

def install():
    msvcc = MSVCCompiler()
    msvcc.initialize()
    msvcc.add_include_dir(CVARS['INCLUDEPY'])
    msvcc.add_library_dir(os.path.join(CVARS['exec_prefix'], 'libs'))

    with tempfile.TemporaryDirectory() as tempdir:
        open(os.path.join(tempdir, 'gpython.cpp'), 'w').write(CPP)

        args = [msvcc.cc]
        args += ['/nologo', '/Ox', '/W3', '/GL', '/DNDEBUG', '/MD']
        args += ['-I' + inc for inc in msvcc.include_dirs]
        args += ['gpython.cpp']
        args += ['/link']
        args += ['/LIBPATH:' + inc for inc in msvcc.library_dirs]
        args += ['User32.lib', 'Shell32.lib']
        args += ['/OUT:gpython.exe']

        subprocess.Popen(args, cwd=tempdir).wait()


def uninstall():
    exe = os.path.join(CVARS['exec_prefix'], 'gpython.exe')
    os.unlink(exe)
