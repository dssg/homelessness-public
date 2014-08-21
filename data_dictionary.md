# Data Dictionary


## Master.csv

Master.csv holds all data about a client’s demographics and basic program entry/exit information

Total number of unique clients: 151695 (ClientID), 131438 (ClientUniqueID)

### Duplication
No two rows should have the same EntryID, since it is a foreign key used in other tables.

*Note: The following information regarding Master.csv was recomputed using the set of July 2 CSVs Adam gave us on a flash drive. Information for other CSVs have not been updated.*

Total rows: 262806
Unique rows: 262783
Unaccounted-for rows: 23

### ClientUniqueID
An identifier based on the client's name and date of birth, later encrypted to hide any identifying information.

**NaNs:** 0 / 00%

### ClientID
An arbitrary identifier for each instance of a client in the system; you'll see this used as a foreign key in other tables

**NaNs:** 0 / 00%

### HouseholdID
All clients in a household will share the same HouseholdID. HouseholdID is independent of any program entry id.

**NaNs:** 165823 / 63%

### Head Of Household?
If client is in a household, Yes or No to answer whether or not client is head of household.

**NaNs:** 165825 / 63%

### Relationship to HoH
If client is in a household, relationship to the head of household. This field, like others, has multiple values that need to be collapsed.

**NaNs:** 168795 / 64%

### Entry Exit GroupID
All household clients in a single program entry will share this ID; you can use this to figure out if clients are grouped together in an entry. This is independent of the HouseholdID.

**NaNs:** 165819 / 63%

### EntryID
Each client gets her/his own EntryID when entering a program; you'll see this is a foreign key you see in other tables

**NaNs:** 0 / 00%

### ProviderID
The ID of the program in which the client is enrolled. There are 707 unique provider IDs.

**NaNs:** 0  / 00%

### ProgramEntryDate
The date the client entered the program. There are 1137 rows with ProgramEntryDate comes later compared with ProgramExitDate.

**NaNs:** 58611 / 22%

### ProgramExitDate
The date the client exited the program. Before ServicePoint was used (starting in 2008 or 2007), there was a different HMIS that might have used different default values. Missing values here means that a person could still be in the program. A missing value here could mean that the person is still in the program, or an entry error.

**NaNs:** 73529 / 28% , missing means the person could still be in the program (OR the user just never got around to exiting them. You can probably use the program type to figure out if the person should be exited or not: if it’s not a PSH program and it has been 5 years, it’s probably a mistake.

### YearOfBirth
The year the client was born. There are 7 entries in Master.csv that have years greater than 2014.

**NaNs:** 2672 / 01%

### Ethnicity
The client's ethnicity. However the values in this field indicate that it is really used to determine whether a client is Latino or Hispanic. The field name should be just Hispanic/Latino Or Not with values true, false, and null. This field, like others, has multiple values that need to be collapsed.

**NaNs:** 33935 / 13 %

See page 47 of the [HMIS Standards](https://www.onecpd.info/resources/documents/FinalHMISDataStandards_March2010.pdf).

### PrimaryRace
The client's race. This field, like others, has multiple values that need to be collapsed.

**NaNs:** 34568 / 13%

See page 46 of the [HMIS Standards](https://www.onecpd.info/resources/documents/FinalHMISDataStandards_March2010.pdf).

### SecondaryRace
This field, like others, has multiple values that need to be collapsed.

**NaNs:** 212674 / 81%

### PrimaryLanguageSpoken
This field, like others, has multiple values that need to be collapsed.

**NaNs:** 242341 / 92 %

### Veteran?
Yes/No question as to whether or not client is a military veteran

**NaNs:** 58611 / 22%

### PreviousLivingSituation
The living situation of the client on the night before s/he entered the program. This field, like others, has multiple values that need to be collapsed.

**NaNs:** 58611 / 22%

See page 52 of the [HMIS Standards](https://www.onecpd.info/resources/documents/FinalHMISDataStandards_March2010.pdf).

### LengthOfStayInPreviousLivingSituation
The amount of time the client spent in that PreviousLiving Situation.

**NaNs:** 58611 / 22%

There was a lot messy data here (17 different options) that need to be collapsed. There are text descriptions of upper and lower bounds on the amount of time. Possibly treat the 7 values as categorical variables.

### ZipCodeOfLastPermanentAddress
The postal code of the client's last permanent address

**NaNs:** 85128 / 32%

This column is very messy (like every column), with over 2500 unique values.

- Collapse NULL & Unknown & Default values (e.g., 0000, 9999, ?, ----) into NULL
- Collapse Zip Codes with dashes to ones without (e.g., 606-40 should be 60640 and 4 digit extensions should be collapsed as well)
- Validation of real zip codes (e.g., 00556 is not valid)

### ZipDataQuality
This indicates whether a zip code is fully recorded, partial, if the client didn't know it, if the client refused to give it

**NaNs:** 65598 / 24%

### DestinationAtExit
If the client exited, where s/he went immediately after. This field, like others, has multiple values that need to be collapsed.

**NaNs:** 101175 / 38%

See page 85 of the [HMIS Standards](https://www.onecpd.info/resources/documents/FinalHMISDataStandards_March2010.pdf).

**These permanent destinations should be flagged for future modeling purpose.** List of permanent destinations (selected from above).

TODO: confirm this with Adam & Lisa

- 3 = Permanent supportive housing for formerly homeless persons (such as SHP, S+C, or SRO
Mod Rehab)
- 10 = Rental by client, no ongoing housing subsidy
- 11 = Owned by client, no ongoing housing subsidy
- 19 = Rental by client, VASH Subsidy
- 20 = Rental by client, other (non-VASH) ongoing housing subsidy
- 21 = Owned by client, with ongoing housing subsidy:
- 22 = Staying or living with family, permanent tenure
- 23 = Staying or living with friends, permanent tenure

### ExitReason
The reason the client exited the program. This field, like others, has multiple values that need to be collapsed.

**NaNs:** 83885 / 32%

See page 104 of the [HMIS Standards](https://www.onecpd.info/resources/documents/FinalHMISDataStandards_March2010.pdf) and page 12 of 40118.

The below are values that we don’t know how to collapse yet:

- Services no longer needed-goals met 275
- RRH - Left Interim Housing Placement before assessment completed 15
- RRH - Not able to complete Assessment 3
- DFSS - Voluntary departure 1856
- Personal Choice/ Voluntary departure 5941
- Services request ended-w/ clinical agreement 41
- Involuntary discharge 65
- Services not offered 40
- Services request ended-unable to locate 49
- Long term leave-incarceration 16
- Long term leave-nursing facility 9
- Never engaged in services 49
- RRH - No contact in 30 days or more 37
- RRH - Not offered RRH Financial Assistance 81

Here’s the collapse:

- 1 = Left for a housing opportunity before completing program
	- Left for housing opp. before completing program
	- Left for a housing opportunity before completing program
- 2 = Completed program
	- Completed program
- 3 = Non-payment of rent/occupancy charge
	- Non-payment of rent
	- Non-payment of rent/occupancy charge
- 4 = Non-compliance with program
	- Non-compliance with project
	- Non-compliance with program
- 5 = Criminal activity/destruction of property/violence
	- Criminal activity / violence
	- criminal activity/violence
	- Non-Violent criminal activity
	- Destructive/Violent behavior
- 6 = Reached maximum time allowed by program
	- Reached maximum time allowed in project
	- Reached maximum time allowed
- 7 = Needs could not be met by program
	- Needs could not be met
	- Needs could not be met by project
- 8 = Disagreement with rules/persons
	- Disagreement with rules/persons
	- disagreement with rules/person
- 9 = Death
	- Deceased
	- Death
- 10 = Unknown/disappeared
	- Unknown/Disappeared
- 11 = Other
	- Other
	- Member moved-out of geographic area

### Anonymous

This is a field generated by Adam that was an attempt at identifying clients who were entered “anonymously” by a user. Everyone labeled as “Anonymous” was entered anonymously, but not everyone entered anonymously will be labeled as “Anonymous.” Several clients entered as anonymous will have the similar names and dates of birth, so the generated ClientUniqueID might be the same for a lot of anonymous clients, erroneously showing that a single ClientUniqueID went to dozens of different programs. There will be clients in the list entered that may not be labeled as Anonymous just due to the user using some other way to mask a client’s identity (e.g. entering the name as “Abc Abc”).

**NaNs:** 234445 / 89%

### DateCreated

**NaNs:** 0 / 00%

### DateUpdated

**NaNs:** 0 / 00%


## EntryDetails.csv

EntryDetails.csv contains basic information collected at entry

Total rows: 308078
Unique rows: 262787
Unaccounted-for rows: 45291

The Unaccounted-form rows are explained below in ClientID: they're all NaNs.

### ClientID
Identifier found in Master.csv

TODO: what's going on here.  Figure this out before moving forward with other diagnostics.

**NaNs:** 45292 / 15%

	entry_details[entry_details['ClientID'].apply(pd.isnull)]

### EntryID
Identifier found in Master.csv

### HousingStatusAtEntry
Literally Homeless, Imminently losing their housing, Stably housed, etc.

### Do you have a disability of long duration?
Yes/No answer

We should be able to interpolate & sanity-check these.

### Income received from any source in past 30 days?
Yes/No answer

We should be able to interpolate & sanity-check these.

### No cash benefit received in past 30 days?
Yes/No answer

We should be able to interpolate & sanity-check these.


## EntryIncome.csv

EntryIncome.csv contains the income data applicable when clients enter their programs

### Duplication
There should be no rows that are simultaneously duplicated on ClientID, EntryID, SourceOfIncome and StartDate.

Total rows: 82214
Unique rows: 81908
Unaccounted-for rows: 306

We should eventually check not only for the *same* start date, but *overlapping* date periods.

### ClientID
Identifier found in Master.csv

**NaNs:** 0 / 00%

### EntryID
Identifier found in Master.csv

**NaNs:** 0 / 00%

### SourceOfIncome
The source of the income for the client

**NaNs:** 4393 / 05%

Needs collapsing; see page 24 of 40118.

Sometimes entries are listed as "No Financial Resources (HUD)", but still list a Last30DayIncome.

### Last30DayIncome
How much income from this source was gained in the last 30 days

**NaNs:** 4561 / 06%

**0s:** 10062 / 12%

Sometimes entries are listed as "No Financial Resources (HUD)", but still list a Last30DayIncome.

We may wish to turn the Floats (e.g., 1024.4) to ints.

You can consider large numbers to be data entry errors. These should be monthly amounts that would keep the person most likely living at or around poverty, so making $1.2 million a year doesn’t really do that.

The poverty line threshold is below:

- $11,670 for individuals
- $15,730 for a family of 2
- $19,790 for a family of 3
- $23,850 for a family of 4
- $27,910 for a family of 5
- $31,970 for a family of 6
- $36,030 for a family of 7
- $40,090 for a family of 8

### StartDate
The day the client started to receive this income

**NaNs:** 0 / 00%

The start dates are often arbitrarily assigned and might just be added as the day before the client entered the program because s/he couldn’t remember when it actually started.

### EndDate
The last day the client received this income. If there is no end date, the client is still receiving the income OR the user hasn't updated the data.

**NaNs:** 64818 / 79%


# EntryNCB.csv

EntryNCB.csv has non-cash benefits (e.g. food stamps, MEDICAID) client has at time of program entry

100378 entries.

### Duplication
No two rows should have the same ClientID, EntryID, SourceOfNonCashBenefit, and StartDate.

Total rows: 100378
Unique rows: 100054
Unaccounted-for rows: 324

We should eventually check not only for the *same* start date, but *overlapping* date periods.

### ClientID
Identifier found in Master.csv

**NaNs:** 0 / 0%

### EntryID
Identifier found in Master.csv

**NaNs:** 0 / 0%

### SourceOfNonCashBenefit
The actual non-cash benefit the client has

**NaNs:** 1918 / 1%

See page 70 of the [HMIS Standards](https://www.onecpd.info/resources/documents/FinalHMISDataStandards_March2010.pdf).

18 types of SourceOfNonCashBenefit:

- Supplemental Nutrition Assistance Program (Food Stamps) (HUD)
- Special Supplemental Nutrition Program for WIC (HUD)
- MEDICAID (HUD)
- MEDICARE (HUD)
- Veteran's Administration (VA) Medical Services (HUD)
- SCHIP (HUD): State Children’s Health Insurance Program
- Section 8, Public Housing or rental assistance (HUD)
- Temporary rental assistance (HUD)
- TANF Child Care Services (HUD)
- TANF Transportation Services (HUD)
- Other TANF-Funded Services (HUD)
- Other Source (HUD)

The following are not in the HMIS data standards, and should be migrated to EntryIncome:

- Veteran 's Pension (HUD)
- TANF (HUD)
- SSDI (HUD): Social Security Disability Income
- SSI/P3
- Employment amount
- No Financial Resources (HUD)

### StartDate
The day the client started to receive this NCB

**NaNs:** 0 / 0%

Q: Is it a correct understanding that no person should receive the same NCB within overlapping time period? For example, could the same person receive Temporary rental assistance twice at overlapping time period? Could the same person receive Food Stamps twice at overlapping time period? Could the same person receive MEDICARE twice at overlapping time period? Could there possibly difference sub-types of MEDICARE?  Are there any differences among the different NCB types (e.g, some of them could be reasonably overlapped, some others cannot?)

A: If you see overlapping duplicates like that, it’s probably due to one person not seeing that another user had already entered that value (either due to data visibility restrictions or just laziness).  N.B. The start dates for NCBs are *often arbitrarily assigned* and might just be added as the day before the client entered the program because s/he couldn’t remember when it actually started.

### EndDate
The last day the client received this NCB

**NaNs:** 84090 / 83%

No rows with StartDate later than EndDate


## EntryDisabilities.csv

EntryDisabilities.csv has the disabling conditions with which clients are afflicted, identified at time of entry

### Duplication
There should be no rows that are simultaneously duplicated on ClientID, EntryID, DisabilityType and StartDate together.

Total rows: 72181
Unique rows: 71662
Unaccounted-for rows: 519

### ClientID
Identifier found in Master.csv

**NaNs:** 0 / 0%

### EntryID
Identifier found in Master.csv

**NaNs:** 0 / 0%

### DisabilityType
Actual disabling condition (e.g. Physical, Mental Health Problem, Alcohol Abuse)

**NaNs:** 1400 / 1%

HUD-defined (in 40118): 

- Mental Health Problem (HUD 40118)
- Alcohol Abuse (HUD 40118)
- Drug Abuse (HUD 40118)
- HIV/AIDS (HUD 40118)
- Developmental (HUD 40118)
- Physical (HUD 40118)

The following should be mapped:

- Both alcohol and drug abuse (HUD 40118): split into two entries
- Physical/Medical (HUD 40118): Physical (HUD 40118)
- Chronic Health Condition: Physical (HUD 40118)
- Dual Diagnosis:split into Mental Health & Drug Abuse
- Vision Impaired: Physical (HUD 40118)
- Hearing Impaired: Physical (HUD 40118)

### DisabilityDetermination
Yes/No response to if condition is legally a disability

**NaNs:** 18592 / 25%

### StartDate
Date disability was identified

**NaNs:** 0 / 0%

There are 4 rows in the future

For Disabilities, the Start Date should be the date the disability was identified, and the End Date should exist only if the person stopped suffering from the disability; if no end date, they still suffer from it.

### EndDate
Date disability no longer affecting client. If there is no end date, then this disability is still affecting the client.

**NaNs:** 61401 / 85%


## ExitStuff.csv

ExitStuff.csv -- basic information collected at exit

### Duplication
No two rows should have the same ClientID and EntryID.

Total rows: 308078
Unique rows: 308078
Unaccounted-for rows: 0

### ClientID
Identifier found in Master.csv

**NaNs:** 0 / 0%

### EntryID
Identifier found in Master.csv

**NaNs:** 0 / 0%

### HousingStatusAtExit
Literally Homeless, Imminently losing their housing, Stably housed, etc.

**NaNs:** 188650 / 61%

### Income received from any source in past 30 days?
Yes/No answer

**NaNs:** 196998 / 63%

We should be able to interpolate & sanity-check these.

### No cash benefit received in past 30 days?
Yes/No answer

**NaNs:** 202439 / 65%

We should be able to interpolate & sanity-check these.


## ExitIncome.csv

ExitIncome.csv has the income data applicable when clients exit their programs

### Duplication
There should be no rows that are simultaneously duplicated on ClientID, EntryID, SourceOfIncome and StartDate.

Total rows: 136038
Unique rows: 135833
Unaccounted-for rows: 205

We should eventually check not only for the *same* start date, but *overlapping* date periods.

### ClientID
Identifier found in Master.csv

**NaNs:** 0 / 0%

### EntryID
Identifier found in Master.csv

**NaNs:** 0 / 0%

### SourceOfIncome
The source of the income for the client

**NaNs:** 5709 / 4%

### Last30DayIncome
How much income from this source was gained in the last 30 days

**NaNs:** 5939 / 4%

### StartDate
The day the client started to receive this income

**NaNs:** 0 / 0%

For income, the StartDate is the date they started receiving the income. If no end date, they are still receiving the income (OR the user didn’t update the data).

The start dates are often arbitrarily assigned and might just be added as the day before the client entered the program because s/he couldn’t remember when it actually started.

There are 3 dates in the future.

### EndDate
The last day the client received this income. If there is no end date, the client is still receiving the income OR the user hasn't updated the data.

**NaNs:** 124855 / 91%


## ExitNCB.csv

ExitNCB.csv has non-cash benefits a client has at time of exit

### Duplication
No two rows should have the same ClientID, EntryID, SourceOfNonCashBenefit, and StartDate.

Total rows: 145720
Unique rows: 145527
Unaccounted-for rows: 193

We should eventually check not only for the *same* start date, but *overlapping* date periods.

Adam: It’s not an issue with how the data were pulled from the system. In some cases, the income/disability/non-cash benefit records were actually entered twice (or more) by users. In other cases, if the client is enrolled multiple times across different programs, the source of income/disability/non-cash benefit is potentially going to show up once per entry (so pay attention to the EntryID).

### ClientID
Identifier found in Master.csv

**NaNs:** 0 / 0%

### EntryID
Identifier found in Master.csv

**NaNs:** 0 / 0%

### SourceOfNonCashBenefit
The actual non-cash benefit the client has

**NaNs:** 2311 / 1%

Migrate those possible rows that could be in ExitIncome to ExitIncome.  Options are the same as in EntryNCB.csv.

### StartDate
The day the client started to receive this NCB

**NaNs:** 0 / 0%

The start dates are often arbitrarily assigned and might just be added as the day before the client entered the program because s/he couldn’t remember when it actually started.

### EndDate
The last day the client received this NCB

**NaNs:** 135140 / 92%

No rows with StartDate later than EndDate


## Services.csv
Services.csv has a list of service transactions provided to clients by programs

### Duplication

No two rows should have the same ClientID, ServiceCode, ServiceProvider, and ServiceStartDate.

Total rows: 1,150,529
Unique rows: 1,029,739
Unaccounted-for rows: 120,790

We should eventually check not only for the *same* start date, but *overlapping* date periods.

According to Adam, it’s not an issue with how the data were pulled from the system; 
he believes all of these services were actually entered twice (or more) by users.

### ServiceID
A unique, arbitrary primary key for the service record

**NaNs:** 0 / 0%

### ClientID
Client identifier found in Master.csv

**NaNs:** 0 / 0%

### ServiceDescription
Brief description of what the service actually is

**NaNs:** 0 / 0%

This has 419 different options, which need to be condensed: if not collapsed, at least grouped by type.

### ServiceCode
A code corresponding with the ServiceDescription. This should just be seen as redundant to the ServiceDescription field.

**NaNs:** 0 / 0%

ServiceCodes have a hierarchy.  You can pretty easily see that when you map codes to ServiceDescriptions:

	select servicecode, servicedescription, count(*) from services group by servicecode, servicedescription order by servicecode;

This may be important for us in collapsing values or otherwise deal with these columns intelligently.

Here’s a brief overview of the categories:

- B: Basic Needs
- D: Consumer Services
- F: Criminal Justice and Legal Services
- H: Education
- J: Environment and Public Health/Safety (no subcategories)
- L: Health Care
- N: Income Support and Employment
- P: Individual and Family Life
- R: Mental Health and Substance Abuse Services
- T: Organizational/Community/International Services
- Y: ? (includes “AIDS/HIV” and “Parents”)

### ProviderSpecificCode
Potentially more detailed description of what the service provided was

**NaNs:** 1129113 / 98%

This is *not* redundant with ServiceDescription, (i.e. a ProviderSpecificCode can be paired with different ServiceDescriptions, and a ServiceDescription can be paired with different ProviderSpecificCodes).

I’m pretty sure this means we can’t impute values here.  There are 507,759 (99.6%) NULLs, so we’re probably just not going to get anything from this column.  It’s possible we can use this column to impute more specific values on general ServiceDescriptions and ServiceCodes, though. ~ihm

### ServiceProvider
The agency/program who provided the service to the client

**NaNs:** 0 / 0%

Most of the providers seem to provide many different kinds of services.

### ServiceStartDate
The date the service was started

**NaNs:** 55 / 0%

### ServiceEndDate
The date the service ended (often the same as ServiceStartDate)

**NaNs:** 390822 / 33%

### FinancialAssistanceType
Potentially more detailed description of what kind of financial assistance the client is receiving (e.g. rental assistance, security deposit)

**NaNs:** 1090366 / 94%

Similar to ProviderSpecificCode, this is probably not going to be useful, unless we use it to impute values on other columns.  For example, “Moving cost assistance” can be used to impute a more specific ServiceCode than just “B: Basic Needs”.

### NeedStatus
If the service offered is successful, unsuccessful, or ongoing

**NaNs:** 0 / 0%

In collapsing, consider the following notes from Adam:

- Met: successfully completed the service
- Completed: closed and met
- Closed: need to go through each provider and make some assumptions (e.g., Emergency Shelters are probably closed and met)

### TotalCost
If applicable, the amount of money (or the cost of the goods) provided to the client

**NaNs:** 1132530 / 98%
**Max:** $16,380
**Min:** $0

These are all just doubles, no NULLs.  There are 7,000 rows that are 0.01 or 0.02, so should be considered as 0.

Possibly missing values or $0 is the actual cost. Use context (e.g., emergency shelter probably won’t have cost; rental assistance likely will)

Cost refers to the cost to the service provider, not the cost to the client.

### DateCreated

**NaNs:** 0 / 0%

### DateUpdated

**NaNs:** 0 / 0%


## Providers.csv

### Duplication

There should be no providers with identical 'Provider' entries.

Total rows: 1280
Unique rows: 1280
Unaccounted-for rows: 0

We're not missing any Providers (that is, no provider appears in Master that's not also in Providers,) so we can throw out that last line.

### Provider
Name of provider as it appears in Master.csv. There are 1280 unique provider names in Providers.csv.

**NaNs:** 1 / 0%

### ProviderLevel
Providers in ServicePoint are organized via a hierarchy. At the top is the sole Level 1 provider: Chicago Alliance to End Homelessness(1), as we are the agency that has access to all information. Below Level 1 is Level 2 where all the agency names are. For example, Heartland Human Care Services(35) refers to the entire agency. Below that are actual programs in Level 3. Heartland Human Care Services Families Building Community(266) is an example of an actual program. You have a few Level 3 programs that are split into multiple Level 4 “sub-programs.”

**NaNs:** 1 / 0%

There will be people enrolled at Level 2, and this would be a mistake. They should be enrolled at the Level 3 program.

### ParentProvider
The provider under which the Provider sits in the hierarchy. The ParentProvider for Heartland Human Care Services Families Building Community(266) is Heartland Human Care Services(35), because 266 sits underneath 35.

**NaNs:** 49 / 3%

ParentProvider is NaN iff ProviderLevel is 1.

### CurrentlyOperational
Yes/No as to whether or not the provider is currently operating

**NaNs:** 1 / 0%

Adam: The value in this column is accurate to which programs are currently operational. This would help you figure out if a person with an enrollment date in 2007 but no exit date is truly still enrolled. So whether or not you include or remove data from operational providers is up to you and probably will not be a catch-all "we will/won't include all inoperational providers."

### AddressLine1
Address information (if available, physical address is used)

**NaNs:** 804 / 62%

Many level 4 providers share the save address.

### AddressLine2
Address information (if available)

**NaNs:** 1190 / 92%

### City
Address information (if available)

**NaNs:** 803 / 62%

'Shreveport' is for 'Bowman CSBG Test Data(805)', the provider of HMIS.

### State
Address information (if available)

**NaNs:** 804 / 62%

Need to strip trailing whitespace, (currently has 'IL ' instead of 'IL').

'LA ' is for 'Bowman CSBG Test Data(805)', the provider of HMIS.

### Zip
Address information (if available)

**NaNs:** 813 / 63%

All are 5-digit zip codes except '60612-3653'.

'71101' is for 'Bowman CSBG Test Data(805)', the provider of HMIS.

### NumActiveUsers
The number of active users, (case managers or technical people,) currently at the agency. Because users are often given access to an entire agency’s data, they will be assigned to a Level 2 provider (the agency) instead of a Level 3 provider (an individual program). This is why a lot of operational Level 3 providers have 0 active users assigned to it.

Active means active in the last few, (6?,) months.

**NaNs:** 1 / 0%

### ProgramTypeCode
How HUD classifies this program.

**NaNs:** 399 / 31%

See page 27 of the [HMIS Standards](https://www.onecpd.info/resources/documents/FinalHMISDataStandards_March2010.pdf).

### AltProgramType
Whether or not the program falls under Interim (because HUD doesn’t use the definition “Interim Housing,” you won’t find it in the ProgramTypeCode column), PHwSS, or Supportive Services for Veteran Families.

**NaNs:** 1165 / 91%

Clarified Provider Types: 

- Permanent Supportive Housing
- Interim Housing
	- Some Transitional Housing (HUD)
	- Some Emergency Shelters (HUD)
- Permanent Housing with Short-term Rent Support (PHwSS)
	- Some Transitional Housing (HUD)
- Emergency Shelter
- Rapid Re-Housing
- Service Only Program
	- Service Only Program
	- Homeless Outreach
	- Prevention
- SSVF
	- Were mislabeled as some HPRP
- Safe Haven
- HPRP
	- most are outdated
	- some are SSVF

'Inner Voice - It Takes a Village (Interim)(452)' should be counted as 'Interim Housing', even though it's marked as 'Permanent Supportive Housing'

We have our 6 Supportive Services for Veteran Families (SSVF) programs marked with a ProgramTypeCode as Homeless Prevention and Rapid Re-Housing (also known as "HPRP"), but that is a bit misleading … SSVF programs are funded by the Veterans Administration (VA), and they don't exactly fall into any of the classic HUD program types. They do work in both homeless prevention and rapid re-housing, but they should not be considered among the other HPRP programs that all stopped operating several years ago. In addition to Interim Housing and Permanent Housing with Short-Term Support, we created another non-HUD program type called SSVF for these six providers.

While programs marked as Safe Havens are a lot like Permanent Supportive Housing, they are lower threshold and probably have not-as-great outcomes as traditional Permanent Supportive Housing programs. You should keep them as their own program type, but don't ignore them.  (Don't be confused by the fact there is an agency called "A Safe Haven." They don't have any programs that are classified as having the safe haven program type.)

Homeless Outreach and Prevention don't directly provide any actual housing, so you could lump them in with being Service Only Programs. You may potentially want to keep them separate as their own entities, though.


## ReviewDetail.csv

### Duplication

No two rows should have the same EntryID and ReviewDate.

Total rows: 7378
Unique rows: 7314
Unaccounted-for rows: 64

### ReviewID
Primary key of this table (arbitrary integer); you’ll see this used as foreign key in other tables

**NaNs:** 1 / 0%

### EntryID
Identifier found in Master.csv

**NaNs:** 1 / 0%

### ReviewType
The type of review being performed (annual, 6-month, 2-month, etc.; some programs have different frequencies of reviews)

**NaNs:** 1 / 0%

### ReviewDate
Date the review was completed

**NaNs:** 1 / 0%

### HousingStatus
Literally Homeless, Imminently losing their housing, Stably housed, etc.

**NaNs:** 60 / 0%

### Do you have a disability of long duration?
Yes/No answer

**NaNs:** 59 / 0%

### Income received from any source in past 30 days?
Yes/No answer

**NaNs:** 86 / 1%

### Non-cash benefit received in past 30 days?
Yes/No answer

**NaNs:** 92 / 1%

### Are you receiving Medicaid?
Yes/No answer

**NaNs:** 3177 / 43%


##ReviewIncome.csv

### EntryID
Identifier found in Master.csv

### ReviewID
Identifier found in ReviewDetail.csv

### SourceOfIncome
The source of the income for the client

### Last30DayIncome
How much income from this source was gained in the last 30 days

### StartDate
The day the client started to receive this income

### EndDate
The last day the client received this income. If there is no end date, the client is still receiving the income OR the user hasn't updated the data.


## ReviewNCB.csv

### EntryID
Identifier found in Master.csv

### ReviewID
Identifier found in ReviewDetail.csv

### SourceOfNonCashBenefit
The actual non-cash benefit the client has

### StartDate
The day the client started to receive this NCB

### EndDate
The last day the client received this NCB


##ReviewDisabilities.csv

### EntryID
Identifier found in Master.csv

### ReviewID
Identifier found in ReviewDetail.csv

### DisabilityType
Actual disabling condition (e.g. Physical, Mental Health Problem, Alcohol Abuse)

### DisabilityDetermination
Yes/No response to if condition is legally a disability

### StartDate
Date disability was identified

### EndDate
Date disability no longer affecting client. If there is no end date, then this disability is still affecting the client.
