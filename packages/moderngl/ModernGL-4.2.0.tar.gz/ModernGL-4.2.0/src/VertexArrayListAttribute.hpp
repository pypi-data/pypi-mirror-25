#pragma once

#include "Python.hpp"

#include "Object.hpp"

struct MGLVertexArrayListAttribute : public MGLObject {
	PyObject * content;
	int location;
};

extern PyTypeObject MGLVertexArrayListAttribute_Type;

MGLVertexArrayListAttribute * MGLVertexArrayListAttribute_New();
