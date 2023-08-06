
#include <stdlib.h>
#include <stdio.h>
#include <stdint.h>

#include "hash_table.h"

/*
 * This file implements a hash table for vectors in 2D or 3D
 *
 * We define collisions to within eps.
 * This means that a vector that is close to the borders between
 * to different bins needs to be added to both. We handle collisions
 * with linked lists, and add the element to both bins if necessary.
 * We keep track of the number reference to object
 */

/* 
 * Union used to cast a float to an unsigned int and extract the
 * most significant bits of the mantissa as a key
 */
typedef union
{
  float f;
  struct {
    unsigned int mantisa : 23;
    unsigned int exponent : 8;
    unsigned int sign : 1;
  } parts;
  struct {
    unsigned int discarded : 15;
    unsigned int key : 8;
    unsigned int discarded2 : 9;
  } hash;
}
float_cast;

/* 
 * we handle collisions with a linked list 
 *
 * We handle epsilon close values by adding one value to neighboring bins
 * if then are closer than epsilon
 */
typedef struct hash_element
{
  float vec[3];
  is_ll_t *image_source;
  unsigned int num_ref;
  sturct hash_element *next;
}
hash_element_t;

/*
 * A hash table
 *
 * bins is the array of linked lists
 * size is the number of bins in the array
 * count is the number of elements in the hash table
 * dim is the length of the vectors to store (2 or 3)
 * eps is the precision for collisions
 */
typedef struct
{
  hash_element_t **bins;
  size_t size;
  size_t count;
  size_t dim;
  float eps;
}
hash_table_t;

hash_table_t *new_hash_table(size_t size, size_t dim, float eps)
{
  // malloc data structure
  hash_table_t *table = (hash_table_t *)malloc(sizeof(hash_table_t));

  // malloc hash table itself
  table->bins = (hash_element_t **)malloc(size*sizeof(hash_element_t *));
  table->size = size;
  table->dim = dim;
  table->eps = eps;

  // initialize
  for (int i = 0 ; i < table->size ; i++)
    table->bins[i] = NULL;

  // contains no element
  table->count = 0;

  return table;
}

void destroy_hash_table(is_hash_table_t *table)
{
  // Delete all the linked lists
  for (int i = 0 ; i < table->size ; i++)
    is_list_delete(&table->bins[i]);

  // free the table array
  free(table->bins);

  // then free the table
  free(table);

}

uint32_t hash_vector(float *vec, int dim)
{
  // This function hashes 2 or 3 floating point values 
  // into an unsigned 32 bit key
  float_cast cell;
  uint32_t key = 0;
  int i;
  int shift_left, shift_right;

  /*
   * In 2D, we use the 16 most significant bits of the mantissa
   * In 3D, we use 11/11/10 most significant bits of the mantissa
   */

  if (dim == 2)
  {
    shift_right = 7;
    shift_left = 16;
  }
  else if (dim == 3)
  {
    shift_right = 12;
    shift_left = 11;
  }

  // We can take care of dim 1 and 2 in a loop
  for (i = 0 ; i < 2 ; i++)
  {
    // evil byte hacking
    cell.f = vec[i];
    key |= (cell.parts.mantissa >> shift) << (i * shift_left);
  }

  // handle separately the 3rd coordinate in 3D because of diff number of bits
  if (dim == 3)
  {
    cell.f = vec[2];
    key |= (cell.parts.mantissa >> 13) << (2 * shift_left);
  }

  return key;
}

// Insert a new IS in the hash table
// returns NULL if the location was already in the table
is_ll_t *insert(is_hash_table_t *table, image_source_t is, int dim)
{
  // compute location in hash table
  uint32_t key = hash_vector(is.loc, dim) % table->table_size;
  is_ll_t *e = table->table[key];

  // run down the linked list to find the node
  while (e != NULL)
  {
    // If the vector exists in the list, do not insert
    if (distance(is.loc, e->is.loc, dim) < eps)
      return NULL;

    e = e->next;
  }

  // If the vector is not in the list, create it
  is_ll_t *new = (is_ll_t *)malloc(sizeof(is_ll_t));
  new->is = is;
  new->visible_mics = NULL;
  new->next = NULL;

  printf("Insert new is at key=%d head=%p new=%p new->next=%p\n", key, table->table[key], new, new->next);

  // insert in the list
  is_list_insert(table->table + key, new);

  // increase the table count
  table->count++;

  return new;
}

void print_hash_table(is_hash_table_t *table, int dim)
{
  int i;
  for (i = 0 ; i < table->table_size ; i++)
  {
    is_ll_t *e = table->table[i];
    while (e != NULL)
    {
      print_vec(e->is.loc, dim);
      e = e->next;
    }
  }
}

