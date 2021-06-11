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

/*
LIST_HEAD_INIT(lh);

int main()
{
    struct list_head *lstub;
    struct mm_node mm1 = {.ttl = 3};
    list_add_tail(&mm1.list, &lh);
    lstub = &mm1.list;

    printf("%d\n", container_of(lstub, struct mm_node, list)->ttl);

    list_ttl_del(&mm1.list, &lh);
    printf("%d\n", container_of(lstub, struct mm_node, list)->ttl);
    printf("%s\n", list_empty(&lh) ? "YES" : "NO");

    list_ttl_del(&mm1.list, &lh);
    printf("%d\n", container_of(lstub, struct mm_node, list)->ttl);
    printf("%s\n", list_empty(&lh) ? "YES" : "NO");

    list_ttl_del(&mm1.list, &lh);
    printf("%d\n", container_of(lstub, struct mm_node, list)->ttl);
    printf("%s\n", list_empty(&lh) ? "YES" : "NO");

    list_for_each(lstub, &lh) {
        printf("%d\n", container_of(lstub, struct mm_node, list)->ttl);
    }
}
*/
