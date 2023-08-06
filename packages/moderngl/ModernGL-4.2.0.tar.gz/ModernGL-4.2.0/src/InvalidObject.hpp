#pragma once

#include "Python.hpp"

#include "Object.hpp"

struct MGLInvalidObject : public MGLObject {
};

extern PyTypeObject MGLInvalidObject_Type;
