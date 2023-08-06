#include <stdlib.h>
#include <string.h>
#include <stdio.h>
#include <time.h>

#define SIZE 10 * 1024 * 1024


int main(int argc, char *argv[]) {
  int i;
  int *p;
  int sum = 0;
  clock_t start;
  float clock_alloc, clock_new, clock_used;

  for (i = 0; i < 500; i ++) {
    start = clock();
    p = (int *) malloc(SIZE);
    clock_alloc += (float)(clock() - start) / CLOCKS_PER_SEC;
    
    start = clock();
    memset(p, 0, SIZE);
    clock_new += (float)(clock() - start) / CLOCKS_PER_SEC;
    sum += p[512];
    
    start = clock();
    memset(p, 0, SIZE);
    clock_used += (float)(clock() - start) / CLOCKS_PER_SEC;
    sum += p[512];

    free(p);
  }
  printf("sum %d\n", sum);
  printf("alloc: %f\nnew %f\nused %f\n", clock_alloc, clock_new, clock_used);
  return 0;
}