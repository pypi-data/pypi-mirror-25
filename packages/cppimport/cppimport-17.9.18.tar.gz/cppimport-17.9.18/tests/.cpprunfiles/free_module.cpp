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
PYBIND11_PLUGIN(${fullname}) {
    pybind11::module m("${fullname}", "");
    m.def("main", main);
    return m.ptr();
}
