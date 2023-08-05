#include <iostream>

int main() {
    std::cout << "HI!" << std::endl;
}


#include <pybind11/pybind11.h>
PYBIND11_PLUGIN(free_module) {
    pybind11::module m("free_module", "");
    m.def("main", main);
    return m.ptr();
}
