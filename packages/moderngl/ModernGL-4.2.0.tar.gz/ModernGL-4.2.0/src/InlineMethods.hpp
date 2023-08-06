#pragma once

inline void clean_glsl_name(char * name, int & name_len) {
	if (name_len && name[name_len - 1] == ']') {
		name_len -= 1;
		while (name_len && name[name_len] != '[') {
			name_len -= 1;
		}
	}
	name[name_len] = 0;
}

inline int swizzle_from_char(char c) {
	switch (c) {
		case 'R':
		case 'r':
		// case 'X':
		// case 'x':
			return GL_RED;

		case 'G':
		case 'g':
		// case 'Y':
		// case 'y':
			return GL_GREEN;

		case 'B':
		case 'b':
		// case 'Z':
		// case 'z':
			return GL_BLUE;

		case 'A':
		case 'a':
		// case 'W':
		// case 'w':
			return GL_ALPHA;

		case '0':
			return GL_ZERO;

		case '1':
			return GL_ONE;
	}

	return -1;
}

inline char char_from_swizzle(int c) {
	switch (c) {
		case GL_RED:
			return 'R';

		case GL_GREEN:
			return 'G';

		case GL_BLUE:
			return 'B';

		case GL_ALPHA:
			return 'A';

		case GL_ZERO:
			return '0';

		case GL_ONE:
			return '1';
	}

	return '?';
}
