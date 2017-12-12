# Defines a dictionary of file headers per file type.
# Headers not in this list are truncated from final output

# Note: Headers valid for ACS 2016 Data

# Top Level: [DP02, DP03, DP05] Indicates the prefix of the summary file
# Inner Levels - List of tuples:
#   [0]: Four character identifier
#   [1]: (P)ercentage or (E)stimate
#   [2]: Friendly name

FILE_HEADERS = {
    'DP02': [
        ('VC03','E','TotalHH'),
        ('VC04','P','FamilyHH'),
        ('VC17','P','HHWithUnder18'),
        ('VC18','P','HHWith65Plus'),
        ('VC21','E','AvgHHSize'),
        ('VC77','P','EnrollmentPreK'),
        ('VC78','P','EnrollmentK'),
        ('VC79','P','EnrollmentElem'),
        ('VC80','P','EnrollmentHS'),
        ('VC81','P','EnrollmentCollege'),
        ('VC86','P','EduElem'),
        ('VC87','P','EduPartialHS'),
        ('VC88','P','EduHS'),
        ('VC89','P','EduSomeCollege'),
        ('VC90','P','EduAssociate'),
        ('VC91','P','EduBachelors'),
        ('VC92','P','EduGraduate'),
        ('VC101','P','PopVetStatus'),
        ('VC106','P','PopDisabledStatus'),
        ('VC121','P','ResidenceDiffUS'),
        ('VC126','P','ResidenceDiffAbroad'),
        ('VC132','P','BornNativeUS'),
        ('VC136','P','BornAbroad'),
        ('VC171','P','LanguageEnglishOnly'),
        ('VC174','P','LanguageSpanish'),
        ('VC178','P','LanguageAsian'),
        ('VC180','P','LanguageOther'),
        ('VC217','P','HHWithComputer'),
        ('VC218','P','HHWithBroadband')
    ],
    'DP03': [
        ('VC05','P','LaborCivilian'),
        ('VC08','P','LaborArmedForces'),
        ('VC12','P','LaborUnempRate'),
        ('VC50','P','IndustryAgMining'),
        ('VC51','P','IndustryConstruction'),
        ('VC52','P','IndustryManufacture'),
        ('VC53','P','IndustryWholesale'),
        ('VC54','P','IndustryRetail'),
        ('VC55','P','IndustryTransport'),
        ('VC56','P','IndustryInfo'),
        ('VC57','P','IndustryFinance'),
        ('VC58','P','IndustryProfessional'),
        ('VC59','P','IndustryEduHealth'),
        ('VC60','P','IndustryEnter'),
        ('VC61','P','IndustryOther'),
        ('VC62','P','IndustryPubAdmin'),
        ('VC68','P','PayrollGovt'),
        ('VC67','P','PayrollPrivate'),
        ('VC69','P','PayrollSelfEmp'),
        ('VC75','P','IncomeUnder10k'),
        ('VC76','P','Income10to14k'),
        ('VC77','P','Income15to24k'),
        ('VC78','P','Income25to34k'),
        ('VC79','P','Income35to49k'),
        ('VC80','P','Income50to74k'),
        ('VC81','P','Income75to99k'),
        ('VC82','P','Income100to149k'),
        ('VC83','P','Income150to199k'),
        ('VC84','P','Income200k'),
        ('VC85','E','IncomeMedianHH'),
        ('VC91','P','IncomeSocialSec'),
        ('VC93','P','IncomeRetirement'),
        ('VC97','P','IncomeSSI'),
        ('VC99','P','IncomePublicAssist'),
        ('VC101','P','IncomeSnap'),
        ('VC118','E','IncomePerCapita'),
        ('VC132','P','InsurancePrivate'),
        ('VC133','P','InsurancePublic'),
        ('VC134','P','InsuranceNone'),
        ('VC161','P','IncomeBelowPoverty')

    ], 
    'DP05': [
        ('VC04','P','PopMale'),
        ('VC08','P','AgeUnder5'),
        ('VC09','P','Age5to9'),
        ('VC10','P','Age10to14'),
        ('VC11','P','Age15to19'),
        ('VC12','P','Age20to24'),
        ('VC13','P','Age25to34'),
        ('VC14','P','Age35to44'),
        ('VC15','P','Age45to54'),
        ('VC16','P','Age55to59'),
        ('VC17','P','Age60to64'),
        ('VC18','P','Age65to74'),
        ('VC19','P','Age75to84'),
        ('VC20','P','Age85Plus'),
        ('VC23','E','AgeMedian'),
        ('VC49','P','RaceWhite'),
        ('VC50','P','RaceBlack'),
        ('VC51','P','RaceNative'),
        ('VC56','P','RaceAsian'),
        ('VC64','P','RacePacific'),
        ('VC69','P','RaceOther'),
        ('VC70','P','RaceMixed'),
        ('VC88','P','PopHispanic')

    ]
}

# Mapping for P or E

HEADER_MAP = {
    'P': 'HC03',
    'E': 'HC01'
}