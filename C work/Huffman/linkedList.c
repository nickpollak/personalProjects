#include <stdio.h>
#include <stdlib.h> // malloc
#include "linkedList.h"

typedef struct node {
  struct tNode* value;
  struct node* next;
} LinkedList;

typedef struct tNode{
  int frequency;
  int c;
  struct tNode* left;
  struct tNode* right;
  struct tNode* parent;
}tNode;

LinkedList* llCreate();
int llIsEmpty(LinkedList* ll);
void llDisplay(LinkedList* ll);
void llAdd(LinkedList** ll, int newValue);
void llFree(LinkedList* ll);

LinkedList* llCreate() {
  return NULL;
}

int llIsEmpty(LinkedList* ll) {
  return (ll == NULL);
}

void llDisplay(LinkedList* ll) {
  
  LinkedList* p = ll;
  printf("[");
  
  while (p != NULL) {
    printf("%d, ", p->value->frequency);
    p = p->next;
  }
  printf("]\n");
}

void llAdd(LinkedList** ll, int newValue) {
  // Create the new node
  LinkedList* newNode = (LinkedList*)malloc(1 * sizeof(LinkedList));
  newNode->value->c = newValue;
  newNode->value->frequency = 1;
  newNode->next = NULL;
  
  // Find the end of the list
  LinkedList* p = *ll;
  if (p == NULL) {  // Add first element
    *ll = newNode;  // This is why we need ll to be a **
  } else {
    while (p->next != NULL) {
      p = p->next;
    }
    
    // Attach it to the end
    p->next = newNode;
  }
}

void llFree(LinkedList* ll) {
  LinkedList* p = ll;
  while (p != NULL) {
    LinkedList* oldP = p;
    p = p->next;
    free(oldP);
  }
}

void list_add_in_order(LinkedList** ll, tNode* n){
	LinkedList* newNode = (LinkedList*) malloc(1 * sizeof(LinkedList));
	newNode->value = n;
	newNode->value->frequency = n->frequency;
	LinkedList* p = *ll;

	//Case if list is empty
	if(p == NULL){
	  *ll = newNode;
	}else{
	//Case if adding to front of list ie frequency is smaller than all other freqs
	if(newNode->value->frequency < p->value->frequency){
	  newNode->next = p;
	  *ll = newNode;
	}else{
	//adding in the list
	while(p->next != NULL && (newNode->value->frequency) > (p->next->value->frequency)){
	  p = p->next;
	}
	newNode->next = p->next;
	p->next = newNode;
	}
	}
}

tNode* remove(LinkedList** ll){
  tNode* a = (*ll)->value;
  (*ll) = (*ll)->next;
  return a;
  //free malloced memory with this method
}

int main(){

}
