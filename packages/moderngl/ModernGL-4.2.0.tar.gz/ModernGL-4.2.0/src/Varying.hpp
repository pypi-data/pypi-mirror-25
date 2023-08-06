#pragma once

#include "Python.hpp"

#include "Object.hpp"
#include "GLMethods.hpp"

struct MGLVarying : public MGLObject {
	PyObject * name;

	int number;
	int type;

	int array_length;

	bool matrix;
};

extern PyTypeObject MGLVarying_Type;

MGLVarying * MGLVarying_New();
void MGLVarying_Invalidate(MGLVarying * varying);
void MGLVarying_Complete(MGLVarying * varying, const GLMethods & gl);
