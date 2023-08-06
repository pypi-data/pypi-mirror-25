#pragma once

#include "Python.hpp"

#include "Object.hpp"

struct MGLSubroutineUniform : public MGLObject {
	PyObject * name;
	int location;
};

extern PyTypeObject MGLSubroutineUniform_Type;

MGLSubroutineUniform * MGLSubroutineUniform_New();
void MGLSubroutineUniform_Complete(MGLSubroutineUniform * subroutine_uniform);
