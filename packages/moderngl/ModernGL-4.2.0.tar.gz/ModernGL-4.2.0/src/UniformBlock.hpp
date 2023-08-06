#pragma once

#include "Python.hpp"

#include "Object.hpp"
#include "GLMethods.hpp"

struct MGLUniformBlock : public MGLObject {
	const GLMethods * gl;

	PyObject * name;

	int program_obj;

	int index;
	int size;
};

extern PyTypeObject MGLUniformBlock_Type;

MGLUniformBlock * MGLUniformBlock_New();
void MGLUniformBlock_Complete(MGLUniformBlock * uniform_block, const GLMethods & gl);
