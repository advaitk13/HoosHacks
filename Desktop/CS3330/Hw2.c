/* do not remove these definitions or replace them #includes */
#define NULL 0
typedef long size_t;
void *malloc(size_t size);
void *realloc(void *ptr, size_t size);
void *calloc(size_t nitems, size_t size);
void free(void* ptr);
int printf(const char *format, ...);

/* The following #ifdef and its contents need to remain as-is. */
#ifndef TYPE
#define TYPE short
TYPE sentinel = -1234;
#else
extern TYPE sentinel;
#endif

/* typedefs needed for this task: */
typedef struct node_t 
{ 
  TYPE payload; 
  struct node_t *next; 
} node;
typedef struct range_t 
{ 
  unsigned int length; 
  TYPE *ptr; 
} range;

int lengthOf(range list) 
{
    return list.length;
}
int lengthOfNode(node *list) 
{
    int i=0; 
    while(list) 
    	{ 
    		list = (*list).next; i+=1; 
    	} 
    return i;
}
node *convert(range list) /* from range to linked list */
{
	int i;
  	node* head;
  	node* a;
  	node* ptr = NULL;
  	if(lengthOf(list) != 0)
      {
      	for(i = 0; i < lengthOf(list); i += 1)
    	{
        	node* temp = malloc(sizeof(node));
      		if(i == 0)
              {
              	temp->payload = list.ptr[i];
              	head = temp;
                a = temp;
			  }
      		else
              {
              	temp->payload = list.ptr[i];
              	a->next = temp;
      			a = temp;
              }
   	 	}
        	a->next = NULL;
        	return head;
    }
  	return ptr;
}
void append(node **dest, node *source) /* append linked list to linked list */
{
  if (source == NULL) {
    return;
  }
  
  node *last = *dest;
  while (last != NULL && last->next != NULL) {
    last = last->next;
  }
  if (last == NULL) {
    *dest = malloc(sizeof(node));
    last = *dest;
    last->payload = source->payload;
    source = source->next;
  }
  while (source != NULL) {
    last->next = malloc(sizeof(node));
    last->next->payload = source->payload;
    last = last->next;
    last->next = NULL;
    source = source->next;
  }
 }
void remove_if_equal(node **dest, TYPE value) 
{
   node *curr = *dest;
   node *prev = *dest; // maybe start prev = NULL ??

   int size = lengthOfNode(*dest);
   if(size != 0)
   {
     int x;
	for(x =0;x<size;x++)
     {
       if((curr)->payload == value && curr == prev)
         {
            node *remove = (*dest);
         	curr = curr->next;
            prev = curr;
         	*dest = (*dest)->next;
         	free(remove);
       	 }
       else if ((curr)->payload == value)
         {
            node *remove = curr;
         	if(curr->next != NULL)
            {
              prev->next = curr->next;
              curr = curr->next;
            }
         	else
            {
              prev->next = NULL;
              curr = NULL;
            }
            free(remove);
         }
      else
        {
        curr = curr->next;
      	}
      }
     }
  }
 /* curr->next= NULL;*/

