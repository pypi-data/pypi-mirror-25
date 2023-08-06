#pragma once

#include "Python.hpp"

#include "Object.hpp"
#include "GLMethods.hpp"

#include "Attribute.hpp"

struct MGLVertexArrayAttribute : public MGLObject {
	MGLAttribute * attribute;

	int vertex_array_obj;
	int location;
};

extern PyTypeObject MGLVertexArrayAttribute_Type;

MGLVertexArrayAttribute * MGLVertexArrayAttribute_New();
void MGLVertexArrayAttribute_Complete(MGLVertexArrayAttribute * attribute, const GLMethods & gl);
