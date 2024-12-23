from ete3 import Tree, TreeStyle, TextFace

# Вложенный словарь
nested_dicts = {'Home': {
    'A': {'B': {'C': {}, 'D': {}}, 'E': {}},
    'F': {'G': {'H': {}}}
}}

ts = TreeStyle()
ts.show_branch_length = False  # Disable branch length display
ts.show_branch_support = False  # Disable branch support display (if any)
ts.show_scale = False
ts.mode = "r"  # for rectangular layout

tree = Tree(format=1)
tree.name = list(nested_dicts.keys())[0]

root = tree
# root = tree.add_child(name=list(nested_dicts.keys())[0])


root.add_child(name="Child1")
root.add_child(name="Child2")


for n in tree.traverse():
    if not n.is_leaf():
        n.add_face(TextFace(n.name + "\nХух"), column=0)
print(tree)

tree.render("render.png", tree_style=ts)

# import ete3

# #t = ete3.Tree("(A,B,(C,D)E)F;", format=8)
# t = ete3.Tree("(A:0.1,B:0.2,(C:0.3,D:0.4)E:0.5)F;", format=1)

# ts = ete3.TreeStyle()
# #ts.show_leaf_name = True

# lstyle = ete3.NodeStyle()
# lstyle["fgcolor"] = "blue"
# lstyle["size"] = 1.5

# nstyle = ete3.NodeStyle()
# nstyle["fgcolor"] = "red"
# nstyle["size"] = 3

# for n in t.traverse():
#     #print(n.name, n.is_leaf())
#     if n.is_leaf():
#         n.set_style(lstyle)
#     else:
#         n.add_face(ete3.TextFace(n.name), column=0)
#         n.set_style(nstyle)

# # all of these are optional
# ts.branch_vertical_margin = 10
# ts.mode = "c"
# ts.arc_start = -70 # 0 degrees = 15:00 o'clock
# ts.arc_span = 170

# # note that it save the file to the current folder
# t.render("./tree.png", w=1920, units="px", tree_style=ts)
# #t.show()