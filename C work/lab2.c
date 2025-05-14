#include <stdio.h>
#include <stdlib.h>
#include <string.h>

typedef struct freq{
char* str;
int frequency;
}Histogram;

char** readScores(int* c){
        char** vals = (char**) malloc(100 * sizeof(char*));
	int count = 0;
	char* a = (char*) malloc(20 * sizeof(char));	
        while((scanf("%s",a)) != EOF){
        	int len = strlen(a);
		char* newW = (char*) malloc((len + 1) * sizeof(char));
		strcpy(newW, a);
		*(vals + count) = newW;
		count++;
	}
	free(a);	
        *c = count;
	return vals;
}

int calcHistogram(int c, char** v, Histogram* f){
	Histogram* hist = (Histogram*) malloc(c * sizeof(Histogram));
        int histCnt = 0;
        for(int i = 0; i < c; i++){
        char* cur = (*(v + i));
        int found = 0;
                for(int j = 0; j < histCnt; j++){
                        if((strcmp((*(f + j)).str, cur) == 0)){
                        (*(f + j)).frequency++;
                        found = 1;
                        }
                }
                if(found == 0){
                (*(f + histCnt)).str = cur;
                (*(f + histCnt)).frequency = 1;
                histCnt = histCnt + 1;
                }
        }
	f = hist;
	free(hist);
        return histCnt;
}


void displayScores(char** v, int count){
	for(int i = 0; i < count; i++){
		printf("Number %d: %s\n", i, (*(v + i))); 
	}
}

void sortHistogram(struct freq* f,int histC){
	for(int i = 0; i < histC; i++){
		int max = (f + i)->frequency;
		int maxI = 0;
		for(int j = i + 1; j < histC; j++){
			if((f + j)->frequency > max){
			max = (f + j)->frequency;
			maxI = j;
		}
		struct freq temp = *(f + i);
		*(f + i) = *(f + maxI);
		*(f + maxI) = temp;
		}
	}
}

void displayHistogram(Histogram* f, int histC){
	for(int i = 0; i < histC; i++){
	printf("String %s: freq %d\n", (*(f + i)).str, (*(f + i)).frequency);
	}
}

int main(){
        char** vals;
        int count = 0;
	int histCount = 0;
        vals = readScores(&count);
        displayScores(vals, count);

	//start histogram programs
	printf("\n");
	Histogram hist[count];
	histCount = calcHistogram(count, vals, hist);
	displayHistogram(hist, histCount);
	printf("\n");
	sortHistogram(hist, histCount);
	displayHistogram(hist, histCount);
	for(int i = 0; i < count; i++){
		free(*(vals + i));
	}
	free(vals);

}
