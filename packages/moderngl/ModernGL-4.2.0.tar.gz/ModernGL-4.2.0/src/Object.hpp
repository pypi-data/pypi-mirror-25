#pragma once

#include "Python.hpp"

struct MGLObject {
	PyObject_HEAD
};

extern PyTypeObject MGLObject_Type;
