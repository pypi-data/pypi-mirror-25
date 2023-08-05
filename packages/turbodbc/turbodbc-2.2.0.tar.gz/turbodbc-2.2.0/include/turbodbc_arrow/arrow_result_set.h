#pragma once

#include <turbodbc/result_sets/row_based_result_set.h>
#include <turbodbc/field.h>
#include <turbodbc/field_translator.h>
#include <pybind11/pybind11.h>

namespace arrow {

class Schema;
class Status;
class Table;

}

namespace turbodbc_arrow {

/**
 * @brief This class adapts a result_set to provide access in
 *        terms of Apache Arrow python objects
 */
class arrow_result_set {
public:
	/**
	 * @brief Create a new numpy_result_set which presents data contained
	 *        in the base result set in a row-based fashion
	 */
	arrow_result_set(turbodbc::result_sets::result_set & base);

	/**
	 * @brief Retrieve a native (C++) Arrow Table which contains
	 *        values and masks for all data
	 */
  arrow::Status fetch_all_native(std::shared_ptr<arrow::Table>* out);

	/**
	 * @brief Retrieve a boost Python object which contains
	 *        values and masks for all data as pyarrow.Table
	 */
  pybind11::object fetch_all();

  /**
   * @brief Translate the schema information into an Arrow schema
   */
  std::shared_ptr<arrow::Schema> schema();

private:
	turbodbc::result_sets::result_set & base_result_;
};

}
