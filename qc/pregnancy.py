"Pregnancy related checks"

from adtl.qc import rule, rules_for
import pandas as pd


@rule(columns=["sex", "sex_at_birth", "pregnancy"])
def rule_male_patients_not_pregnant(df: pd.DataFrame) -> pd.Series:
    "Male patients are not pregnant"
    return (
        (df.sex == "female")
        | (df.sex_at_birth == "female")
        | (((df.sex_at_birth == "male") | (df.sex == "male")) & df.pregnancy != True)
        | (df.sex.isnull() & df.sex_at_birth.isnull())
    )


rules_for("*-subject.csv", rule_male_patients_not_pregnant)
