VertexArray
***********

.. currentmodule:: ModernGL

.. automethod:: Context.simple_vertex_array(program, buffer, attributes) -> VertexArray
	:noindex:

.. automethod:: Context.vertex_array(program, content, index_buffer=None) -> VertexArray
	:noindex:

.. autoclass:: VertexArray
	:members: program, attributes, index_buffer, vertices, subroutines

	.. automethod:: render(mode=TRIANGLES, vertices=-1, first=0, instances=1)
	.. automethod:: transform(buf, mode=POINTS, vertices=-1, *, first=0, instances=1)

.. toctree::
	:maxdepth: 4
	:caption: Classes:

	Attributes <VertexArrayAttributes.rst>
