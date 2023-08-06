#pragma once

#include "Python.hpp"

#include "FramebufferAttachment.hpp"

#include "TextureFilter.hpp"

struct MGLTexture : public MGLFramebufferAttachment {
	MGLTextureFilter * filter;
	bool repeat_x;
	bool repeat_y;
};

extern PyTypeObject MGLTexture_Type;

MGLTexture * MGLTexture_New();
void MGLTexture_Invalidate(MGLTexture * texture);
