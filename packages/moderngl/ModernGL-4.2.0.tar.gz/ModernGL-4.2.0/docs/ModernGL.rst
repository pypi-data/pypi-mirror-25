ModernGL
********

ModernGL on `Github <https://github.com/cprogrammer1994/ModernGL>`_

If you have less time to read docs go to the `TL;DR <TLDR.html>`_ section.

.. rubric:: ModernGL and OpenGL

OpenGL is a great environment for developing portable, platform independent,
interactive 2D and 3D graphics applications. The API implementation in Python is cumbersome,
resulting in applications with high latency. To solve this problem we have developed ModernGL,
a wrapper over OpenGL that simplifies the creation of simple graphics applications like
scientific simulations, small games or user interfaces. Usually, acquiring in-depth knowledge
of OpenGL requires a steep learning curve. In contrast, ModernGL is easy to learn and use,
moreover it is capable of rendering with the same performance and quality, with less code written.

.. rubric:: How to install?

``pip install ModernGL``

.. rubric:: How to create a window?

ModernGL encapsulates the use of the OpenGL API, a separate module must be used for creating a window.
ModernGL can be integrated easily in GLWindow_, PyQt5_, pyglet_, pygame_, GLUT_ and many more.

.. _PyQt5: https://github.com/cprogrammer1994/ModernGL/tree/master/examples/PyQt5
.. _pyglet: https://github.com/cprogrammer1994/ModernGL/tree/master/examples/pyglet
.. _pygame: https://github.com/cprogrammer1994/ModernGL/tree/master/examples/pygame
.. _GLUT: https://github.com/cprogrammer1994/ModernGL/tree/master/examples/PyOpenGL
.. _GLWindow: https://github.com/cprogrammer1994/ModernGL/tree/master/examples/GLWindow

.. rubric:: How to create a context?

- Create a window
- Call :py:func:`ModernGL.create_context`

.. automodule:: ModernGL

	.. currentmodule:: ModernGL

.. toctree::
	:maxdepth: 4
	:caption: API Documentation:

	Context <Context.rst>

	Shaders and Programs <ShadersAndPrograms.rst>

	Buffers <Buffers.rst>
	VertexArrays <VertexArrays.rst>
	Textures <Textures.rst>

	Framebuffers <Framebuffers.rst>
	Renderbuffers <Renderbuffers.rst>
	ComputeShaders <ComputeShaders.rst>

	InvalidObjects <InvalidObjects.rst>
	Constants <Constants.rst>
	Errors <Errors.rst>
