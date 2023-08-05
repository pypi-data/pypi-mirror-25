
#include "swigExtras.h"
#include <string>
#include <iostream>
using namespace std;


int ReadSpec ( const char* theFileName, BufferType* myBuffer,  char * allAtts )
{

    AttributeList * myList = NULL;
    int err = 0;
    err = ReadIM7 ( theFileName, myBuffer, &myList );
    int cntr = 0;
    char str[10000];
    str[0] = '\0';
    while (myList)
		{
        cntr++;
         AttributeList* ptr = myList;
         myList = myList->next;
         sprintf(str, "%s%sATTDIV%sATTSEP", str, ptr->name, ptr->value);
         free(ptr->name);
         free(ptr->value);
         free(ptr);
      }
    strcpy(allAtts, str);

    //allAtts = (char*)malloc(sizeof(char)*sizeof(str));
    //memcpy(allAtts, str, sizeof(str));
    //return cntr;
    return err;
}

int ReadSpec2 ( const char* theFileName, BufferType* myBuffer,  AttributeList * myListin )
{

    AttributeList * myList = NULL;
    int err = 0;
    err = ReadIM7 ( theFileName, myBuffer, &myList );

    myListin->next = myList;
    return err;
}




void DestroyAttributeList2(AttributeList * myListin)
{
    AttributeList * myList = myListin->next;
    DestroyAttributeList(&myList);
}
