"""The cleaning module.

Really the only method that's important for a user to know about is :func:`load`.  :func:`clean` is used to clean raw
data into `clean/`, but is wrapped by `make`, (see `Makefile` and `README` for more info`).

There are several functions that operate on `master`, and they all function on `master_all` as well.

"""
import pandas as pd
import numpy as np
import os, sys, datetime, dateutil

# the path where the raw data resides
raw_path = '/mnt/data/allchicago/data/'
# the path where the raw auxiliary data resides
auxiliary_path = '/mnt/data/allchicago/auxiliary_data/'

script_dir = os.path.dirname(__file__)
clean_dir = os.path.join(script_dir, 'clean')

def clean(df_name):
    """Given the data frame name, load the raw data and cleaned dependencies, clean the raw data, and save it as a CSV
    and a pickle.

    :param df_name: The dataframe to clean.  This should be in the form `entry_details`, not `EntryDetails`.
    :type df: str.

    """
    df = load_raw(df_name)

    # clean `master` and `master_all`
    if df_name.startswith('master'):
        # load `providers` and merge
        providers = load_clean('providers')
        df = pd.merge(df, providers, left_on='ProviderID', right_on='Provider', how='left')

        df['DateCreated'] = pd.to_datetime(df['DateCreated'], format="%m/%d/%Y")
        df['DateUpdated'] = pd.to_datetime(df['DateUpdated'], format="%m/%d/%Y")
        # if we're cleaning `master`, (not `master_all`,) only take records after September 2012
        if df_name == 'master':
            df = df[df['DateCreated'] > switch_date]

        df['Refused'] = df.apply(get_refused, axis=1)

        df.replace({'Relationship to HoH': master_relationship_to_hoh_replacements}, inplace=True)

        df['ProgramEntryDate'] = pd.to_datetime(df['ProgramEntryDate'], format="%m/%d/%Y")
        # replace default value of 1980-01-01 with pd.NaT
        df['ProgramEntryDate'].replace(datetime.datetime(1980,1,1), pd.NaT, inplace=True)
        df['ProgramExitDate'] = pd.to_datetime(df['ProgramExitDate'], format="%m/%d/%Y")
        # replace default value of 1980-01-01 with pd.NaT
        df['ProgramExitDate'].replace(datetime.datetime(1980,1,1), pd.NaT, inplace=True)
        # compute `LengthOfStay` if possible
        df['LengthOfStay'] = (df['ProgramExitDate'] - df['ProgramEntryDate']).map(get_days_geq_0)

        df['YearOfBirth'].replace('#NUM!', np.NaN, inplace=True)
        df['YearOfBirth'] = pd.to_datetime(df['YearOfBirth'], format="%Y")

        # generate AgeEntered
        df['AgeEntered'] = df.apply(get_age_entered, axis=1)
        # generate AgeEnteredBucket and AgeEnteredBucketDFSS for different categorizations
        df['AgeEnteredBucket'] = df['AgeEntered'].apply(get_age_bucket)
        df['AgeEnteredBucketDFSS'] = df['AgeEntered'].apply(get_dfss_age_bucket)

        df = pd.merge(df, get_family_composition(df), on='EntryID', how='left')

        df['Ethnicity'].replace(master_ethnicity_nans, np.NaN, inplace=True)

        df.replace({'PrimaryRace': master_primary_race_replacements}, inplace=True)

        df['Race/Ethnicity (4-way)'] = df.apply(get_race_ethnicity_4_way, axis=1)

        df['Veteran?'].replace(master_veteran_nans, np.NaN, inplace=True)
        # fill in all nulls with 'No (HUD)'
        # TODO this should just be a :func:`fillna`.
        df['Veteran?Imputed'] = df['Veteran?'].apply(impute_veteran)

        # get entry disability information, merge, and fill in any missing rows with `False`s
        df = pd.merge(df, get_disabilities('entry_disabilities').rename(columns=lambda x: x+" Entry"), left_on='EntryID', right_index=True, how='left')
        df.fillna({d: False for d in disability_types_entry}, inplace=True)
        df['Disabled? Entry'] = df[disability_types_entry].any(axis=1)

        # get review disability information, merge, and fill in any missing rows with `False`s
        df = pd.merge(df, get_disabilities('review_disabilities').rename(columns=lambda x: x+" Review"), left_on='EntryID', right_index=True, how='left')
        df.fillna({d: False for d in disability_types_review}, inplace=True)
        df['Disabled? Review'] = df[disability_types_review].any(axis=1)

        # use entry and review disability information to compute "general" disability information
        for dt in disability_types:
            df[dt] = df[dt+' Entry'] | df[dt+' Review']
        df['Disabled?'] = df[disability_types].any(axis=1)

        # get entry income information, merge, and fill in any missing rows with `0`s
        entry_income_granular, entry_income_total = get_income('entry_income')
        df = pd.merge(df, entry_income_granular, left_on='EntryID', right_index=True, how='left')
        df = pd.merge(df, entry_income_total, left_on='EntryID', right_index=True, how='left')
        df.fillna({i: 0 for i in income_types}, inplace=True)
        df.fillna({'Last30DayIncome': 0}, inplace=True)
        # bucket entry income
        df['Last30DayIncomeBucket'] = df['Last30DayIncome'].apply(get_income_bucket)

        # get exit income information, merge, and fill in any missing rows with `0`s
        exit_income_granular, exit_income_total = get_income('exit_income')
        df = pd.merge(df, exit_income_granular.rename(columns=lambda x: x+" Exit"), left_on='EntryID', right_index=True, how='left')
        df = pd.merge(df, exit_income_total.rename(columns=lambda x: x+" Exit"), left_on='EntryID', right_index=True, how='left')
        df.fillna({i: 0 for i in income_types_exit}, inplace=True)
        df.fillna({'Last30DayIncome Exit': 0}, inplace=True)
        # bucket exit income
        df['Last30DayIncomeExitBucket'] = df['Last30DayIncome Exit'].apply(get_income_bucket)

        # get entry ncb information, merge, and fill in any missing rows with `False`s
        df = pd.merge(df, get_ncb('entry_ncb'), left_on='EntryID', right_index=True, how='left')
        df.fillna({d: False for d in ncb_types}, inplace=True)

        # get exit ncb information, merge, and fill in any missing rows with `False`s
        df = pd.merge(df, get_ncb('exit_ncb'), left_on='EntryID', right_index=True, how='left', suffixes=('',' Exit'))
        df.fillna({d: False for d in ncb_types_exit}, inplace=True)

        df.replace({'PreviousLivingSituation': master_previous_living_situation_replacements}, inplace=True)

        df.replace({'LengthOfStayInPreviousLivingSituation': master_length_of_stay_in_previous_living_situation_replacements}, inplace=True)

        # if we're cleaning `master`, compute legacy information about the first time a client entered the homelessness
        # system, both into a program in general, and specifically into a "Homelessness Program" (see
        # `providers_homelessness_programs`).
        if df_name == 'master':
            # master
            master_all = load_clean('master_all')
            # get info about first entry in a program in general
            df = pd.merge(df, first_entry(master_all), on='EntryID', how='left')
            # get info about first entry in a "Homelessness Program" in general
            df = pd.merge(df, first_entry(master_all[master_all['HomelessnessProgram?'] == True]), on='EntryID', suffixes=('','HomelessnessProgram'), how='left')
            # compute days since first entries
            df['DaysSinceFirstEntryBucket'] = df['DaysSinceFirstEntry'].apply(get_days_since_first_entry_bucket)
            df['DaysSinceFirstEntryHomelessnessProgramBucket'] = df['DaysSinceFirstEntryHomelessnessProgram'].apply(get_days_since_first_entry_bucket)

        # load census zip data, and compare zip codes to see if they are valid
        zips = {z for z in load_auxiliary('zips')['zip'].values}
        df['ValidZipCodeOfLastPermanentAddress?'] = df['ZipCodeOfLastPermanentAddress'].apply(lambda z: z != '99999' and z in zips)

        df.replace({'DestinationAtExit': master_destination_at_exit_replacements}, inplace=True)

        # check if a client was reviewed by looking for their `EntryID` in `review_details`
        reviews = {e for e in load_clean('review_details')['EntryID']}
        df['Reviewed?'] = df['EntryID'].apply(lambda e: e in reviews)

        # find what services a client got, and compute if they got any
        df = pd.merge(df, get_services(df).rename(columns=lambda x: x+" Service"), left_on='EntryID', right_index=True, how='left')
        df.fillna({d: False for d in service_types}, inplace=True)
        df['Services?'] = df[service_types].any(axis=1)

        ############
        # Outcomes #
        ############

        # compute `CaseOutcome` and `CaseSuccess` from `DestinationAtExit`; `CaseSuccess` is just whether or not
        # `CaseOutcome` is `Permanent`
        df['CaseOutcome'] = df.apply(get_case_outcome, axis=1)
        df['CaseSuccess'] = df['CaseOutcome'].apply(lambda o: np.NaN if pd.isnull(o) else o == 'Permanent')

        # get reentry information, merge, and compute reentry outcomes
        df = pd.merge(df, get_reentries(df), on=['ClientUniqueID','ProgramExitDate'], suffixes=('','Reentry'), how='left')
        df['Reentered6Month'] = get_delta_reentries(df, np.timedelta64(6,'M'))
        df['Reentered12Month'] = get_delta_reentries(df, np.timedelta64(12,'M'))
        # only merge rows whose `CaseOutcome` is 'Permanent'
        df['Reentered6MonthFromPermanent'] = get_delta_reentries(df, np.timedelta64(6,'M'))[df['CaseOutcome'] == 'Permanent']
        df['Reentered12MonthFromPermanent'] = get_delta_reentries(df, np.timedelta64(12,'M'))[df['CaseOutcome'] == 'Permanent']

        # compute income outcomes
        df['EarnedIncomeExitHas'] = df['Earned Income (HUD) Exit'] > 0
        df['EarnedIncomeExitChange'] =  df['Earned Income (HUD) Exit'] - df['Earned Income (HUD)']
        df['CashIncomeExitHas'] = df['Last30DayIncome Exit'] > 0
        df['CashIncomeExitChange'] =  df['Last30DayIncome Exit'] - df['Last30DayIncome']

        # compute ncb outcomes
        df['NCBIncomeHas'] = df[ncb_types+ncb_types_exit].any(axis=1)
        df['NCBIncomeExitHas'] = df[ncb_types_exit].any(axis=1)

        # remove duplicate entries
        df = deduplicate_entry_id(df)

    elif df_name == 'providers':
        df = df[:-1] # ignore blank last row

        # manually make a few providers' type into 'Street Outreach' to distinguish them as "Homelessness Programs"
        df.loc[df['Provider'].apply(lambda p: p in providers_street_outreach), 'AltProgramType'] = 'Street Outreach'

        # get the `ProgramType`, `ProgramTypeAggregate`, and `HomelessnessProgram?` from `ProgramTypeCode` and `AltProgramType`
        # TODO this should be a simple | statement between the two columns
        df['ProgramType'] = df.apply(get_program_type, axis=1)
        df['ProgramTypeAggregate'] = df['ProgramType'].replace(providers_program_type_aggregates)
        df['HomelessnessProgram?'] = df['ProgramType'].apply(lambda t: np.NaN if pd.isnull(t) else (t in providers_homelessness_programs))

    elif df_name == 'entry_details':
        # ignore blank last 45,292 rows
        df = df[:-45292]

    elif df_name == 'entry_disabilities':
        df.replace({'DisabilityType': disability_type_replacements}, inplace=True)

    elif df_name == 'entry_income' or df_name == 'exit_income':
        df['StartDate'] = pd.to_datetime(df['StartDate'], format="%m/%d/%Y")
        df['EndDate'] = pd.to_datetime(df['EndDate'], format="%m/%d/%Y")

        df.replace({'SourceOfIncome': income_replacements}, inplace=True)

    elif df_name == 'entry_ncb' or df_name == 'exit_ncb':
        df['StartDate'] = pd.to_datetime(df['StartDate'], format="%m/%d/%Y")
        df['EndDate'] = pd.to_datetime(df['EndDate'], format="%m/%d/%Y")

        df.replace({'SourceOfNonCashBenefit': ncb_replacements}, inplace=True)

    elif df_name == 'review_details':
        # ignore blank last row
        df = df[:-1]

        df['ReviewDate'] = pd.to_datetime(df['ReviewDate'], format="%m/%d/%Y")

        df['HousingStatus'].replace(review_details_housing_status_nans, np.NaN, inplace=True)
        df['HousingStatusAggregate'] = df['HousingStatus'].replace(review_details_housing_status_aggregates)

    elif df_name == 'review_disabilities':
        df.replace({'DisabilityType': disability_type_replacements}, inplace=True)

    elif df_name == 'services':
        df.rename(columns={'ServiceDescription])': 'ServiceDescription'}, inplace=True)

        df['DateCreated'] = pd.to_datetime(df['DateCreated'], format="%m/%d/%Y")
        df['DateUpdated'] = pd.to_datetime(df['DateUpdated'], format="%m/%d/%Y")

        df['ServiceStartDate'] = pd.to_datetime(df['ServiceStartDate'], format="%m/%d/%Y")
        df['ServiceEndDate'] = pd.to_datetime(df['ServiceEndDate'], format="%m/%d/%Y")
        # compute `LengthOfService` if possible
        df['LengthOfService'] = (df['ServiceEndDate'] - df['ServiceStartDate']).map(lambda x: x/np.timedelta64(1, 'D'))

        # compute Level 1 and Level 2 of AIRS taxonomy for each service
        df['ServiceTypeL1'] = df['ServiceCode'].apply(lambda x: x[0])
        df['ServiceTypeL2'] = df['ServiceCode'].apply(lambda x: x[:2] if len(x) > 1 else np.NaN)

    # write output to pickel and CSV
    df.to_pickle(pickle_path(df_name))
    df.to_csv(csv_path(df_name))

    return None

def load_clean(df_name):
    """Given the data frame name, return the cleaned, pickled data frame

    :param df_name: The dataframe to load.  This should be in the form `entry_details`, not `EntryDetails`.
    :type df_name: str.

    """
    return pd.io.pickle.read_pickle(pickle_path(df_name))

# alias for convenience & backwards compatability
load = load_clean

def load_auxiliary(file_name):
    """Given the file name, return the auxiliary data frame

    :param df_name: The dataframe to clean.  This is currently only used for `zips`.
    :type df_name: str.

    """
    path = os.path.join(auxiliary_path, file_name + '.csv')
    return pd.read_csv(path, dtype=str)

def load_raw(df_name):
    """Given the data frame name, return the raw data frame

    :param df_name: The dataframe to load.  This should be in the form `entry_details`, not `EntryDetails`.
    :type df_name: str.

    """
    path = os.path.join(raw_path, raw_names[df_name]+'.csv')
    return pd.read_csv(path, na_values="NA", low_memory=False)

def pickle_path(df_name):
    """Given the data frame name, return the path to the clean pickle

    :param df_name: The dataframe to load.  This should be in the form `entry_details`, not `EntryDetails`.
    :type df_name: str.

    """
    return os.path.join(clean_dir, 'pickles', df_name+'.pkl')

def csv_path(df_name):
    """Given the data frame name, return the path to the clean csv

    :param df_name: The dataframe to load.  This should be in the form `entry_details`, not `EntryDetails`.
    :type df_name: str.

    """
    return os.path.join(clean_dir, 'csvs', df_name+'.csv')

# the raw names of the files we were given
raw_names = {'master':              'Master',
             'master_all':          'Master',
             'entry_details':       'EntryDetails',
             'entry_income':        'EntryIncome',
             'entry_ncb':           'EntryNCB',
             'entry_disabilities':  'EntryDisabilities',
             'exit_stuff':          'ExitStuff',
             'exit_income':         'ExitIncome',
             'exit_ncb':            'ExitNCB',
             'services':            'Services',
             'providers':           'Providers',
             'review_details':      'ReviewDetail',
             'review_income':       'ReviewIncome',
             'review_ncb':          'ReviewNCB',
             'review_disabilities': 'ReviewDisabilities'}

## date when HMIS switched to All Chicago 
switch_date = datetime.datetime(2012, 9, 16)

## date of dump
dump_date = datetime.datetime(2014, 7, 1)

def get_days_geq_0(t):
    """Given an `numpy.timedelta64`, return the number of days it represents, and if it's less than 0, return `pd.NaT`.

    :param t: The timedelta.
    :type t: numpy.timedelta64.

    """
    t = t/np.timedelta64(1, 'D')
    return t if t >= 0 else pd.NaT

def get_refused(row):
    """Given a row from `master`, return whether or not the client ever refused to answer a question.

    :param row: A row from `master`.
    :type row: dict-like.

    """
    for _, v in row.iteritems():
        if v == 'Refused (HUD)' or  v == 'refused':
            return True
    return False

master_relationship_to_hoh_replacements = {'Son':                'Child',
                                           'Daughter':           'Child',
                                           'Step-son':           'Child',
                                           'Step-daughter':      'Child',
                                           'Husband':            'Spouse',
                                           'Wife':               'Spouse',
                                           'Significant other':  'Spouse',
                                           'Father':             'Parent',
                                           'Mother':             'Parent',
                                           'Husband and Father': 'Parent',
                                           'Wife and Mother':    'Parent',
                                           'Guardian':           'Parent',
                                           'Grandson':           'Grandchild',
                                           'Granddaughter':      'Grandchild',
                                           'In-Law':             'Sibling',
                                           'Grandfather':        'Grandparent',
                                           'Grandmother':        'Grandparent',
                                           'cousin':             'Cousin',
                                           'Other relative':     np.NaN,
                                           'Other non-relative': np.NaN,
                                           'Non-Relative':       np.NaN,
                                           'Unknown':            np.NaN,
                                           'Other':              np.NaN}

def get_age_entered(row):
    """Return years between entry year and birth year.

    :param row: A row from `master`.
    :type row: dict-like.

    """
    program_entry_date = row['ProgramEntryDate']
    year_of_birth = row['YearOfBirth']
    if program_entry_date is pd.NaT or year_of_birth is pd.NaT:
        return np.NaN
    else:
        return dateutil.relativedelta.relativedelta(program_entry_date, year_of_birth).years

def get_age_bucket(age):
    """Return the age bucket.

    :param age: Age.
    :type age: int.

    """
    if pd.isnull(age):
        return np.NaN
    elif age < 6:
        return 'Under 6 years'
    elif age < 18:
        return '6 to 17 years'
    elif age < 65:
        return '18 to 64 years'
    else:
        return '65 years and over'

def get_dfss_age_bucket(age):
    """Return the DFSS age bucket.

    :param age: Age.
    :type age: int.

    """
    if pd.isnull(age):
        return np.NaN
    elif age < 1:
        return 'DFSS: Under 1 year'
    elif age < 6:
        return 'DFSS: 1 to 5 years'
    elif age < 13:
        return 'DFSS: 6 to 12 years'
    elif age < 18:
        return 'DFSS: 13 to 17 years'
    elif age < 25:
        return 'DFSS: 18 to 24 years'
    elif age < 31:
        return 'DFSS: 25 to 30 years'
    elif age < 51:
        return 'DFSS: 31 to 50 years'
    elif age < 62:
        return 'DFSS: 51 to 61 years'
    else:
        return 'DFSS: 62 years and over'

age_buckets = ['Under 6 years','6 to 17 years','18 to 64 years','65 years and over']

def get_family_composition(df):
    """Given `master`, compute the age composition for each entry's family.  Do so by pivoting each `Entry Exit GroupID`
    out on `AgeEnteredBucket`, then merge it into the dataframe to recover `EntryID`, so that it can be easily merged
    back into `master`.

    :param df: `master` dataframe.
    :type df: pandas.Dataframe.
    
    """
    # prep f to pivot on 'Entry Exit GroupID' if there is one, otherwise on 'EntryID'
    f = df[['EntryID','Entry Exit GroupID','AgeEnteredBucket']].copy()
    f['Entry Exit GroupID'][pd.isnull(f['Entry Exit GroupID'])] = -f['EntryID']
    # build fp, a pivot table on 'AgeEnteredBucket'
    # NOTE: this drops people who have no AgeEnteredBucket
    f['count'] = 1
    fp = pd.pivot_table(f, values='count', index='Entry Exit GroupID', columns='AgeEnteredBucket', aggfunc=np.sum, fill_value=0)
    # compute 'OtherFamilyMembers'
    fp['OtherFamilyMembers'] = fp.sum(axis=1) - 1
    # compute binary variables
    fp['Family?'] = fp['OtherFamilyMembers'] > 0
    fp['SingleAdult?'] = fp['18 to 64 years'] + fp['65 years and over'] <= 1
    fp['Children?'] = fp['Under 6 years'] + fp['6 to 17 years'] > 0
    fp['SingleAdultWithChildren?'] = fp['SingleAdult?'] & fp['Children?']
    for b in age_buckets:
        fp[b+'?'] = fp[b] > 0
    # merge fp back into f and return
    return_cols = ['EntryID','OtherFamilyMembers','Family?','SingleAdult?','Children?','SingleAdultWithChildren?'] + age_buckets + [b+'?' for b in age_buckets]
    return pd.merge(f, fp, left_on='Entry Exit GroupID', right_index=True)[return_cols]

master_ethnicity_nans = ["Don't Know (HUD)", 'Refused (HUD)', 'Other (Non-Hispanic/Latino)']

master_primary_race_replacements = {'white': 'White (HUD)',
                                    'black/african american': 'Black or African American (HUD)',
                                    'asian': 'Asian (HUD)',
                                    'native american': 'American Indian or Alaska Native (HUD)',
                                    'Other': np.NaN,
                                    "Don't Know (HUD)": np.NaN,
                                    'Other Multi-Racial': np.NaN,
                                    'Refused (HUD)': np.NaN,
                                    'multi-racial': np.NaN,
                                    'American Indian/Alaskan Native & White (new HUD 40118)': np.NaN,
                                    'Pacific Islander (HUD 40118)': np.NaN,
                                    'Black/African American & White (new HUD 40118)': np.NaN,
                                    'American Indian/Alaskan Native & Black (new HUD 40118)': np.NaN,
                                    'Asian & White (new HUD 40118)': np.NaN}

race_replacements_4_way = {'Black or African American (HUD)':                 'Black or African American (4-way)',
                           'White (HUD)':                                     'White (4-way)',
                           'Native Hawaiian or Other Pacific Islander (HUD)': 'Other (4-way)',
                           'American Indian or Alaska Native (HUD)':          'Other (4-way)',
                           'Asian (HUD)':                                     'Other (4-way)'}

def get_race_ethnicity_4_way(row):
    """Compute `Race/Ethnicity (4-way)`.  'Hispanic/Latino (HUD)' takes precedence.

    :param row: A row from `master`.
    :type row: dict-like.

    """
    if row['Ethnicity'] == 'Hispanic/Latino (HUD)':
        return 'Hispanic/Latino (4-way)'
    else:
        return race_replacements_4_way[row['PrimaryRace']] if pd.notnull(row['PrimaryRace']) else np.NaN

master_veteran_nans = ["Don't Know (HUD)", 'Refused (HUD)']

# TODO this should just be a :func:`fillna`.
def impute_veteran(veteran):
    """Impute veteran status: if a client has no label, assume they are not a veteran.

    :param veteran: A veteran status from `master`.
    :type veteran: str.

    """
    if pd.isnull(veteran):
        return 'No (HUD)'
    else:
        return veteran

master_previous_living_situation_replacements = {
    'Emergency Shelter':                                            'Emergency shelter, including hotel or motel paid for with emergency shelter voucher(HUD)',
    'emergency shelter (hud)':                                      'Emergency shelter, including hotel or motel paid for with emergency shelter voucher(HUD)',
    'Transitional Housing for Homeless Person':                     'Transitional housing for homeless persons (including homeless youth) (HUD)',
    'Interim Housing':                                              'Transitional housing for homeless persons (including homeless youth) (HUD)',
    'Permanent Housing for Formerly Homeless Person':               'Permanent housing for formerly homeless persons(such as SHP, S+C, or SRO Mod Rehab)(HUD)',
    'Psychiatric Facility':                                         'Psychiatric hospital or other psychiatric facility (HUD)',
    'Substance Abuse Treatment Facility':                           'Substance abuse treatment facility or detox center (HUD)',
    'Hospital':                                                     'Hospital (non-psychiatric) (HUD)',
    'hospital (hud)':                                               'Hospital (non-psychiatric) (HUD)',
    'Prison':                                                       'Jail, prison or juvenile detention facility (HUD)',
    'Jail':                                                         'Jail, prison or juvenile detention facility (HUD)',
    'jail, prison, or juvenile facility (hud)':                     'Jail, prison or juvenile detention facility (HUD)',
    'living with family (hud)':                                     "Staying or living in a family member's room, apartment or house (HUD)",
    'living with friends (hud)':                                    "Staying or living in a friend's room, apartment or house (HUD)",
    'Living with Someone Else (like Family or Friends)':            "Staying or living in a friend's room, apartment or house (HUD)",
    'Hotel or Motel':                                               'Hotel or motel paid for without emergency shelter voucher (HUD)',
    'hotel/motel without emergency shelter':                        'Hotel or motel paid for without emergency shelter voucher (HUD)',
    'Foster Care Home':                                             'Foster care home or foster care group home (HUD)',
    'Anywhere Outside (like Streets, Parks, etc.)':                 "Place not meant for habitation inclusive of 'non-housing service site(outreach programs only)'(HUD)",
    'A Car or Other Vehicle':                                       "Place not meant for habitation inclusive of 'non-housing service site(outreach programs only)'(HUD)",
    'An Abandoned Building':                                        "Place not meant for habitation inclusive of 'non-housing service site(outreach programs only)'(HUD)",
    'At a Transportation Center (like Bus Station, Airport, etc.)': "Place not meant for habitation inclusive of 'non-housing service site(outreach programs only)'(HUD)",
    'Subsidized Housing':                                           'Rental by client, with other (non-VASH) housing subsidy (HUD)',
    'Public Housing - Non-lease Holder':                            'Rental by client, with other (non-VASH) housing subsidy (HUD)',
    'Public Housing-Lease Holder (CHA)':                            'Rental by client, with other (non-VASH) housing subsidy (HUD)',
    'Subsidized Rental Housing/Section 8':                          'Rental by client, with other (non-VASH) housing subsidy (HUD)',
    'Unsubsidized Rental Housing':                                  'Rental by client, no housing subsidy (HUD)',
    'Recipients Rented Apartment':                                  'Rental by client, no housing subsidy (HUD)',
    'Recipients Own House or Condo':                                'Owned by client, no housing subsidy (HUD)',
    "Don't Know (HUD)":                                             np.NaN,
    "don't know":                                                   np.NaN,
    'Other (HUD)':                                                  np.NaN,
    'Other':                                                        np.NaN,
    'Refused (HUD)':                                                np.NaN,
    'don t know (hud)':                                             np.NaN,
    'refused':                                                      np.NaN,
    'Domestic Violence Situation':                                  np.NaN,
    'Second Stage Shelter':                                         np.NaN}

master_length_of_stay_in_previous_living_situation_replacements = {'More than one year':       'One year or longer (HUD)',
                                                                   'Seven months to one year': 'More than three months, but less than one year (HUD)',
                                                                   'Two to three months':      'One to three months (HUD)',
                                                                   'Three weeks to one month': 'More than one week, but less than one month (HUD)',
                                                                   'Less than one week':       'One week or less (HUD)',
                                                                   'One to two weeks':         'More than one week, but less than one month (HUD)',
                                                                   'Four to six months':       'More than three months, but less than one year (HUD)',
                                                                   "Don't Know (HUD)":         np.NaN,
                                                                   'Refused (HUD)':            np.NaN,
                                                                   'don t know':               np.NaN}

def first_entry(ma):
    """Given `master_all` or a subset thereof, get info about the first entry in a program for each `EntryID`.

    :param ma: `master_all` or a subset thereof.
    :type ma: pandas.Dataframe.

    """
    # sort `ma` by `ProgramEntryDate` and get the first entry for a given `ClientUniqueID`
    first_ma = ma.sort('ProgramEntryDate', inplace=False).groupby('ClientUniqueID').first()
    # merge the firsts back into the dataframe
    # XXX this can be engineered so that there are fewer columns, (and less memory,) involved
    ma_first_ma = pd.merge(ma, first_ma, left_on='ClientUniqueID', right_index=True, suffixes=('','OfFirstEntry'))
    # compute `DaysSinceFirstEntry`
    ma_first_ma['DaysSinceFirstEntry'] = (ma_first_ma['ProgramEntryDate'] - ma_first_ma['ProgramEntryDateOfFirstEntry']).map(get_days_geq_0)
    # only return the important columns, including `EntryID` for merging
    return ma_first_ma[['EntryID','ProgramEntryDateOfFirstEntry','ProgramTypeOfFirstEntry','DaysSinceFirstEntry']]

def get_days_since_first_entry_bucket(d):
    """Return the days-since-first-entry bucket.

    :param d: Days.
    :type d: int.

    """
    if d < 1:
        return '0 days'
    elif d <= 7:
        return 'One week or less'
    elif d < 30:
        return 'More than one week, but less than one month'
    elif d <= 90:
        return 'One to three months'
    elif d < 365:
        return 'More than three months, but less than one year'
    else:
        return 'One year or longer'

master_destination_at_exit_replacements = {
    'Emergency shelter':                                            'Emergency shelter, including hotel or motel paid for with emergency shelter voucher (HUD)',
    'Runaway facility':                                             'Emergency shelter, including hotel or motel paid for with emergency shelter voucher (HUD)',
    'Transitional housing for homeless persons':                    'Transitional housing for homeless persons (including homeless youth) (HUD)',
    'transitional: transitional housing for homeless':              'Transitional housing for homeless persons (including homeless youth) (HUD)',
    'Other support housing':                                        'Permanent supportive housing for formerly homeless persons(such as SHP, S+C, or SRO Mod Rehab)(HUD)',
    'Other: Other supportive housing':                              'Permanent supportive housing for formerly homeless persons(such as SHP, S+C, or SRO Mod Rehab)(HUD)',
    'Permanent: Shelter Plus Care':                                 'Permanent supportive housing for formerly homeless persons(such as SHP, S+C, or SRO Mod Rehab)(HUD)',
    'Psychiatric facility':                                         'Psychiatric hospital or other psychiatric facility (HUD)',
    'Inpatient alcohol or other drug treatment facility':           'Substance abuse treatment facility or detox center (HUD)',
    'Substance abuse treatment facility':                           'Substance abuse treatment facility or detox center (HUD)',
    'Hospital':                                                     'Hospital (non-psychiatric) (HUD)',
    'Jail':                                                         'Jail, prison or juvenile detention facility (HUD)',
    'institution: jail/prison':                                     'Jail, prison or juvenile detention facility (HUD)',
    'institution: inpatient alcohol/drug facility':                 'Jail, prison or juvenile detention facility (HUD)',
    'Prison':                                                       'Jail, prison or juvenile detention facility (HUD)',
    'Juvenile detention center':                                    'Jail, prison or juvenile detention facility (HUD)',
    'Rental house or apartment (no subsidy)':                       'Rental by client, no housing subsidy (HUD)',
    'permanent: rental house/apartment (no subsidy)':               'Rental by client, no housing subsidy (HUD)',
    'Rental room/house/apartment':                                  'Rental by client, no housing subsidy (HUD)',
    'Own house/apartment':                                          'Owned by client, no housing subsidy (HUD)',
    'Homeownership':                                                'Owned by client, no housing subsidy (HUD)',
    'Staying in a family members room/apartment':                   'Staying or living with family, temporary tenure (e.g., room, apartment or house)(HUD)',
    'Residence with family or friends':                             'Staying or living with friends, temporary tenure (e.g., room apartment or house)(HUD)',
    "Staying in a friend's room/apartment/house":                   'Staying or living with friends, temporary tenure (e.g., room apartment or house)(HUD)',
    'Transitional: Moved in with family/friends':                   'Staying or living with friends, temporary tenure (e.g., room apartment or house)(HUD)',
    'Foster care home':                                             'Foster care home or foster care group home (HUD)',
    'Child care residential institution':                           'Foster care home or foster care group home (HUD)',
    'Anywhere outside':                                             'Place not meant for habitation (e.g., a vehicle or anywhere outside) (HUD)',
    'Places not meant for human habitation (e.g street)':           'Place not meant for habitation (e.g., a vehicle or anywhere outside) (HUD)',
    'Other subsidized house or apartment':                          'Rental by client, other (non-VASH) housing subsidy (HUD)',
    'HOME subsidized house or apartment':                           'Rental by client, other (non-VASH) housing subsidy (HUD)',
    'permanent: moved in with family/friends':                      'Staying or living with friends, permanent tenure (HUD)',
    'Moved in with family or friends':                              'Staying or living with friends, permanent tenure (HUD)',
    'Deceased':                                                     np.NaN,
    "Don't Know (HUD)":                                             np.NaN,
    'Unknown':                                                      np.NaN,
    'Other (HUD)':                                                  np.NaN,
    'other':                                                        np.NaN,
    'Refused (HUD)':                                                np.NaN,
    'Returning to State of Origin':                                 np.NaN,
    'Deceased (HUD)':                                               np.NaN,
    'Shelter Plus Care':                                            np.NaN,
    'Section 8':                                                    np.NaN,
    'Public Housing':                                               np.NaN,
    'Permanent':                                                    np.NaN,
    'Permanent: Section 8':                                         np.NaN,
    'Residence with other parent':                                  np.NaN}

master_case_outcomes = {'Owned by client, no housing subsidy (HUD)':                                                           'Permanent',
                        'Staying or living with friends, permanent tenure (HUD)':                                              'Permanent',
                        'Staying or living with family, permanent tenure (HUD)':                                               'Permanent',
                        'Jail, prison or juvenile detention facility (HUD)':                                                   'Institutional',
                        'Rental by client, no housing subsidy (HUD)':                                                          'Permanent',
                        'Staying or living with family, temporary tenure (e.g., room, apartment or house)(HUD)':               'Temporary',
                        'Emergency shelter, including hotel or motel paid for with emergency shelter voucher (HUD)':           'Temporary',
                        'Rental by client, other (non-VASH) housing subsidy (HUD)':                                            'Permanent',
                        'Hospital (non-psychiatric) (HUD)':                                                                    'Institutional',
                        'Transitional housing for homeless persons (including homeless youth) (HUD)':                          'Temporary',
                        'Rental by client, VASH Subsidy (HUD)':                                                                'Permanent',
                        'Psychiatric hospital or other psychiatric facility (HUD)':                                            'Institutional',
                        'Staying or living with friends, temporary tenure (e.g., room apartment or house)(HUD)':               'Temporary',
                        'Permanent supportive housing for formerly homeless persons(such as SHP, S+C, or SRO Mod Rehab)(HUD)': 'Permanent',
                        'Substance abuse treatment facility or detox center (HUD)':                                            'Institutional',
                        'Hotel or motel paid for without emergency shelter voucher (HUD)':                                     'Temporary',
                        'Owned by client, with housing subsidy (HUD)':                                                         'Permanent',
                        'Safe Haven (HUD)':                                                                                    'Temporary',
                        'Place not meant for habitation (e.g., a vehicle or anywhere outside) (HUD)':                          'Temporary',
                        'Foster care home or foster care group home (HUD)':                                                    'Institutional',
                        np.NaN:                                                                                                np.NaN}

psh_permanent_tenure = 180

def psh_case_outcome(row):
    """Given a row in PSH, compute the `CaseOutcome`.  This is complicated because we have to consider whether someone
    was in PSH for at least 6 months, (`psh_permanent_tenure`).

    :param row: A row from `master`.
    :type row: dict-like.

    """
    # if we have `LengthOfStay`, use it
    if pd.notnull(row['LengthOfStay']):
        if row['LengthOfStay'] > psh_permanent_tenure:
            return 'Permanent'
        else: # in for less than psh_permanent_tenure
            return master_case_outcomes[row['DestinationAtExit']]
    # we don't have LengthOfStay, but we have ProgramEntryDate,
    # so we can see if they entered >`psh_permanent_tenure` before when we got the data, (`dump_date`).
    elif pd.notnull(row['ProgramEntryDate']):
        if row['ProgramEntryDate'] < dump_date - dateutil.relativedelta.relativedelta(days=psh_permanent_tenure):
            return 'Permanent'
        else: # in for less than psh_permanent_tenure
            return master_case_outcomes[row['DestinationAtExit']]
    else: # no LengthOfStay, no ProgramEntryDate
        return master_case_outcomes[row['DestinationAtExit']]

def get_case_outcome(row):
    """Given a row, compute the `CaseOutcome`.  If the row is PSH, delegate to :func:`psh_case_outcome`; otherwise, just
    use `DestinationAtExit`.

    :param row: A row from `master`.
    :type row: dict-like.

    """
    if row['ProgramType'] == 'Permanent supportive housing (HUD)':
        return psh_case_outcome(row)
    else:
        return master_case_outcomes[row['DestinationAtExit']]

def get_reentries(df):
    """Given `master` or a subset thereof, find the next entry into a "Homelessness Program" for each exit.

    :param df: `master`.
    :type df: pandas.Dataframe.

    """
    # just get the rows that exited, and get the important columns
    df_exits = df[pd.notnull(df['ProgramExitDate'])][['ClientUniqueID','ProgramExitDate']]
    # just get the rows that entered into a homelessness program, and get the columns that are important for reentry
    df_entries = df[df['HomelessnessProgram?'] == True][['ClientUniqueID','ProgramEntryDate','ProgramType']]
    # merge on ClientUniqueID to get the cross product of all exits and entries on ClientUniqueID
    df_ee = pd.merge(df_exits, df_entries, on='ClientUniqueID', how='right')
    # build a mask for all entries that happened after exits
    df_reentered = df_ee[df_ee['ProgramExitDate'] < df_ee['ProgramEntryDate']]
    r_columns = ['ClientUniqueID','ProgramExitDate','ProgramEntryDate','ProgramType']
    # return the *next* reentry for each exit
    return df_reentered.sort('ProgramEntryDate', inplace=False).groupby(['ClientUniqueID','ProgramExitDate']).head(1)[r_columns]

def get_delta_reentries(df, delta):
    """Given `master` or a subset thereof, compute which rows reentered within the given timedelta.

    :param df: `master`.
    :type df: pandas.Dataframe.
    :param delta: the timedelta to consider.
    :type delta: numpy.timedelta64.

    """
    # get only the rows that exited delta before the dump_date
    exited_before_dump_minus_delta  = pd.notnull(df['ProgramExitDate']) & (df['ProgramExitDate'] + delta < dump_date)
    # compute reentry before delta and return only to rows that meet the above criteria
    reentered_before_delta = pd.notnull(df['ProgramEntryDateReentry']) & (df['ProgramExitDate'] + delta > df['ProgramEntryDateReentry'])
    return reentered_before_delta[exited_before_dump_minus_delta]

def deduplicate_entry_id(df):
    """Given `master`, drop duplicates on EntryID, making sure to take the one with a `Relationship to HoH`.
    
    From the Chicago Alliance:

    There are 23 duplicated EntryIDs.  One has a populated Relationship to HoH,
    and one does not. Take the record with the relationship field populated.

    There is one exception: EntryID 329811 has both Son and Daughter in its two
    records. It should be associated with a Daughter. Get rid of the Son record.

    XXX since we're not differentiating Son & Daughter, we can just drop one of
    them.

    :param df: `master`.
    :type df: pandas.Dataframe.

    """
    # get the duplicated rows
    duplicated = df[df.duplicated('EntryID')]['EntryID'].values
    # only keep the rows that are not duplicated or that have a `Relationship to HoH`
    df = df[(df['EntryID'].apply(lambda i: i not in duplicated)) | (df['Relationship to HoH'].notnull())]
    df = df.drop_duplicates('EntryID')

    return df

def get_program_type(row):
    """Get the `ProgramType`, `ProgramTypeAggregate`, and `HomelessnessProgram?` from `ProgramTypeCode` and
    `AltProgramType`.

    :param row: A row from `master`.
    :type row: dict-like.

    """
    return row['AltProgramType'] if pd.notnull(row['AltProgramType']) else row['ProgramTypeCode']

providers_street_outreach = ['Heartland Health Outreach Pathways Home Outpatient(533)',
                             'Matthew House, Inc. - Diaconia(352)',
                             'Thresholds, Inc. Mobile Assessment Outreach(506)']

providers_program_type_aggregates = {'Interim':                    'Transitional housing (HUD)',
                                     'PHwSS':                      'Transitional housing (HUD)'}

providers_homelessness_programs = ['Interim',
                                   'Emergency Shelter (HUD)',
                                   'Supportive Services for Veteran Families',
                                   'PHwSS',
                                   'Transitional housing (HUD)',
                                   'Street Outreach']

disability_type_replacements = {'Chronic Health Condition': 'Physical (HUD 40118)',
                                'Physical/Medical (HUD 40118)': 'Physical (HUD 40118)',
                                'Vision Impaired': 'Physical (HUD 40118)',
                                'Hearing Impaired': 'Physical (HUD 40118)',
                                'Other': 'Physical (HUD 40118)',
                                'Dual Diagnosis': 'Both alcohol and drug abuse (HUD 40118)'}

disability_types = ['Mental Health Problem (HUD 40118)',
                    'Physical (HUD 40118)',
                    'Drug Abuse (HUD 40118)',
                    'HIV/AIDS (HUD 40118)',
                    'Alcohol Abuse (HUD 40118)',
                    'Both alcohol and drug abuse (HUD 40118)',
                    'Developmental (HUD 40118)']

disability_types_entry = [d+' Entry' for d in disability_types]
disability_types_review = [d+' Review' for d in disability_types]

def get_disabilities(df_name):
    """Given either 'entry_disabilities' or 'review_disabilities', compute a pivot table of disabilities.

    :param df_name: the name of the dataframe, either 'entry_disabilities' or 'review_disabilities'
    :type df_name: str.

    """
    df = load_clean(df_name)
    df = df[['EntryID','DisabilityType']].drop_duplicates()
    df['value'] = True
    return pd.pivot_table(df, values='value', index='EntryID', columns='DisabilityType')

income_replacements = {'Employment amount':                              'Earned Income (HUD)',
                       'Self Employment Wages':                          'Earned Income (HUD)',
                       "Veteran 's Pension (HUD)":                       "Veteran's Pension (HUD)",
                       'Alimony':                                        'Alimony or Other Spousal Support (HUD)',
                       'SSI/P3':                                         'SSI (HUD)',
                       'Pension/Retirement':                             'Pension From a Former Job (HUD)',
                       'Family/Friend Regular Support':                  'Contributions From Other People',
                       'Annuities':                                      'Pension From a Former Job (HUD)',
                       'Railroad Retirement':                            'Pension From a Former Job (HUD)',
                       'Food Stamps (HUD)':                              np.NaN,
                       'Participate in Kid Care insurance':              np.NaN,
                       'State Disability':                               np.NaN,
                       'Aged, Blind & Disabled':                         np.NaN,
                       'Other (HUD)':                                    np.NaN,
                       'No Financial Resources (HUD)':                   np.NaN}

income_types = ['Alimony or Other Spousal Support (HUD)',
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

income_types_exit = ['Alimony or Other Spousal Support (HUD) Exit',
                     'Child Support (HUD) Exit',
                     'Contributions From Other People Exit',
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
                     'Dividends (Investments) Exit']

def get_income(df_name):
    """Given either 'entry_income' or 'exit_income', compute a pivot table of incomes.

    :param df_name: the name of the dataframe, either 'entry_income' or 'exit_income'
    :type df_name: str.

    """
    df = load_clean(df_name)
    # sort by start date, and only take the most recent entry for a given `SourceOfIncome`
    df.sort('StartDate', inplace=True)
    df = df.groupby(['EntryID','SourceOfIncome']).last()['Last30DayIncome'].reset_index()
    df_granular = pd.pivot_table(df, values='Last30DayIncome', index='EntryID', columns='SourceOfIncome')
    df_total = df.groupby('EntryID').sum()
    return df_granular, df_total

def get_income_bucket(dollars):
    """Return the income bucket.

    :param dollars: Income.
    :type dollars: int.

    """
    if pd.isnull(dollars):
        return np.NaN
    elif dollars == 0:
        return 'Zero dollars'
    elif dollars <= 500:
        return '1 to 500 dollars'
    elif dollars <= 1000:
        return '501 to 1000 dollars'
    elif dollars <= 2000:
        return '1001 to 2000 dollars'
    elif dollars <= 3000:
        return '2001 to 3000 dollars'
    else:
        return '3001 dollars and over'

ncb_replacements = {'Other Source (HUD)':                 np.NaN,
                    'Other TANF-Funded Services (HUD)':   np.NaN,
                    'TANF Child Care Services (HUD)':     np.NaN,
                    'TANF Transportation Services (HUD)': np.NaN,
                    'No Financial Resources (HUD)':       np.NaN,
                    "Veteran 's Pension (HUD)":           np.NaN,
                    'SSDI (HUD)':                         np.NaN,
                    'TANF (HUD)':                         np.NaN,
                    'SSI/P3':                             np.NaN,
                    'Employment amount':                  np.NaN}

ncb_types = ['MEDICAID (HUD)',
             'MEDICARE (HUD)',
             'SCHIP (HUD)',
             'Section 8, Public Housing or rental assistance (HUD)',
             'Special Supplemental Nutrition Program for WIC (HUD)',
             'Supplemental Nutrition Assistance Program (Food Stamps) (HUD)',
             'Temporary rental assistance (HUD)',
             "Veteran's Administration (VA) Medical Services (HUD)"]

ncb_types_exit = [n+' Exit' for n in ncb_types]

def get_ncb(df_name):
    """Given either 'entry_ncb' or 'exit_ncb', compute a pivot table of ncbs.

    :param df_name: the name of the dataframe, either 'entry_ncb' or 'exit_ncb'
    :type df_name: str.

    """
    df = load_clean(df_name)
    # deduplicate
    df = df[['EntryID','SourceOfNonCashBenefit']].drop_duplicates()
    df['value'] = True
    return pd.pivot_table(df, values='value', index='EntryID', columns='SourceOfNonCashBenefit')

review_details_housing_status_nans = ["Don't Know (HUD)", 'Refused (HUD)']

review_details_housing_status_aggregates = {'Stably housed (HUD)':                                       'Stably housed',
                                            'Literally Homeless (HUD)':                                  'Literally Homeless',
                                            'Unstably housed and at-risk of losing their housing (HUD)': 'Unstably housed',
                                            'Imminently losing their housing (HUD)':                     'Unstably housed',
                                            np.NaN:                                                      np.NaN}

service_types = ['B Service', 'D Service', 'F Service', 'H Service', 'L Service', 'N Service', 'P Service', 'R Service', 'T Service']

def get_services(df):
    """Given either `master` as a dataframe, get the pivot table of services that client received during their stay.

    :param df: `master`.
    :type df: pandas.Dataframe.

    """
    # load services
    s = load_clean('services')
    # merge services into `df`
    dfs = pd.merge(df, s, on='ClientID', how='right')
    # only keep services that fall between the entry and exit dates
    dfs = dfs[(dfs['ProgramEntryDate'] <= dfs['ServiceStartDate']) & (dfs['ServiceStartDate'] < dfs['ProgramExitDate'])]
    dfs['value'] = True
    # pivot out the services and return
    return pd.pivot_table(dfs, values='value', index=['EntryID'], columns='ServiceTypeL1')

def print_usage():
    print "clean.py"
    print "Usage: python clean.py DFNAME"
    print
    print "Clean the given DFNAME into ./clean/"

if __name__ == "__main__":
    """Given the data frame name, load the raw data and cleaned dependencies, clean the raw data, and save it as a CSV
    and a pickle.  This should be in the form `entry_details`, not `EntryDetails`.

    """
    if len(sys.argv) != 2:
        print_usage()
    else:
        clean(sys.argv[1])
