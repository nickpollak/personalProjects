#include <iostream>
#include <thread>
#include <omp.h>
#include <mutex>

std::mutex screenLock;

bool isPrime(int n);
int blocking(int start, int stop);
int striping(int start, int stop);

int main(){
  //serial
  //int n;
  //std::cout << "Type start number: ";
  //std::cin >> n;
  //int m;
  //std::cout << "Type stop number: ";
  //std::cin >> m;
  //int x = primesInRange(n, m);
  //std::cout << "Number of primes from "<< n << " to " << m << ": " << x;

  //blocking
  int start, stop;
  std::cout <<"Type start Number: ";
  std::cin >> start;
  std::cout << "Type stop Number: ";
  std::cin >> stop;
  omp_set_num_threads(4);
  int primes = striping(start, stop);
}

bool isPrime(int n){
  int i = 2;
  while(i < n){
    if(n % i == 0){
      return false;
    }
    i++;
  }
  return true;
}

//blocking
int blocking(int start, int stop){
  int n = stop - start;
  int total = 0;
  double startT = omp_get_wtime();
  #pragma omp parallel reduction(+: total)
  {
  
  int threadCount = omp_get_num_threads();
  int threadNum = omp_get_thread_num();
  #pragma omp for schedule(static, stop/threadCount) nowait
    for(int i = start; i < stop; i++){
      if(isPrime(i)){
        total++;
      }
    }
    double threadT = omp_get_wtime();
    double myThreadT = threadT - startT;
    std::cout << "Time for " << threadNum << ": " << myThreadT<< " with " << total << " primes found.\n";
  }
  double endT = omp_get_wtime();
  double overallT = endT - startT;
  std::cout << "Overall Time: " << overallT << " with " << total << " primes found.";
  return total;
}

//striping
int striping(int start, int stop){
  int n = stop - start;
  int total = 0;
  double startT = omp_get_wtime();
  #pragma omp parallel reduction(+: total)
  {
  
  int threadCount = omp_get_num_threads();
  int threadNum = omp_get_thread_num();
  #pragma omp for schedule(static, 2) nowait
    for(int i = start; i < stop; i++){
      if(isPrime(i)){
        total++;
      }
    }
    double threadT = omp_get_wtime();
    double myThreadT = threadT - startT;
    screenLock.lock();
    std::cout << "Time for " << threadNum << ": " << myThreadT<< " with " << total << " primes found.\n";
    screenLock.unlock();
  }
  double endT = omp_get_wtime();
  double overallT = endT - startT;
  std::cout << "Overall Time: " << overallT << " with " << total << " primes found.";
  return total;
}


