"Merge acute and followup data for StopCOVID Russia"

import pandas as pd

# these three files are part of the acute patient dataset
part1_dates = pd.read_csv("CVMEWUS_Part1-Dates-07.08.20.csv", dtype=str)
part2_dates = pd.read_csv("CVMEWUS_Part2-Dates-07.08.20_utf.csv", dtype=str)
part2_dates.rename(columns={"PIN": "subjid"}, inplace=True)
sympt_comorb = pd.read_csv(
    "CVMEWUS_Sympt-Comorb-CheckedPIN-IDDO-28.07.20UTF-8.csv", dtype=str
)

# merged followup dataset
followup = pd.read_csv("../stopcovid-russia.csv", dtype=str)

output = "../stopcovid-russia-with-acute.csv"

# only add acute patients who are not in followup
acute_not_in_followup_ids = (
    set(part1_dates.subjid) | set(part2_dates.subjid) | set(sympt_comorb.subjid)
) - set(followup.subjid)

part1_dates = part1_dates[part1_dates.subjid.isin(acute_not_in_followup_ids)]
part2_dates = part2_dates[part2_dates.subjid.isin(acute_not_in_followup_ids)]
sympt_comorb = sympt_comorb[sympt_comorb.subjid.isin(acute_not_in_followup_ids)]

# ensure no common patients between acute and followup
assert not (acute_not_in_followup_ids & set(followup.subjid))

merged_acute = part1_dates.merge(part2_dates, "outer", "subjid").merge(
    sympt_comorb, "outer", "subjid"
)

# use .concat() instead of .merge() as merge creates _x and _y columns
# for columns that are named the same in both
merge = pd.concat((merged_acute, followup), axis=0, ignore_index=True)
merge.to_csv(output, index=False)
print(output)
