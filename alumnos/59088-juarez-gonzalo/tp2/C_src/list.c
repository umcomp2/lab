/*
 * yup, this is a ruthless copy of the linux kernel implementation of a doubly linked list.
 * what can i say, it's the best one i've seen...
 */

#define container_of(ptr, type, member) ({				\
		(type *)((char *)ptr - offset_of(type, member)); })

#define offset_of(type, member)				    		\
	((unsigned int)&((type *)0)->member)

struct list_head {
	struct list_head *next;
	struct list_head *prev;
};

#define LIST_HEAD_INIT(name)				    		\
	struct list_head name = { &(name), &(name) }

static inline void INIT_HEAD_LIST(struct list_head *headp)
{
    headp->next = headp;
    headp->prev = headp;
}

static inline void __list_add(struct list_head *new, struct list_head *prev, struct list_head *next)
{
	new->prev = prev;
	prev->next = new;
	new->next = next;
	next->prev = new;
}

static inline void list_add(struct list_head *new, struct list_head *headp)
{
	__list_add(new, headp, headp->next);
}

static inline void list_add_tail(struct list_head *new, struct list_head *headp)
{
	__list_add(new, headp->prev, headp);
}

/* notice it does not remove the allocated space to the "deleted" node, it just unlinks it from the list (dlmalloc pun intended) */
static inline void __list_del(struct list_head *prev, struct list_head *next)
{
	prev->next = next;
	next->prev = prev;
}

static inline void list_del(struct list_head *rm)
{
	__list_del(rm->prev, rm->next);
}

static inline void list_del_tail(struct list_head *headp)
{
	list_del(headp->prev);
}

static inline struct list_head *singly_next_safe(struct list_head *curr, struct list_head *headp)
{
    struct list_head *next = 0;
    if (curr->next != headp)
        next = curr->next;
    return next;
}

/*
 * Macros for queue over already implemented functions/macros.
 * @new:	a pointer to list_head struct to enqueue
 * @headp:	a pointer to the head of the linked list
 */

#define list_enqueue(new, headp)				\
	list_add_tail(new, headp);				    \

#define list_dequeue(headp) ({					\
		list_empty(headp) ?		        		\
		NULL :						            \
		({						                \
		struct list_head *__dq = (headp)->next;	\
		list_del((headp)->next);			    \
		__dq;						            \
		});						                \
	})

static inline int list_empty(struct list_head *headp)
{
	return (headp->next == headp);
}

/*
 * @ptr:	a pointer used as cursor through the list
 * @headp:	a pointer to the head of the linked list
 */
#define list_for_each(ptr, headp) \
	for (ptr = (headp)->next; ptr != (headp); ptr = ptr->next)
