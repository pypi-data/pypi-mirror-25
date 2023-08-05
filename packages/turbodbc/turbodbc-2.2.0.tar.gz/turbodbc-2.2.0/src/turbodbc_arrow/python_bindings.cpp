#include <turbodbc_arrow/arrow_result_set.h>

#include <pybind11/pybind11.h>

using turbodbc_arrow::arrow_result_set;

namespace {

arrow_result_set make_arrow_result_set(std::shared_ptr<turbodbc::result_sets::result_set> result_set_pointer)
{
	return arrow_result_set(*result_set_pointer);
}

}

PYBIND11_PLUGIN(turbodbc_arrow_support) {
    pybind11::module module("turbodbc_arrow_support", "Native helpers for turbodbc's Apache Arrow support");

    pybind11::class_<arrow_result_set>(module, "ArrowResultSet")
        .def("fetch_all", &arrow_result_set::fetch_all);

    module.def("make_arrow_result_set", make_arrow_result_set);
    return module.ptr();
}
