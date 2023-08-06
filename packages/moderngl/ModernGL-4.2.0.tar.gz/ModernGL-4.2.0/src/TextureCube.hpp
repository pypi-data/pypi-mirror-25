#pragma once

#include "Python.hpp"

#include "FramebufferAttachment.hpp"

#include "TextureFilter.hpp"

struct MGLTextureCube : public MGLContextMember {
	int texture_obj;

	int width;
	int height;
	int depth;

	int components;

	bool floats;
};

extern PyTypeObject MGLTextureCube_Type;

MGLTextureCube * MGLTextureCube_New();
void MGLTextureCube_Invalidate(MGLTextureCube * texture);
