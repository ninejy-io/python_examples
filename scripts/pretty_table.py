from prettytable import PrettyTable
# pip install prettytable

tabs = PrettyTable()

tabs.field_names = ["name", "age", "job"]
tabs.add_row(["Tom", 20, "IT"])
tabs.add_column("sex", ["male"])
tabs.add_row(["Lily", 19, "Teacher", "female"])

print tabs
