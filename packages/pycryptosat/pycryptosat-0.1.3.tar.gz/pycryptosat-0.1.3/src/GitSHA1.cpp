/******************************************
Copyright (c) 2017, Mate Soos

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
THE SOFTWARE.
***********************************************/

#include "src/GitSHA1.h"
const char* get_version_sha1()
{
    static const char myversion_sha1[] = "5f4c574f7e189050d66f92d4a167f3f577ff76f0";
    return myversion_sha1;
}

const char* get_version_tag()
{
    static const char myversion_tag[] = "5.0.1";
    return myversion_tag;
}

const char* get_compilation_env()
{
    static const char compilation_env[] =
    "CMAKE_CXX_COMPILER = /usr/bin/c++ | "
    "CMAKE_CXX_FLAGS =  -std=c++11 -g -pthread -Wall -Wextra -Wunused -pedantic -Wsign-compare -fno-omit-frame-pointer -Wtype-limits -Wuninitialized -Wno-deprecated -Wstrict-aliasing -Wpointer-arith -fvisibility=hidden -Wpointer-arith -Wformat-nonliteral -Winit-self -Wparentheses -Wunreachable-code -ggdb3 -fPIC | "
    "COMPILE_DEFINES =  -DUSE_PTHREADS -DBOOST_TEST_DYN_LINK -DUSE_ZLIB | "
    "STATICCOMPILE = OFF | "
    "ONLY_SIMPLE = OFF | "
    "Boost_FOUND = 1 | "
    "STATS = OFF | "
    "SQLITE3_FOUND =  | "
    "ZLIB_FOUND = TRUE | "
    "VALGRIND_FOUND = TRUE | "
    "ENABLE_TESTING = OFF | "
    "M4RI_FOUND = FALSE | "
    "SLOW_DEBUG = OFF | "
    "ENABLE_ASSERTIONS = ON | "
    "PYTHON_EXECUTABLE = /home/Lex/.virtualenvs/cadbiom2/bin/python | "
    "PYTHON_LIBRARY = /usr/lib/x86_64-linux-gnu/libpython2.7.so | "
    "PYTHON_INCLUDE_DIRS = /usr/include/python2.7 | "
    "MY_TARGETS =  | "
    "LARGEMEM = OFF | "
    "LIMITMEM = OFF | "
    "compilation date time = " __DATE__ " " __TIME__
    ""
    ;
    return compilation_env;
}
