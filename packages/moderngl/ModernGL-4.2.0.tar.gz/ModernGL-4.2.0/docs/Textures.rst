Textures
********

.. currentmodule:: ModernGL

.. automethod:: Context.texture(size, components, data=None, samples=0, floats=False) -> Texture
	:noindex:

.. automethod:: Context.depth_texture(size, data=None, samples=0) -> Texture
	:noindex:

.. automethod:: Context.texture3d(size, components, data=None, floats=False) -> Texture3D
	:noindex:

.. autoclass:: Texture
	:members: width, height, size, components, samples, floats, depth, filter, repeat_x, repeat_y, swizzle

	.. automethod:: read(alignment=1) -> bytes
	.. automethod:: read_into(buffer, alignment=1, write_offset=0)
	.. automethod:: write(data, viewport=None, alignment=1)
	.. automethod:: build_mipmaps(base=0, max_level=1000)
	.. automethod:: use(location=0)

.. autoclass:: Texture3D
	:members: width, height, depth, size, components, floats, filter, repeat_x, repeat_y, repeat_z, swizzle

	.. automethod:: read(alignment=1) -> bytes
	.. automethod:: read_into(buffer, alignment=1, write_offset=0)
	.. automethod:: write(data, viewport=None, alignment=1)
	.. automethod:: build_mipmaps(base=0, max_level=1000)
	.. automethod:: use(location=0)

.. autoclass:: TextureCube
	.. automethod:: use(location=0)

.. toctree::
	:maxdepth: 4
