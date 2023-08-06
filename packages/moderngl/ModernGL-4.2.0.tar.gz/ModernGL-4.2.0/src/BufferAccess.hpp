#pragma once

#include "Python.hpp"

#include "Object.hpp"
#include "GLMethods.hpp"

struct MGLBufferAccess : public MGLObject {
	GLMethods * gl;

	char * ptr;

	int buffer_obj;

	Py_ssize_t offset;
	Py_ssize_t size;

	int access;
};

extern PyTypeObject MGLBufferAccess_Type;

MGLBufferAccess * MGLBufferAccess_New();
