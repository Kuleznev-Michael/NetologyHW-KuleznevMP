import json

dict = {}
with open('purchase_log.txt') as purchase_log:
    for i, row in enumerate(purchase_log):
        row = json.loads(row)
        key = row["user_id"]
        value = row["category"]
        dict[key] = value
with open('visit_log__1_.csv', 'r') as visit_log, open("funnel.csv","w") as funnel:
    for i, row in enumerate(visit_log):
        row = row.strip().split(',')
        if row[0] in dict.keys():
            row.append(dict[row[0]])
            add_row = ",".join(row)
            funnel.write(f"{add_row}\n")