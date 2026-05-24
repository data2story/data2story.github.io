"""Analyze 2019.csv: gender, genre, spoken split."""
import pandas as pd
import os

DATA_DIR = "/Users/forrest/Desktop/data2blog/data_preprint/pudding/06_register/data"

y2019 = pd.read_csv(os.path.join(DATA_DIR, "2019.csv"))

# --- ana_2019_gender: register by gender in 2019 ---
print("=== ana_2019_gender ===")
print("rows:", len(y2019))
print("gender counts:")
print(y2019['gender'].value_counts())
print("register by gender:")
print(y2019.groupby('gender')['register'].agg(['count','mean','median','std','min','max']).round(3))

# --- ana_2019_genre: register by genre in 2019 ---
print("=== ana_2019_genre ===")
# normalize duplicate "no genreno genre"
y2019['genre_clean'] = y2019['genre'].replace({'no genreno genre':'no genre'}).fillna('no genre')
print("genre counts after cleaning:")
print(y2019['genre_clean'].value_counts())
print("register by genre (all):")
print(y2019.groupby('genre_clean')['register'].agg(['count','mean','median','std','min','max']).round(3).sort_values('mean', ascending=False))

# --- ana_2019_spoken: spoken-vocals share and effect ---
# spoken column appears to be 0-10 scale (degree of rapped delivery)
print("=== ana_2019_spoken ===")
print("spoken value counts:")
print(y2019['spoken'].value_counts(dropna=False).sort_index())
# Bucket
y2019['spoken_bucket'] = pd.cut(y2019['spoken'], bins=[-1,0,4,7,10],
                                 labels=['sung (0)','mostly sung (1-4)','mixed (5-7)','rapped (8-10)'])
print("register by spoken bucket:")
print(y2019.groupby('spoken_bucket', observed=False)['register'].agg(['count','mean','median']).round(3))

# --- ana_2019_male_subset: register among male leads (excluding spoken-rap >=8) ---
print("=== ana_2019_male_subset ===")
male_sung = y2019[(y2019['gender']=='male') & (y2019['spoken']<8)]
print("n male, mostly-sung:", len(male_sung))
print("mean register:", round(male_sung['register'].mean(), 3))
print("median:", male_sung['register'].median())
print("Distribution:")
print(male_sung['register'].value_counts().sort_index())
# Compare to female
female = y2019[y2019['gender']=='female']
print("n female:", len(female))
print("female mean register:", round(female['register'].mean(), 3))

# --- ana_2019_high_register: distribution of high-register songs ---
print("=== ana_2019_high_register ===")
hi = y2019[y2019['register'] >= 8]
print(f"songs with register >= 8: {len(hi)} / {len(y2019)} = {len(hi)/len(y2019)*100:.1f}%")
print("by gender:")
print(hi['gender'].value_counts())
print("by genre:")
print(hi['genre_clean'].value_counts())
# Among male-led non-rap (sung pop/rock/etc)
male_pop_sung = y2019[(y2019['gender']=='male') & (y2019['spoken']<5)]
hi_male_sung = male_pop_sung[male_pop_sung['register']>=8]
print(f"male sung songs: {len(male_pop_sung)}, of which register>=8: {len(hi_male_sung)} ({len(hi_male_sung)/max(len(male_pop_sung),1)*100:.1f}%)")

# --- ana_2019_genre_dist: stacked-bar-friendly table of genre x register ---
print("=== ana_2019_genre_dist ===")
ct = pd.crosstab(y2019['genre_clean'], y2019['register'])
print("counts (genre x register):")
print(ct)

# --- ana_2019_rap_register: how rap reduces register ---
print("=== ana_2019_rap_register ===")
print("Rap/Hip hop register histogram:")
rap = y2019[y2019['genre_clean']=='Rap/Hip hop']
print(rap['register'].value_counts().sort_index())
print("Rap mean:", round(rap['register'].mean(),3))
print("Non-rap mean:", round(y2019[y2019['genre_clean']!='Rap/Hip hop']['register'].mean(),3))
