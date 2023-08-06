#ifndef __HASH_TABLE_H__
#define __HASH_TABLE_H__

#include <stdint.h>
#include <stdlib.h>
#include "room.h"

typedef struct is_table
{
  is_ll_t **table;
  size_t table_size;
  size_t count;
} is_hash_table_t;

is_hash_table_t *new_hash_table(size_t size);
void destroy_hash_table(is_hash_table_t *table);
uint32_t hash_vector(float *vec, int dim);
is_ll_t *insert(is_hash_table_t *table, image_source_t is, int dim);
void print_hash_table(is_hash_table_t *table, int dim);

#endif
