#include <stdio.h>
#include <math.h>

typedef unsigned short bitSet;

void bitSet makeBitSet(){
	return 0;	
}

void displayBitSet(bitSet bs){
	for(int i = 0; i < 16; i++){
		int x = bitValue(*bs, i);
		printf("%d\n", x);
	}
}

void setBitSet(bitSet* bs, int index){
	unsigned short a = 1 << index;
	*bs |= a;	
}

void clearBitSet(bitSet* bs, int index){
	unsigned short a = ~(1 << index);
	*bs &= a;
}

int bitValue(bitSet bs, int index){
	int a =  *bs >> index;
	a &= 1;
	return a;
}

int main(){

}
