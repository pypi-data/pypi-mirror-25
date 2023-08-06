Shaders and Programs
********************

.. currentmodule:: ModernGL

.. automethod:: Context.vertex_shader(source) -> Shader
	:noindex:

.. automethod:: Context.fragment_shader(source) -> Shader
	:noindex:

.. automethod:: Context.geometry_shader(source) -> Shader
	:noindex:

.. automethod:: Context.tess_evaluation_shader(source) -> Shader
	:noindex:

.. automethod:: Context.tess_control_shader(source) -> Shader
	:noindex:

.. automethod:: Context.program(shaders, varyings=()) -> Program
	:noindex:

.. autoclass:: Shader
	:members: source

.. autoclass:: Program
	:members: uniforms, uniform_blocks, attributes, varyings, vertex_shader, fragment_shader, geometry_shader, tess_evaluation_shader, tess_control_shader, geometry_input, geometry_output, geometry_vertices

.. toctree::
	:maxdepth: 4
	:caption: Classes:

	Uniforms <Uniforms.rst>
	UniformBlocks <UniformBlocks.rst>
	Attributes <Attributes.rst>
	Varyings <Varyings.rst>
	ProgramStages <ProgramStages.rst>
