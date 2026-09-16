/*
 * clings exercise: 09_dynamic_memory/07_linked_list
 * title: A singly linked list
 * objective: Build, traverse, and free a linked list.
 * hint: The new node must point at the previous head.
 */

#include "clings/test.h"

#include <stdlib.h>
#include <stddef.h>

struct node {
    int value;
    struct node *next;
};

struct node *list_push(struct node *head, int value)
{
    struct node *node = malloc(sizeof *node);
    if (node == NULL) {
        return head;
    }
    node->value = value;
    node->next = head;
    return node;
}

size_t list_length(const struct node *head)
{
    size_t count = 0;
    for (const struct node *node = head; node != NULL; node = node->next) {
        ++count;
    }
    return count;
}

void list_free(struct node *head)
{
    while (head != NULL) {
        struct node *next = head->next;
        free(head);
        head = next;
    }
}

int main(void)
{
    struct node *head = NULL;

    head = list_push(head, 1);
    head = list_push(head, 2);
    head = list_push(head, 3);
    CLINGS_CHECK_INT(list_length(head), 3);
    CLINGS_CHECK_INT(head->value, 3);
    CLINGS_CHECK_INT(head->next->value, 2);
    list_free(head);
    return clings_report();
}
