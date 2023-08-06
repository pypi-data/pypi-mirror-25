#pragma once

#include "Python.hpp"

#include "ContextMember.hpp"

struct MGLFramebufferAttachment : public MGLContextMember {
	union {
		int renderbuffer_obj;
		int texture_obj;
	};

	int width;
	int height;
	int components;

	int samples;

	bool floats;
	bool depth;
};
