#include <iostream>
#include <thread>

bool isPrime(int n);

  void myRun(int threadNum, int start, int stop, int* primes){
    int total = 0;
    for(int i = start; i < stop; i++){
       if(isPrime(i)){
	  total = total + 1;
       }
    }
    primes[threadNum] = total;
  }

bool isPrime(int n) {
  int i = 2;
  while(i < n){
    if(n % i == 0) {
    return false;
    }
  i++;
  }
  return true;
}

int main(){
  int n = 1000000;
  int numThreads = 4;
  int* primes = (int*)malloc(numThreads * sizeof(int));
  std::thread* ths[numThreads];
  for (int i=0; i<numThreads; i++) {
    int start = (n/numThreads)*i;
    int stop = (n/numThreads)*(i+1);
    std::thread* th = new std::thread(myRun, i, start, stop, primes);
    ths[i] = th;
  }

  for (int i=0; i<numThreads; i++) {
    ths[i]->join();
  }

  int totalPrimes = 0;
  for(int i = 0; i < numThreads; i++){
	totalPrimes = totalPrimes + primes[i];
  }
  printf("number of primes: %d", totalPrimes);
  
}

