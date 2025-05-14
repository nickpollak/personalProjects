
#ifndef linkedList_h
#define linkedList_h

LinkedList* llCreate();
int llIsEmpty(LinkedList* ll);
void llDisplay(LinkedList* ll);
void llAdd(LinkedList** ll, int newValue);
void llFree(LinkedList* ll);
void list_add_in_order(LinkedList** ll, tNode* n);
tNode* remove(LinkedList** ll);
tNode* createFreqTable(FILE* a);
tNode* createHuffmanTree(struct tNode* nodes);
void encodeFile(FILE readIn, tNode* leaf);
void decodeFile(char** args, tNode* huffs);
typedef struct tNode();
typedef struct node();

#endif /* linkedList_h */
