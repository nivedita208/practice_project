## what is pluck
“In Frappe, pluck is an argument we can use with frappe.get_all() or frappe.get_list() when we only need a single field’s values as a flat list.
Without pluck, these functions return a list of dictionaries, which would require extra steps to extract the values.
pluck saves time and makes the code cleaner when we just need one field.”

`Example to show`:
```python
# Without pluck
records = frappe.get_all("Estimation", filters={"opportunity": "OPP-001"}, fields=["name"])
# records = [{'name': 'EST-001'}, {'name': 'EST-002'}]
names = [r['name'] for r in records]  # extra step needed

# With pluck
names = frappe.get_all("Estimation", filters={"opportunity": "OPP-001"}, pluck="name")
# names = ['EST-001', 'EST-002']  # direct flat list
```