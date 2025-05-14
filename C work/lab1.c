#include <stdio.h>

struct freq{
int value;
int frequency;
};

void readScores(int* v, int* c){
	int count = 0;
	int a = 0;
	while(a != -1){
	int x;
	int y;
	y = scanf("%d", &x);
	a = y;
	if(a != -1){
		v[count] = x;
		count++;
	}
	}
	*c = count;
}

void calcHistogram(struct freq* f, int* c, int* v, int* histC){
	int histCnt = 0;
	for(int i = 0; i < *c; i++){
	int cur = v[i];
	int found = 0;
		for(int j = 0; j < histCnt; j++){
			if(f[j].value == cur){
			f[j].frequency++;
			found = 1;
			}		
		}
		if(found == 0){
		f[histCnt].value = cur;
		f[histCnt].frequency =  1;
		histCnt = histCnt + 1;
		}
	}
	*histC = histCnt;
}

void displayScores(int v[], int* count){
	for(int i = 0; i < *count; i++){
		printf("score %d: %d\n", i, v[i]); 
	}
}

void sortHistogram(struct freq* f,int* histC){
	for(int i = 0; i < *histC; i++){
		int max = f[i].frequency;
		int maxI = 0;
		for(int j = i+1; j < *histC; j++){
			if(f[j].frequency > max){
			max = f[j].frequency;
			maxI = j;
		}
		struct freq temp = f[i];
		f[i] = f[maxI];
		f[maxI] = temp;
		}
	}
}

void displayHistogram(struct freq* f, int* histC){
	for(int i = 0; i < *histC; i++){
		printf("value %d: freq %d\n", f[i].value, f[i].frequency);
	}
}

int main(){
        int vals[100];
        int count = 0;
	int histCount = 0;
        readScores(vals, &count);
        displayScores(vals, &count);
	//start histogram programs
	printf("\n");
	struct freq hist[count];
	calcHistogram(hist, &count, vals, &histCount);
	displayHistogram(hist, &histCount);
	printf("\n");
	sortHistogram(hist, &histCount);
	displayHistogram(hist, &histCount);
}

