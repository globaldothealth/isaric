"""
Contains dictionary structures for standard formats

Dictionary structures which can be called to build up a parser file using a webapp interface.
"""


def predefined_value_maps(values: dict):
    return {"values": values}


def single_field(f, d):
    return {"field": f, "description": d}


# I'm not entirely sure if this will produce the correct nested key atm
# TODO: work out how to factor in anything other than '='
def conditional_field(f, d, condition, conditionals, values):
    rule = {"field": f, "description": d, condition: {}}

    if isinstance(conditionals, list):
        for c, v in zip(conditionals, values):
            rule[condition].update({c: v})
    else:
        rule[condition].update({conditionals: values})

    return rule


def field_with_unit(
    f: str, d: str, unit_f: str, source_unit_f: str, source_unit_v: dict
):
    return {
        "field": f,
        "description": d,
        "unit": unit_f,
        "source_unit": {"field": source_unit_f, "values": source_unit_v},
    }


def field_with_date(f: str, d: str, source_date_f: str):
    return {
        "field": f,
        "description": d,
        "date": "%d/%m/%Y",
        "source_date": source_date_f,
    }


def field_value_mapped(f: str, d: str, value_maps: dict | str):
    if isinstance(value_maps, dict):
        return {"field": f, "description": d, "values": value_maps}
    else:
        return {"field": f, "description": d, "ref": value_maps}


def field_with_transformation(f: str, d: str, func: str, params: list | None):
    rule = {"field": f, "description": d, "apply": {"function": func}}

    if params:
        rule["apply"]["params"] = params

    return rule


## Combined types


# look for ways to show the 4 options available for this.
def combined_type(rule: str, fields: list):
    return {"combinedType": rule, "fields": fields}


## Observations - get top bit working first.


# rest are optional - either make lots of seperate functions calling this one, or lots of **kwargs.
def observation_field(name, descrip, phase, date):
    pass
