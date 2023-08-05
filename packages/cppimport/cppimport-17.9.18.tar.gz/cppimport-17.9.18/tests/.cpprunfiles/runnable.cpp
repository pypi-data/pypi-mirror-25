#include <iostream>

int main() {
    std::cout << "HI!" << std::endl;
}

<%
import pybind11
cfg['compiler_args'] = ['-std=c++11']
cfg['include_dirs'] = [pybind11.get_include(), pybind11.get_include(True)]
%>
#include <pybind11/pybind11.h>
#include <pybind11/pybind11.h>
namespace py = pybind11;
PYBIND11_PLUGIN(runnable) {
    py::module m("runnable", "");
    m.def("main", main);
    return m.ptr();
}
