/*
 * clings exercise: 16_data_structures/02_binary_search_tree
 * title: Binary search tree
 * objective: Insert into and search a binary search tree.
 * hint: Smaller values go left; larger values go right.
 */

#include "clings/test.h"

#include <stddef.h>
#include <stdlib.h>

struct node {
    int value;
    struct node *left;
    struct node *right;
};

struct node *insert(struct node *root, int value)
{
    if (root == NULL) {
        struct node *node = malloc(sizeof *node);
        if (node == NULL) {
            return NULL;
        }
        node->value = value;
        node->left = NULL;
        node->right = NULL;
        return node;
    }
    if (value < root->value) {
        root->left = insert(root->left, value);
    } else if (value > root->value) {
        /* TODO: larger values go to the right subtree. */
        root->left = insert(root->left, value);
    }
    return root;
}

int contains(const struct node *root, int value)
{
    if (root == NULL) {
        return 0;
    }
    if (value < root->value) {
        return contains(root->left, value);
    }
    if (value > root->value) {
        return contains(root->right, value);
    }
    return 1;
}

void free_tree(struct node *root)
{
    if (root == NULL) {
        return;
    }
    free_tree(root->left);
    free_tree(root->right);
    free(root);
}

int main(void)
{
    struct node *root = NULL;

    root = insert(root, 5);
    root = insert(root, 3);
    root = insert(root, 7);
    CLINGS_CHECK_INT(contains(root, 5), 1);
    CLINGS_CHECK_INT(contains(root, 3), 1);
    CLINGS_CHECK_INT(contains(root, 7), 1);
    CLINGS_CHECK_INT(contains(root, 4), 0);
    free_tree(root);
    return clings_report();
}
