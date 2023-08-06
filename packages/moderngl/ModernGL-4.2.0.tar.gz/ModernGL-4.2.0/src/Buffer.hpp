#pragma once

#include "Python.hpp"

#include "ContextMember.hpp"

struct MGLBuffer : public MGLContextMember {
	int buffer_obj;

	Py_ssize_t size;
	bool dynamic;
};

extern PyTypeObject MGLBuffer_Type;

MGLBuffer * MGLBuffer_New();
void MGLBuffer_Invalidate(MGLBuffer * buffer);
