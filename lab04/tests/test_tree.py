from algorithms import TreeNode, inorder, postorder, preorder


def test_tree_traversals() -> None:
    tree = TreeNode(
        val=4,
        left=TreeNode(val=2, left=TreeNode(1), right=TreeNode(3)),
        right=TreeNode(val=6, left=TreeNode(5), right=TreeNode(7)),
    )
    assert preorder(tree) == [4, 2, 1, 3, 6, 5, 7]
    assert inorder(tree) == [1, 2, 3, 4, 5, 6, 7]
    assert postorder(tree) == [1, 3, 2, 5, 7, 6, 4]


def test_empty_tree() -> None:
    assert preorder(None) == []
    assert inorder(None) == []
    assert postorder(None) == []
