#include <math.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

int logBase(int base, int value);

int binToDec(char* bin){
	int result = 0;
	char current;
	for(int i = 0; i < strlen(bin); i++){
		current = *(bin + i);
		if(current == '1'){
			result = result + pow(2, strlen(bin) - 1 - i);
		}
	}
	return result;
}

char* decToBin(int dec){
	char* bin = (char*) malloc(16 * sizeof(char));
	int len = logBase(2, dec);
	if(dec > 0){
		for(int i = len; i >= 0; i--){
			if((dec - pow(2,i) >= 0)){
				*(bin + (len - i)) = '1';
				dec = dec - pow(2,i);
			}else{
				*(bin + (len - i)) = '0';
			}
		}
	}
	return bin;
}

int logBase(int base, int value){
	double logB = log(value)/log(base);
	return (int)logB;
}

int baseToDec(int base, char* value){
	int result = 0;
	char current;
	if(base <= 9){
		for(int i = 0; i < strlen(value); i++){
			current = *(value + i);
			if(current != '0'){
				int cur = ((int)*(value + i) - 48);
				result += cur * pow(base, (strlen(value) - 1  - i));
			}
		}
	}
	if(base >= 10){
		for(int i = 0; i < strlen(value); i++){
		current = *(value + i);
		int check = ((int)*(value + i) - 48);
		if(check <= 9 && check >= 0){
			result += check * pow(base, (strlen(value) - 1 - i));
		}else{
			int AE = ((int) *(value + i) - 87);
			result += AE * pow(base, (strlen(value) - 1 - i));
		}
		}	
	}
	return result;
}

char* decToBase(int base, int dec){
	char* result = (char*)malloc(16 * sizeof(char));
	int len = logBase(base, dec);
	if(base <= 9){
		for(int i = len; i >= 0; i--){
			int num = dec / ((int)(pow(base, i)));
			*(result + len - i) = (num + 48);
			dec = dec % ((int)(pow(base, i))); 
		}
	}
	if(base >= 10){
		for(int i = len; i >= 0; i--){
			int num = dec / ((int)(pow(base, i)));
			if(num < 10){
			*(result + len - i) = (num + 48);
			dec = dec % ((int)(pow(base, i)));
			}else{
			*(result + len - i) = (num + 87);
			dec = dec % ((int)(pow(base,i)));
			}
		}	
	}
	return result;
}

int main(){
	char* a = "11001";
	int b = 25;
	int test = binToDec(a);
	char* test2 = decToBin(b);	
	//printf("%d\n", test);
	//printf("%s\n", test2);
	free(test2);

	int dec = baseToDec(2, "11001");
	int dec2 = baseToDec(8, "157");
	int dec3 = baseToDec(16, "f8");	
	char* dec4 = decToBase(2, 25);
	char* dec5 = decToBase(8, 111);
	char* dec6 = decToBase(16, 248);
	printf("%d\n", dec);
	printf("%d\n", dec2);
	printf("%d\n", dec3);
	printf("%s\n", dec4);
	printf("%s\n", dec5);
	printf("%s\n", dec6);
}
