Uniform
*******

.. currentmodule:: ModernGL

.. autoclass:: Uniform
	:members: name, location, dimension, array_length, value

	.. automethod:: read() -> bytes
	.. automethod:: write(value)

.. autoclass:: UniformMap

	.. automethod:: __getitem__(key) -> Uniform

.. toctree::
	:maxdepth: 4
