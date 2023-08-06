
PyGLM ( WIP )
=============

A lazy implementation of OpenGL Mathematics (GLM).

Why "lazy"? - PyGLM is in it's core a translation of GLM (by hand), 
which is why I lazily left some features out.
For example, there is no tvec1 in PyGLM, because I didn't see the need for it,
if you think differently, please tell me by posting an issue over on `GitHub <https://github.com/Zuzu-Typ/PyGLM>`_.
Another example would be the lack of different precisions (like highp and lowp).

PyGLM is still in active development (hence the WIP), so please let me know if you 
experience any issues or want to request additional features.

To install PyGLM, just use the default PyPI procedure.
	
    pip install PyGLM


To import PyGLM's functions, simply use 'import glm'.

Example:

    import glm
    	
    v = glm.vec3()
    	
    v.x = 7
    	
    z = v.xxx
    	
    print(z)

	
You can define macros in prep.py (in the glm folder).
For example:
	
    GLM_FORCE_MESSAGES = True