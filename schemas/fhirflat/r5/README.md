# FHIRFlat schemas

This specifies deviations in FHIRFlat from the FHIR r5 specification.

Attributes marked with (PII) were removed due to having personally identifiable information

## Patient

Dropped attributes:

* `identifier` - We use `id`, `identifier` can store other identifiers for a Patient
* `active` - Whether this patient's record is in active use, not required by us
* `name` - patient name (PII)
* `telecom` - contact details of patient (PII)
* `address` - address details of patient (PII)
* `photo` - photo of patient (PII)
* `contact` - contact party for the patient (PII)
* `communication` - language which may be used to communicate with the patient about his or her health
* `link` - link to a patient that concerns the same actual individual

Changed attributes:

* `gender` - we do not store the terminology URL as the ValueSet is unlikely to change
* `maritalStatus` - codeable concepts merge terminology URL and the code
