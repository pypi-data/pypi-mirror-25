#pragma once

#include "Python.hpp"

#include "Object.hpp"
#include "Context.hpp"

struct MGLContextMember : public MGLObject {
	MGLContext * context;
};
