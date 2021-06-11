#include "list.c"

struct mm_node {
    char *mm;
    unsigned int ttl;
    struct list_head list;
};

static inline void list_ttl_del(struct mm_node *rm, struct list_head *headp)
{
    if (&rm->list == headp)
        return;
    rm->ttl--;
    if (rm->ttl == 0)
        list_del(&rm->list);
}
