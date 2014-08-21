"""A module with commonly- and uncommonly-used feature sets for modeling.

To be used primarily with :mod:`pipeline`.

"""

unused = ['ClientUniqueID',
          'ClientID',
          'HouseholdID',
          'Head Of Household?',
          'Relationship to HoH',
          'Entry Exit GroupID',
          'EntryID',
          'ProviderID',
          'ProgramEntryDate',
          'ProgramExitDate',
          'PrimaryRace',
          'Ethnicity',
          'Veteran?',
          'YearOfBirth',
          'AgeEntered',
          'AgeEnteredBucketDFSS',
          'SecondaryRace',
          'PrimaryLanguageSpoken',
          'ZipCodeOfLastPermanentAddress',
          'ZipDataQuality',
          'ExitReason',
          'Anonymous',
          'DateCreated',
          'DateUpdated',
          'Provider',
          'ProviderLevel',
          'ParentProvider',
          'CurrentlyOperational',
          'AddressLine1',
          'AddressLine2',
          'City',
          'State',
          'NumActiveUsers',
          'ProgramTypeCode',
          'AltProgramType',
          'Last30DayIncome',
          'ProgramEntryDateOfFirstEntry',
          'ProgramTypeOfFirstEntry',
          'ProgramEntryDateOfFirstEntryHomelessnessProgram',
          'ProgramTypeOfFirstEntryHomelessnessProgram',
          'DaysSinceFirstEntry',
          'DaysSinceFirstEntryHomelessnessProgram',
          'DaysSinceFirstEntryHomelessnessProgramBucket',
          'ValidZipCodeOfLastPermanentAddress?',
          'ProgramEntryDateReentry',
          'ProgramTypeReentry']

demographics = ['Race/Ethnicity (4-way)',
                'Veteran?Imputed',
                'Refused',
                'AgeEnteredBucket']

housing_demographics = ['PreviousLivingSituation',
                        'LengthOfStayInPreviousLivingSituation',
                        'DaysSinceFirstEntryBucket']

family_demographics = ['Family?',
                       'SingleAdult?',
                       'Children?',
                       'SingleAdultWithChildren?',
                       'Under 6 years?',
                       '6 to 17 years?',
                       '18 to 64 years?',
                       '65 years and over?']

family_counts = ['Under 6 years',
                 '6 to 17 years',
                 '18 to 64 years',
                 '65 years and over',
                 'OtherFamilyMembers']

exit_stuff = ['DestinationAtExit',
              'LengthOfStay']

program = ['ProgramType',
           'Reviewed?']

program_aggs = ['ProgramTypeAggregate',
                'HomelessnessProgram?']

program_location = ['Zip']

disabilities_entry = ['Alcohol Abuse (HUD 40118) Entry',
                      'Both alcohol and drug abuse (HUD 40118) Entry',
                      'Developmental (HUD 40118) Entry',
                      'Drug Abuse (HUD 40118) Entry',
                      'HIV/AIDS (HUD 40118) Entry',
                      'Mental Health Problem (HUD 40118) Entry',
                      'Physical (HUD 40118) Entry',
                      'Disabled? Entry']

disabilities_review = ['Alcohol Abuse (HUD 40118) Review',
                       'Both alcohol and drug abuse (HUD 40118) Review',
                       'Developmental (HUD 40118) Review',
                       'Drug Abuse (HUD 40118) Review',
                       'HIV/AIDS (HUD 40118) Review',
                       'Mental Health Problem (HUD 40118) Review',
                       'Physical (HUD 40118) Review',
                       'Disabled? Review']

disabilities_breakout = ['Mental Health Problem (HUD 40118)',
                         'Physical (HUD 40118)',
                         'Drug Abuse (HUD 40118)',
                         'HIV/AIDS (HUD 40118)',
                         'Alcohol Abuse (HUD 40118)',
                         'Both alcohol and drug abuse (HUD 40118)',
                         'Developmental (HUD 40118)']

disabilities = ['Disabled?']

income_breakout = ['Alimony or Other Spousal Support (HUD)',
                   'Child Support (HUD)',
                   'Contributions From Other People',
                   'Earned Income (HUD)',
                   'General Assistance (HUD)',
                   'Pension From a Former Job (HUD)',
                   'Private Disability Insurance (HUD)',
                   'Private Health Insurance',
                   'Rental Income',
                   'Retirement Disability',
                   'Retirement Income From Social Security (HUD)',
                   'SSDI (HUD)',
                   'SSI (HUD)',
                   'TANF (HUD)',
                   'Unemployment Insurance (HUD)',
                   "Veteran's Disability Payment (HUD)",
                   "Veteran's Pension (HUD)",
                   "Worker's Compensation (HUD)"]

income = ['Last30DayIncomeBucket']

income_exit = ['Alimony or Other Spousal Support (HUD) Exit',
               'Child Support (HUD) Exit',
               'Contributions From Other People Exit',
               'Dividends (Investments) Exit',
               'Earned Income (HUD) Exit',
               'General Assistance (HUD) Exit',
               'Pension From a Former Job (HUD) Exit',
               'Private Disability Insurance (HUD) Exit',
               'Private Health Insurance Exit',
               'Rental Income Exit',
               'Retirement Disability Exit',
               'Retirement Income From Social Security (HUD) Exit',
               'SSDI (HUD) Exit',
               'SSI (HUD) Exit',
               'TANF (HUD) Exit',
               'Unemployment Insurance (HUD) Exit',
               "Veteran's Disability Payment (HUD) Exit",
               "Veteran's Pension (HUD) Exit",
               "Worker's Compensation (HUD) Exit",
               'Last30DayIncome Exit',
               'EarnedIncomeExitChange',
               'CashIncomeExitChange']

income_outcomes = ['EarnedIncomeExitHas',
                   'CashIncomeExitHas']

ncb_breakout = ['MEDICAID (HUD)',
                'MEDICARE (HUD)',
                'SCHIP (HUD)',
                'Section 8, Public Housing or rental assistance (HUD)',
                'Special Supplemental Nutrition Program for WIC (HUD)',
                'Supplemental Nutrition Assistance Program (Food Stamps) (HUD)',
                'Temporary rental assistance (HUD)',
                "Veteran's Administration (VA) Medical Services (HUD)"]

ncb = ['NCBIncomeHas']

ncb_exit = ['MEDICAID (HUD) Exit',
            'MEDICARE (HUD) Exit',
            'SCHIP (HUD) Exit',
            'Section 8, Public Housing or rental assistance (HUD) Exit',
            'Special Supplemental Nutrition Program for WIC (HUD) Exit',
            'Supplemental Nutrition Assistance Program (Food Stamps) (HUD) Exit',
            'Temporary rental assistance (HUD) Exit',
            "Veteran's Administration (VA) Medical Services (HUD) Exit"]

ncb_outcomes = ['NCBIncomeExitHas']

services_breakout = ['B Service',
                     'D Service',
                     'F Service',
                     'H Service',
                     'L Service',
                     'N Service',
                     'P Service',
                     'R Service',
                     'T Service']

services = ['Services?']

housing_outcomes = ['CaseOutcome',
                    'CaseSuccess',
                    'Reentered6Month',
                    'Reentered12Month',
                    'Reentered6MonthFromPermanent',
                    'Reentered12MonthFromPermanent']

reduced = ['ProgramType',
           'Reviewed?',
           'Veteran?Imputed',
           'PreviousLivingSituation',
           'DaysSinceFirstEntryBucket',
           'AgeEnteredBucket',
           'Last30DayIncomeBucket',
           'NCBIncomeHas']

all_sets = demographics + housing_demographics + family_counts + program + disabilities + income + ncb + services
