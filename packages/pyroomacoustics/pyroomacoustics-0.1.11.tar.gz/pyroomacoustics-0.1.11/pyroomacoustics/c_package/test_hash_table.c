
#include <stdio.h>
#include "hash_table.h"

int main(int argc, char **argv)
{
  int p[2];
  for (p[0] = 0 ; p[0] < 2 ; p[0]++)
    for (p[1] = 0 ; p[1] < 4 ; p[1]++)
      printf("p0: %d p1: %d\n", p[0], p[1]);
}
