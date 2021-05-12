"""
File: linkedbst.py
Author: Ken Lambert
"""

from os import link
from abstractcollection import AbstractCollection
from bstnode import BSTNode
from linkedstack import LinkedStack
import random
import sys
from time import time
from math import log


class LinkedBST(AbstractCollection):
    """An link-based binary search tree implementation."""

    def __init__(self, sourceCollection=None):
        """Sets the initial state of self, which includes the
        contents of sourceCollection, if it's present."""
        self._root = None
        AbstractCollection.__init__(self, sourceCollection)

    # Accessor methods
    def __str__(self):
        """Returns a string representation with the tree rotated
        90 degrees counterclockwise."""

        def recurse(node, level):
            string = ""
            if node != None:
                string += recurse(node.right, level + 1)
                string += "| " * level
                string += str(node.data) + "\n"
                string += recurse(node.left, level + 1)
            return string

        return recurse(self._root, 0)

    def __iter__(self):
        """Supports a preorder traversal on a view of self."""
        if not self.isEmpty():
            stack = LinkedStack()
            stack.push(self._root)
            while not stack.isEmpty():
                node = stack.pop()
                yield node.data
                if node.right != None:
                    stack.push(node.right)
                if node.left != None:
                    stack.push(node.left)

    def preorder(self):
        """Supports a preorder traversal on a view of self."""
        return None

    def inorder(self):
        """Supports an inorder traversal on a view of self."""
        lyst = list()

        def recurse(node):
            if node != None:
                recurse(node.left)
                lyst.append(node.data)
                recurse(node.right)

        recurse(self._root)
        return iter(lyst)

    def postorder(self):
        """Supports a postorder traversal on a view of self."""
        return None

    def levelorder(self):
        """Supports a levelorder traversal on a view of self."""
        return None

    def __contains__(self, item):
        """Returns True if target is found or False otherwise."""
        return self.find(item) != None

    def find(self, item):
        """If item matches an item in self, returns the
        matched item, or None otherwise."""

        def recurse(node):
            if node is None:
                return None
            elif item == node.data:
                return node.data
            elif item < node.data:
                return recurse(node.left)
            else:
                return recurse(node.right)

        return recurse(self._root)

    # Mutator methods
    def clear(self):
        """Makes self become empty."""
        self._root = None
        self._size = 0

    def add(self, item):
        """Adds item to the tree."""
        if self._root is not None:
            cur_node = self._root

            while True:

                if cur_node.data <= item:
                    if cur_node.right is not None:
                        cur_node = cur_node.right

                    else:
                        cur_node.right = BSTNode(item)
                        break

                else:
                    if cur_node.left is not None:
                        cur_node = cur_node.left

                    else:
                        cur_node.left = BSTNode(item)
                        break
        else:
            self._root = BSTNode(item)
        self._size += 1

    def remove(self, item):
        """Precondition: item is in self.
        Raises: KeyError if item is not in self.
        postcondition: item is removed from self."""
        if not item in self:
            raise KeyError("Item not in tree.""")

        # Helper function to adjust placement of an item
        def lift_max_in_left_subtree_to_top(top):
            # Replace top's datum with the maximum datum in the left subtree
            # Pre:  top has a left child
            # Post: the maximum node in top's left subtree
            #       has been removed
            # Post: top.data = maximum value in top's left subtree
            parent = top
            current_node = top.left
            while not current_node.right == None:
                parent = current_node
                current_node = current_node.right
            top.data = current_node.data
            if parent == top:
                top.left = current_node.left
            else:
                parent.right = current_node.left

        # Begin main part of the method
        if self.isEmpty(): return None

        # Attempt to locate the node containing the item
        item_removed = None
        pre_root = BSTNode(None)
        pre_root.left = self._root
        parent = pre_root
        direction = 'L'
        current_node = self._root
        while not current_node == None:
            if current_node.data == item:
                item_removed = current_node.data
                break
            parent = current_node
            if current_node.data > item:
                direction = 'L'
                current_node = current_node.left
            else:
                direction = 'R'
                current_node = current_node.right

        # Return None if the item is absent
        if item_removed == None: return None

        # The item is present, so remove its node

        # Case 1: The node has a left and a right child
        #         Replace the node's value with the maximum value in the
        #         left subtree
        #         Delete the maximium node in the left subtree
        if not current_node.left == None \
                and not current_node.right == None:
            lift_max_in_left_subtree_to_top(current_node)
        else:

            # Case 2: The node has no left child
            if current_node.left == None:
                new_child = current_node.right

                # Case 3: The node has no right child
            else:
                new_child = current_node.left

                # Case 2 & 3: Tie the parent to the new child
            if direction == 'L':
                parent.left = new_child
            else:
                parent.right = new_child

        # All cases: Reset the root (if it hasn't changed no harm done)
        #            Decrement the collection's size counter
        #            Return the item
        self._size -= 1
        if self.isEmpty():
            self._root = None
        else:
            self._root = pre_root.left
        return item_removed

    def replace(self, item, new_item):
        """
        If item is in self, replaces it with new_item and
        returns the old item, or returns None otherwise."""
        probe = self._root
        while probe != None:
            if probe.data == item:
                old_data = probe.data
                probe.data = new_item
                return old_data
            elif probe.data > item:
                probe = probe.left
            else:
                probe = probe.right
        return None

    def height(self):
        '''
        Return the height of tree
        :return: int
        '''

        def height1(top):
            '''
            Helper function
            :param top:
            :return:
            '''
            if top == None:
                return 0

            else:
                left_height = height1(top.left)
                right_height = height1(top.right)
                return 1 + max(left_height, right_height)

        next_root = self._root
        return height1(next_root) - 1

    def is_balanced(self):
        '''
        Return True if tree is balanced
        :return:
        '''
        lyst = list()

        def recurse(node):
            if node != None:
                recurse(node.left)
                lyst.append(node.data)
                recurse(node.right)

        recurse(self._root)
        length = len(lyst)

        return self.height() < 2 * log(length + 1, 2) - 1

    def range_find(self, low, high):
        '''
        Returns a list of the items in the tree, where low <= item <= high."""
        :param low:
        :param high:
        :return:
        '''
        min_item = self.successor(low, strict=True)
        max_item = self.predecessor(high, strict=True)

        lst = [x for x in self.inorder()]

        min_idx = lst.index(min_item)
        max_idx = lst.index(max_item)

        return lst[min_idx : max_idx+1]

    def rebalance(self):
        '''
        Rebalances the tree.
        :return:
        '''
        lyst = list()

        def recurse(node):
            if node != None:
                recurse(node.left)
                lyst.append(node.data)
                recurse(node.right)

        recurse(self._root)
        self.clear()
        linked_bst = sorted(lyst)

        def recurse_2(linked_bst):
            """
            Extra method.
            """

            if len(linked_bst) != 0:
                mid = len(linked_bst) // 2
                return BSTNode(linked_bst[mid], recurse_2(linked_bst[:mid]), recurse_2(linked_bst[mid + 1:]))

            return None

        self._root = recurse_2(linked_bst)
        return None


    def successor(self, item, strict = False):
        """
        Returns the smallest item that is larger than
        item, or None if there is no such item.
        :param item:
        :type item:
        :return:
        :rtype:
        """
        lst = [x for x in self.inorder()]

        prev = None

        for elem in sorted(lst, reverse=True):

            if strict:
                if elem <  item:
                    break

            elif elem <= item:
                break

            prev = elem

        return prev

    def predecessor(self, item, strict = False):
        """
        Returns the largest item that is smaller than
        item, or None if there is no such item.
        :param item:
        :type item:
        :return:
        :rtype:
        """
        lst = [x for x in self.inorder()]

        prev = None

        for elem in lst:

            if strict:
                if elem >  item:
                    break

            elif elem >= item:
                break

            prev = elem

        return prev

    def demo_bst(self, path):
        """
        Demonstration of efficiency binary search tree for the search tasks.
        :param path:
        :type path:
        :return:
        :rtype:
        """
        words = []

        with open(path, 'r', encoding='utf-8') as f_words:
            for word in f_words:
                words.append(word.strip())

        f_words.close()
        sample = random.sample(words, 10000)
        start_time = time()

        for word in sample:
            words.index(word)

        next_time = time()
        print("час пошуку 10000 випадкових слів у впорядкованому за абеткою\
 словнику = {}".format(next_time - start_time))
        linked_bst_2 = LinkedBST()

        for word in words:
            linked_bst_2.add(word)

        start_time = time()

        for word in sample:
            linked_bst_2.find(word)

        mext_time = time()
        print("час пошуку 10000 випадкових слів у словнику, який представлений у вигляді\
 бінарного дерева пошуку = {}".format(next_time - start_time))
        random.shuffle(words)
        linked_bst_1 = LinkedBST()

        for word in words:
            linked_bst_1.add(word)

        start_time = time()

        for word in sample:
            linked_bst_1.find(word)

        mext_time = time()
        print("час пошуку 10000 випадкових слів у словнику, який представлений у вигляді\
 бінарного дерева пошуку. Бінарне дерево пошуку будується на основі послідовного додавання\
 в дерево слів зі словника який не впорядкований за абеткою = {}".format(next_time - start_time))
        linked_bst_1.rebalance()
        start_time = time()

        for word in sample:
            linked_bst_1.find(word)

        mext_time = time()
        print("час пошуку 10000 випадкових слів у словнику, який представлений у вигляді\
 бінарного дерева пошуку після його балансування = {}".format(next_time - start_time))


if __name__ == '__main__':
    sys.setrecursionlimit(5000000)
    linked_bst_demo = LinkedBST()
    linked_bst_demo.demo_bst('words.txt')
