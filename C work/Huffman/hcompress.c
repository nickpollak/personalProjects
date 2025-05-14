#include <stdio.h>
#include "linkedList.h"

public tNode* createFreqTable(FILE* a){
  // array of t nodes read file add frequencies
  tNode* nodes = (tNode*)malloc(128 * sizeof(tNode));
  //add loop and initialize them all
  for(int i = 0; i < 128; i++){
	nodes[i].c = i;
	nodes[i].frequency = 0;
  }
  //make frequency for each node in nodes
  int b = 0;
  while((b = fgetc(a)) != -1){
      nodes[ch].frequency = nodes[ch].frequency + 1;
  }
  return nodes;
}

public tNode* createHuffmanTree(struct tNode* nodes){
  //This method will make a whole bunch of add in order calls to put the frequencies in order
  //then it will remove two and add the new node that has the left and rights set to the
  //leaf nodes back into the list til the linked list is just one node and thus the tree
  //Linked list added in order
  LinkedList* huff = llCreate();
  for(int i = 0; i < 128; i++){
	list_add_in_order(&huff, &nodes[i]);
  }
  //tNodes to store
  tNode* temp1;
  tNode* temp2;
  //take out the tNodes assign them to insert
  //then add in order to huff
  while((*huff)->next != NULL){
	temp1 = remove(&huff);
	temp2 = remove(&huff);
	tNode* insert = (tNode*)malloc(sizeof(tNode));
	insert->frequency = (temp1->frequency + temp2->frequency);
	temp1->parent = insert;
	temp2->parent = insert;
	insert->left = temp1;
	insert->right = temp2;
	insert->parent = NULL;
	list_add_in_order(&huff, &insert);
  }
  return *huff->value;
}

public void encodeFile(FILE readIn, tNode* leaf){
	int ch = fgetc(readIn);
	int a[1000];
	byte write = 0;
	int curSpot = 7;
	//loop for this code
	while(ch != -1){
	  int index = 0;
	  tNode* current = &leaf[ch];
	    while(current->parent != NULL){
	    if(current->parent->left == current){
		a[index] = 0;
		index++;
	    }
	    if(current->parent->right == current){
		a[index] = 1;
		index++;
	    }
	    }
	    //need to check if the values have filled the byte
	    while(index != 0){
	      if(curSpot != 0){
	  	unsigned short b = a[index] << curSpot;
		write |= b;
		index--;
		curSpot--;
		}
		//write
		fput(write, "huffman.huf");
		if(index != 0){
		curSpot = 7;
		}
	    }
	ch = fgetc(readIn);
	}
}

public void decodeFile(char** args, tNode* huffs){
  while(*args != NULL){
	tNode search = *huffs;
	while(search->right != NULL && search->left != NULL){
	  int count = 7;
	  byte a = *args >> count;
	  count--;
	  a &= 1;
		if(a == 1){
		search = search->right;
		}else{
		search = search->left;
		}
	}
	char character = search->c;
	fput(character, huffman.huf);
  }
}

int main(int argc, char *argv[]) {

  // Check the make sure the input parameters are correct

   if (argc != 3) {
      printf("Error: The correct format is \"hcompress -e filename\" or \"hcompress -d filename.huf\"\n"); fflush(stdout);

    exit(1);

  }
  LinkedList* ll = llCreate();
  

  struct tNode* leafNodes = createFreqTable("decind.txt");
	

  struct tNode* treeRoot = createHuffmanTree(leafNodes);


  if (strcmp(argv[1], "-e") == 0) {


encodeFile(argv[2], leafNodes);

  } else { // decode

decodeFile(argv[2], treeRoot);

  }

  return 0;

}
