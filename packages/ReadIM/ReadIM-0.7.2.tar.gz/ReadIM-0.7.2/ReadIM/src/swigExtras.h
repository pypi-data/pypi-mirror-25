#ifndef __SWIG_EXT_H
#define __SWIG_EXT_H

#include "ReadIMX.h"
#include "ReadIM7.h"


int ReadSpec ( const char* theFileName, BufferType* myBuffer,  char * allAtts );
int ReadSpec2 ( const char* theFileName, BufferType* myBuffer,   AttributeList * myListin);
void DestroyAttributeList2(AttributeList * myListin);


#endif

