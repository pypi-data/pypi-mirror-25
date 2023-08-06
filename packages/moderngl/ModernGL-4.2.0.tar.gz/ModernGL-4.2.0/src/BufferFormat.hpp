#pragma once

struct FormatNode {
	int count;
	int size;
	char shape;
};

struct FormatInfo {
	int nodes;
	int size;
	int divisor;
	bool valid;
};

struct FormatIterator {
	const char * ptr;
	FormatNode node;

	FormatIterator(const char * str);

	FormatInfo info();
	FormatNode * next();
};

extern FormatNode * InvalidFormat;
