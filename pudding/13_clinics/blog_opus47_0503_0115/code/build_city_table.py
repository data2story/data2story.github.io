"""Build the slim city table that the map will draw — saved as a python dict so
we can paste it into analyst.json's data_table.rows."""
import pandas as pd, json

DATA = "/Users/forrest/Desktop/data2blog/data_preprint/pudding/13_clinics/cities.csv"
df = pd.read_csv(DATA)

# slim columns
cols = ['city','state','population','latitude','longitude',
        'gestation_8_duration','gestation_12_duration','gestation_16_duration','gestation_20_duration',
        'gestation_8_duration_closed','gestation_12_duration_closed','gestation_16_duration_closed','gestation_20_duration_closed']
slim = df[cols].copy()
# round lat/lng to 3 decimals for size; integers already
slim['latitude'] = slim['latitude'].round(3)
slim['longitude'] = slim['longitude'].round(3)
print(slim.head().to_dict(orient='records'))
print(f"total rows={len(slim)}")
# Print as a JSON-friendly list of rows
rows = slim.values.tolist()
print(f"first row: {rows[0]}")
print(f"json size approx: {len(json.dumps(rows))} chars")
# Dump to file for analyst use
with open('/Users/forrest/Desktop/data2blog/project/pudding/13_clinics/blog_opus47_0503_0115/code/city_table.json','w') as f:
    json.dump({"columns": cols, "rows": rows}, f)
print("wrote code/city_table.json")
