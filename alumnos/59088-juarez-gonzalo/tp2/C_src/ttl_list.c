#include "list.c"

struct mm_node {
    char *mm;
    unsigned int ttl;
    struct list_head list;
};

static inline void list_ttl_del(struct list_head *rm, struct list_head *headp)
{
    struct mm_node *p;

    if (rm == headp)
        return;

    p = container_of(rm, struct mm_node, list);
    p->ttl--;

    if (p->ttl == 0)
        list_del(rm);
}
