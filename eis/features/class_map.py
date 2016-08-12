import numpy as np
import pdb
import pandas as pd
import yaml
import logging
import sys
import datetime

from . import officers
from . import dispatches

log = logging.getLogger(__name__)


class UnknownFeatureError(Exception):
    def __init__(self, feature):
        self.feature = feature

    def __str__(self):
        return "Unknown feature: {}".format(self.feature)

def find_categorical_features(feature_list):
    """Given a list of feature names return the names of the
    features which are categorical

    Args:
        feature_list(list): list of feature names to check

    Returns:
        categorical_features(list): the features which are categorical
    """

    # TODO: make it so that we don't need to supply a bogus fake today to instantiate an OfficerFeature
    dummy_kwargs = {'to_date': '', 'from_date': '', 'fake_today':datetime.datetime.today(), 'table_name':'dummy_table'}
    feature_classes = [lookup(feature, **dummy_kwargs) for feature in feature_list]

    categorical_features = [feature.feature_name for feature in feature_classes if feature.is_categorical]

    return categorical_features


def find_label_features(feature_list):
    """Given a list of feature names return the names of the
    features which are labels

    Args:
        feature_list(list): list of feature names to check

    Returns:
        label_features(list): the features which are labels
    """

    # TODO: make it so that we don't need to supply a bogus fake today to instantiate an OfficerFeature
    dummy_kwargs = {'to_date': '', 'from_date': '', 'fake_today':datetime.datetime.today(), 'table_name':'dummy_table'}
    feature_classes = [lookup(feature, **dummy_kwargs) for feature in feature_list]

    label_features = [feature.feature_name for feature in feature_classes if feature.is_label]

    return label_features

def lookup(feature, **kwargs):

    if feature[1:3] == "yr":
        kwargs["feat_time_window"] = int(feature[0])
    else:
        kwargs["feat_time_window"] = 15

    dict_lookup = { 'AcademyScore': officers.AcademyScore(**kwargs),
                    'ArrestCount1Yr': officers.ArrestCount1Yr(**kwargs),
                    'ArrestCountCareer': officers.ArrestCountCareer(**kwargs),
                    'DivorceCount': officers.DivorceCount(**kwargs),
                    'SustainedRuleViolations': officers.SustainedRuleViolations(**kwargs),
                    'IncidentCount': officers.IncidentCount(**kwargs),
                    'MeanHoursPerShift': officers.MeanHoursPerShift(**kwargs),
                    'MilesFromPost': officers.MilesFromPost(**kwargs),
                    'OfficerGender': officers.OfficerGender(**kwargs),
                    'TimeGatedDummyFeature': officers.TimeGatedDummyFeature(**kwargs),
                    'OfficerRace': officers.OfficerRace(**kwargs),
                    'AllAllegations': officers.AllAllegations(**kwargs),
                    'LabelSustained': dispatches.LabelSustained(**kwargs),
                    'LabelUnjustified': dispatches.LabelUnjustified(**kwargs),
                    'LabelPreventable': dispatches.LabelPreventable(**kwargs),
                    'DispatchHour': dispatches.DispatchHour(**kwargs),
                    'DispatchDayOfWeek': dispatches.DispatchDayOfWeek(**kwargs),
                    'DispatchMonth': dispatches.DispatchMonth(**kwargs),
                    'DispatchYearQuarter': dispatches.DispatchYearQuarter(**kwargs),
                    'DispatchYear': dispatches.DispatchYear(**kwargs),
                    'DispatchMinute': dispatches.DispatchMinute(**kwargs),
                    'OriginalPriority': dispatches.OriginalPriority(**kwargs),
                    'DispatchType': dispatches.DispatchType(**kwargs),
                    'DispatchSubType': dispatches.DispatchSubType(**kwargs),
                    'NumberOfUnitsAssigned': dispatches.NumberOfUnitsAssigned(**kwargs),
                    'ArrestsInPast1Hour': dispatches.ArrestsInPast1Hour(**kwargs),
                    'ArrestsInPast6Hours': dispatches.ArrestsInPast6Hours(**kwargs),
                    'ArrestsInPast12Hours': dispatches.ArrestsInPast12Hours(**kwargs),
                    'ArrestsInPast24Hours': dispatches.ArrestsInPast24Hours(**kwargs),
                    'ArrestsInPast48Hours': dispatches.ArrestsInPast48Hours(**kwargs),
                    'ArrestsInPastWeek': dispatches.ArrestsInPastWeek(**kwargs),
                    'FelonyArrestsInPast1Hour': dispatches.FelonyArrestsInPast1Hour(**kwargs),
                    'FelonyArrestsInPast6Hours': dispatches.FelonyArrestsInPast6Hours(**kwargs),
                    'FelonyArrestsInPast12Hours': dispatches.FelonyArrestsInPast12Hours(**kwargs),
                    'FelonyArrestsInPast24Hours': dispatches.FelonyArrestsInPast24Hours(**kwargs),
                    'FelonyArrestsInPast48Hours': dispatches.FelonyArrestsInPast48Hours(**kwargs),
                    'FelonyArrestsInPastWeek': dispatches.FelonyArrestsInPastWeek(**kwargs),
                    'OfficersDispatchedInPast1Minute': dispatches.OfficersDispatchedInPast1Minute(**kwargs),
                    'OfficersDispatchedInPast15Minutes': dispatches.OfficersDispatchedInPast15Minutes(**kwargs),
                    'OfficersDispatchedInPast30Minutes': dispatches.OfficersDispatchedInPast30Minutes(**kwargs),
                    'OfficersDispatchedInPast1Hour': dispatches.OfficersDispatchedInPast1Hour(**kwargs),
                    'OfficersDispatchedAverageUnjustifiedIncidentsInPastYear': dispatches.OfficersDispatchedAverageUnjustifiedIncidentsInPastYear(**kwargs),
                    'OfficersDispatchedAverageJustifiedIncidentsInPastYear': dispatches.OfficersDispatchedAverageJustifiedIncidentsInPastYear(**kwargs),
                    'OfficersDispatchedAverageSustainedAllegationsInPastYear': dispatches.OfficersDispatchedAverageSustainedAllegationsInPastYear(**kwargs),
                    'OfficersDispatchedAverageUnsustainedAllegationsInPastYear': dispatches.OfficersDispatchedAverageUnsustainedAllegationsInPastYear(**kwargs),
                    'OfficersDispatchedAveragePreventableIncidentsInPastYear': dispatches.OfficersDispatchedAveragePreventableIncidentsInPastYear(**kwargs),
                    'OfficersDispatchedAverageNonPreventableIncidentsInPastYear': dispatches.OfficersDispatchedAverageNonPreventableIncidentsInPastYear(**kwargs),
                    'OfficersDispatchedAverageUnjustifiedIncidentsInPast6Months': dispatches.OfficersDispatchedAverageUnjustifiedIncidentsInPast6Months(**kwargs),
                    'OfficersDispatchedAverageJustifiedIncidentsInPast6Months': dispatches.OfficersDispatchedAverageJustifiedIncidentsInPast6Months(**kwargs),
                    'OfficersDispatchedAverageSustainedAllegationsInPast6Months': dispatches.OfficersDispatchedAverageSustainedAllegationsInPast6Months(**kwargs),
                    'OfficersDispatchedAverageUnsustainedAllegationsInPast6Months': dispatches.OfficersDispatchedAverageUnsustainedAllegationsInPast6Months(**kwargs),
                    'OfficersDispatchedAveragePreventableIncidentsInPast6Months': dispatches.OfficersDispatchedAveragePreventableIncidentsInPast6Months(**kwargs),
                    'OfficersDispatchedAverageNonPreventableIncidentsInPast6Months': dispatches.OfficersDispatchedAverageNonPreventableIncidentsInPast6Months(**kwargs),
                    'OfficersDispatchedAverageUnjustifiedIncidentsInPast1Month': dispatches.OfficersDispatchedAverageUnjustifiedIncidentsInPast6Months(**kwargs),
                    'OfficersDispatchedAverageJustifiedIncidentsInPast1Month': dispatches.OfficersDispatchedAverageJustifiedIncidentsInPast1Month(**kwargs),
                    'OfficersDispatchedAverageSustainedAllegationsInPast1Month': dispatches.OfficersDispatchedAverageSustainedAllegationsInPast1Month(**kwargs),
                    'OfficersDispatchedAverageUnsustainedAllegationsInPast1Month': dispatches.OfficersDispatchedAverageUnsustainedAllegationsInPast1Month(**kwargs),
                    'OfficersDispatchedAveragePreventableIncidentsInPast1Month': dispatches.OfficersDispatchedAveragePreventableIncidentsInPast1Month(**kwargs),
                    'OfficersDispatchedAverageNonPreventableIncidentsInPast1Month': dispatches.OfficersDispatchedAverageNonPreventableIncidentsInPast1Month(**kwargs),
                    'MedianAgeInCT': dispatches.MedianAgeInCT(**kwargs),
                    'MedianAgeOfMenInCT': dispatches.MedianAgeOfMenInCT(**kwargs),
                    'MedianAgeOfWomenInCT': dispatches.MedianAgeOfWomenInCT(**kwargs),
                    'UnweightedSampleCountOfPopulationInCT': dispatches.UnweightedSampleCountOfPopulationInCT(**kwargs),
                    'UnweightedSampleCountOfHousingUnitsInCT': dispatches.UnweightedSampleCountOfHousingUnitsInCT(**kwargs),
                    'PercentageWomenInCT': dispatches.PercentageWomenInCT(**kwargs),
                    'PercentageMenInCT': dispatches.PercentageMenInCT(**kwargs),
                    'PercentageWhiteInCT': dispatches.PercentageWhiteInCT(**kwargs),
                    'PercentageBlackInCT': dispatches.PercentageBlackInCT(**kwargs),
                    'PercentageAsianInCT': dispatches.PercentageAsianInCT(**kwargs),
                    'PercentageHispanicInCT': dispatches.PercentageHispanicInCT(**kwargs),
                    'PercentageForeignBornInCT': dispatches.PercentageForeignBornInCT(**kwargs),
                    'ProportionOfPopulationUnderAge18InCT': dispatches.ProportionOfPopulationUnderAge18InCT(**kwargs),
                    'ProportionOfPopulationEnrolledInSchoolInCT': dispatches.ProportionOfPopulationEnrolledInSchoolInCT(**kwargs),
                    'ProportionOfPopulationOver25WithLessThanHighSchoolEducationInCT': dispatches.ProportionOfPopulationOver25WithLessThanHighSchoolEducationInCT(**kwargs),
                    'ProportionOfPopulationVeteransInCT': dispatches.ProportionOfPopulationVeteransInCT(**kwargs),
                    'ProportionOfPopulationWithIncomeBelowPovertyLevelInPastYearInCT': dispatches.ProportionOfPopulationWithIncomeBelowPovertyLevelInPastYearInCT(**kwargs),
                    'ProportionOfPopulationWithIncomeInPast12MonthsBelow45000DollarsInCT': dispatches.ProportionOfPopulationWithIncomeInPast12MonthsBelow45000DollarsInCT(**kwargs),
                    'MedianIncomeInPast12MonthsInCT': dispatches.MedianIncomeInPast12MonthsInCT(**kwargs),
                    'MedianHouseholdIncomeInPast12MonthsInCT': dispatches.MedianHouseholdIncomeInPast12MonthsInCT(**kwargs),
                    'ProportionOfHouseholdsReceivingAssistanceOrFoodStampsInCT': dispatches.ProportionOfHouseholdsReceivingAssistanceOrFoodStampsInCT(**kwargs),
                    'ProportionOfHousingUnitsVacantInCT': dispatches.ProportionOfHousingUnitsVacantInCT(**kwargs),
                    'ProportionOfHousingUnitsOccupiedByOwnerInCT': dispatches.ProportionOfHousingUnitsOccupiedByOwnerInCT(**kwargs),
                    'MedianYearStructureBuildInCT': dispatches.MedianYearStructureBuildInCT(**kwargs),
                    'MedianYearRenterMovedIntoHousingUnitInCT': dispatches.MedianYearRenterMovedIntoHousingUnitInCT(**kwargs),
                    'MedianYearOwnerMovedIntoHousingUnitInCT': dispatches.MedianYearOwnerMovedIntoHousingUnitInCT(**kwargs),
                    'MedianGrossRentInCT': dispatches.MedianGrossRentInCT(**kwargs),
                    'MedianPropertyValueInCT': dispatches.MedianPropertyValueInCT(**kwargs),
                    'LowerQuartilePropertyValueInCT': dispatches.LowerQuartilePropertyValueInCT(**kwargs),
                    'UpperQuartilePropertyValueInCT': dispatches.UpperQuartilePropertyValueInCT(**kwargs),
                    'AverageHouseholdSizeInCT': dispatches.AverageHouseholdSizeInCT(**kwargs),
                    'ProportionOfChildrenUnder18LivingWithSingleParentInCT': dispatches.ProportionOfChildrenUnder18LivingWithSingleParentInCT(**kwargs),
                    'ProportionOfChildrenUnder18LivingWithMotherInCT': dispatches.ProportionOfChildrenUnder18LivingWithMotherInCT(**kwargs),
                    'ProportionOfPopulationNeverMarriedInCT': dispatches.ProportionOfPopulationNeverMarriedInCT(**kwargs),
                    'ProportionOfPopulationDivorcedOrSeparatedInCT': dispatches.ProportionOfPopulationDivorcedOrSeparatedInCT(**kwargs),
                    'ProportionOfPopulationWithoutHealthInsuranceInCT': dispatches.ProportionOfPopulationWithoutHealthInsuranceInCT(**kwargs),
                    'ProportionOfWomenWhoGaveBirthInPast12MonthsInCT': dispatches.ProportionOfWomenWhoGaveBirthInPast12MonthsInCT(**kwargs),
                    'DispatchesWithin1kmRadiusInPast15Minutes': dispatches.DispatchesWithin1kmRadiusInPast15Minutes(**kwargs),
                    'DispatchesWithin1kmRadiusInPast30Minutes': dispatches.DispatchesWithin1kmRadiusInPast30Minutes(**kwargs),
                    'DispatchesWithin1kmRadiusInPast1Hour': dispatches.DispatchesWithin1kmRadiusInPast1Hour(**kwargs),
                    'ArrestsWithin1kmRadiusInPast6Hours': dispatches.ArrestsWithin1kmRadiusInPast6Hours(**kwargs),
                    'ArrestsWithin1kmRadiusInPast12Hours': dispatches.ArrestsWithin1kmRadiusInPast12Hours(**kwargs),
                    'AverageOfficerDispatchesWithin100mRadiusIn1PastHour': dispatches.AverageOfficerDispatchesWithin100mRadiusInPast1Hour(**kwargs),
                    'AverageOfficerDispatchesWithin100mRadiusInPast6Hours': dispatches.AverageOfficerDispatchesWithin100mRadiusInPast6Hours(**kwargs),
                    'AverageOfficerDispatchesWithin100mRadiusInPast48Hours': dispatches.AverageOfficerDispatchesWithin100mRadiusInPast48Hours(**kwargs),
                    'AverageAgeOfRespondingOfficers': dispatches.AverageAgeOfRespondingOfficers(**kwargs),
                    'LowestEducationLevelAmongRespondingOfficers': dispatches.LowestEducationLevelAmongRespondingOfficers(**kwargs),
                    'HighestEducationLevelAmongRespondingOfficers': dispatches.HighestEducationLevelAmongRespondingOfficers(**kwargs),
                    'ProportionOfRespondingOfficersWithFourYearCollegeDegreeOrHigher': dispatches.ProportionOfRespondingOfficersWithFourYearCollegeDegreeOrHigher(**kwargs),
                    'ProportionOfRespondingOfficersMale': dispatches.ProportionOfRespondingOfficersMale(**kwargs),
                    'ProportionOfRespondingOfficersDivorcedOrSeparated': dispatches.ProportionOfRespondingOfficersDivorcedOrSeparated(**kwargs),
                    'ProportionOfRespondingOfficersMarried': dispatches.ProportionOfRespondingOfficersMarried(**kwargs)
                  }

    #dict_lookup = {'dummyfeature': officers.dummyfeature(**kwargs),
    #                'ArrestCount1Yr': officers.ArrestCount1Yr(**kwargs),
    #                'ArrestCountCareer': officers.ArrestCountCareer(**kwargs),
    #                'height_weight': officers.HeightWeight(**kwargs),
    #                'education': officers.Education(**kwargs),
    #                'daysexperience': officers.DaysExperience(**kwargs),
    #                'yearsexperience': officers.YrsExperience(**kwargs),
    #                'malefemale': officers.MaleFemale(**kwargs),
    #                'race': officers.Race(**kwargs),
    #                'officerage': officers.Age(**kwargs),
    #                'officerageathire': officers.AgeAtHire(**kwargs),
    #                'maritalstatus': officers.MaritalStatus(**kwargs),
    #                'numrecentarrests': officers.NumRecentArrests(**kwargs),
    #                'careerNPCarrests': officers.NPCArrests(**kwargs),
    #                '1yrNPCarrests': officers.NPCArrests(**kwargs),
    #                'careerdiscarrests': officers.DiscArrests(**kwargs),
    #                '1yrdiscarrests': officers.DiscArrests(**kwargs),
    #                'arresttod': officers.AverageTimeOfDayArrests(**kwargs),
    #                'arresteeage': officers.AvgAgeArrests(**kwargs),
    #                'disconlyarrests': officers.DiscOnlyArrestsCount(**kwargs),
    #                'arrestratedelta': officers.ArrestRateDelta(**kwargs),
    #                'arresttimeseries': officers.ArrestTimeSeries(**kwargs),
    #                'arrestcentroids': officers.ArrestCentroids(**kwargs),
    #                'careernpccitations': officers.NPCCitations(**kwargs),
    #                '1yrnpccitations': officers.NPCCitations(**kwargs),
    #                'careercitations': officers.Citations(**kwargs),
    #                '1yrcitations': officers.Citations(**kwargs),
    #                'numsuicides': officers.YearNumSuicides(**kwargs),
    #                'numjuveniles': officers.YearNumJuvenileVictim(**kwargs),
    #                'numdomesticviolence': officers.YearNumDomesticViolence(**kwargs),
    #                'numhate': officers.YearNumHate(**kwargs),
    #                'numnarcotics': officers.YearNumNarcotics(**kwargs),
    #                'numgang': officers.YearNumGang(**kwargs),
    #                'numpersweaps': officers.YearNumPersWeaps(**kwargs),
    #                'numgunknife': officers.YearNumGunKnife(**kwargs),
    #                'avgagevictims': officers.AvgAgeVictims(**kwargs),
    #                'minagevictims': officers.MinAgeVictims(**kwargs),
    #                'careerficount': officers.FICount(**kwargs),
    #                '1yrficount': officers.FICount(**kwargs),
    #                'careernontrafficficount': officers.NonTrafficFICount(**kwargs),
    #                '1yrnontrafficficount': officers.NonTrafficFICount(**kwargs),
    #                'careerhighcrimefi': officers.HighCrimeAreaFI(**kwargs),
    #                '1yrhighcrimefi': officers.HighCrimeAreaFI(**kwargs),
    #                '1yrloiterfi': officers.LoiterFI(**kwargs),
    #                'careerloiterfi': officers.LoiterFI(**kwargs),
    #                'careerblackfi': officers.CareerBlackFI(**kwargs),
    #                'careerwhitefi': officers.CareerWhiteFI(**kwargs),
    #                'avgsuspectagefi': officers.FIAvgSuspectAge(**kwargs),
    #                'avgtimeofdayfi': officers.FIAvgTimeOfDay(**kwargs),
    #                'fitimeseries': officers.FITimeseries(**kwargs),
    #                'careercadstats': officers.CADStatistics(**kwargs),
    #                '1yrcadstats': officers.CADStatistics(**kwargs),
    #                'careercadterms': officers.CountCADTerminationTypes(**kwargs),
    #                '1yrcadterms': officers.CountCADTerminationTypes(**kwargs),
    #                'careerelectivetrain': officers.ElectHoursTrain(**kwargs),
    #                '1yrelectivetrain': officers.ElectHoursTrain(**kwargs),
    #                'careerhourstrain': officers.HoursTrain(**kwargs),
    #                '1yrhourstrain': officers.HoursTrain(**kwargs),
    #                'careerworkouthours': officers.HoursPhysFit(**kwargs),
    #                '1yrworkouthours': officers.HoursPhysFit(**kwargs),
    #                'careerrochours': officers.HoursROCTrain(**kwargs),
    #                '1yrrochours': officers.HoursROCTrain(**kwargs),
    #                'careerproftrain': officers.HoursProfTrain(**kwargs),
    #                '1yrproftrain': officers.HoursProfTrain(**kwargs),
    #                'careertrafficstopnum': officers.NumTrafficStops(**kwargs),
    #                '1yrtrafficstopnum': officers.NumTrafficStops(**kwargs),
    #                'careerdomvioltrain': officers.HoursDomViolTrain(**kwargs),
    #                '1yrdomvioltrain': officers.HoursDomViolTrain(**kwargs),
    #                'careermilitarytrain': officers.HoursMilitaryReturn(**kwargs),
    #                '1yrmilitarytrain': officers.HoursMilitaryReturn(**kwargs),
    #                'careertasertrain': officers.HoursTaserTrain(**kwargs),
    #                '1yrtasertrain': officers.HoursTaserTrain(**kwargs),
    #                'careerbiastrain': officers.HoursBiasTrain(**kwargs),
    #                '1yrbiastrain': officers.HoursBiasTrain(**kwargs),
    #                'careerforcetrain': officers.HoursForceTrain(**kwargs),
    #                '1yrforcetrain': officers.HoursForceTrain(**kwargs),
    #                'careertsuofarr': officers.NumTStopRunTagUOFOrArrest(**kwargs),
    #                '1yrtsuofarr': officers.NumTStopRunTagUOFOrArrest(**kwargs),
    #                'careerforcetraffic': officers.NumTrafficStopsForce(**kwargs),
    #                '1yrforcetraffic': officers.NumTrafficStopsForce(**kwargs),
    #                'careertsblackdaynight': officers.TSPercBlackDayNight(**kwargs),
    #                '1yrtsblackdaynight': officers.TSPercBlackDayNight(**kwargs),
    #                '1yrtrafstopresist': officers.NumTrafficStopsResist(**kwargs),
    #                '3yrtrafstopresist': officers.NumTrafficStopsResist(**kwargs),
    #                '5yrtrafstopresist': officers.NumTrafficStopsResist(**kwargs),
    #                'careertrafstopresist': officers.NumTrafficStopsResist(**kwargs),
    #                '1yrtrafstopsearch': officers.TrafficStopsSearch(**kwargs),
    #                '3yrtrafstopsearch': officers.TrafficStopsSearch(**kwargs),
    #                '5yrtrafstopsearch': officers.TrafficStopsSearch(**kwargs),
    #                'careertrafstopsearch': officers.TrafficStopsSearch(**kwargs),
    #                '1yrtrafstopsearchreason': officers.TrafficStopSearchReason(**kwargs),
    #                '3yrtrafstopsearchreason': officers.TrafficStopSearchReason(**kwargs),
    #                '5yrtrafstopsearchreason': officers.TrafficStopSearchReason(**kwargs),
    #                'careertrafstopsearchreason': officers.TrafficStopSearchReason(**kwargs),
    #                '1yrtrafstopruntagreason': officers.TrafficStopRunTagReason(**kwargs),
    #                '3yrtrafstopruntagreason': officers.TrafficStopRunTagReason(**kwargs),
    #                '5yrtrafstopruntagreason': officers.TrafficStopRunTagReason(**kwargs),
    #                'careertrafstopruntagreason': officers.TrafficStopRunTagReason(**kwargs),
    #                '1yrtrafstopresult': officers.TrafficStopResult(**kwargs),
    #                '3yrtrafstopresult': officers.TrafficStopResult(**kwargs),
    #                '5yrtrafstopresult': officers.TrafficStopResult(**kwargs),
    #                'careertrafstopresult': officers.TrafficStopResult(**kwargs),
    #                '1yrtrafstopbyrace': officers.TrafficStopFracRace(**kwargs),
    #                '3yrtrafstopbyrace': officers.TrafficStopFracRace(**kwargs),
    #                '5yrtrafstopbyrace': officers.TrafficStopFracRace(**kwargs),
    #                'careertrafstopbyrace': officers.TrafficStopFracRace(**kwargs),
    #                '1yrtrafstopbygender': officers.TrafficStopFracGender(**kwargs),
    #                '3yrtrafstopbygender': officers.TrafficStopFracGender(**kwargs),
    #                '5yrtrafstopbygender': officers.TrafficStopFracGender(**kwargs),
    #                'careertrafstopbygender': officers.TrafficStopFracGender(**kwargs),
    #                'trafficstoptimeseries': officers.TrafficStopTimeSeries(**kwargs),
    #                '1yreiswarnings': officers.EISWarningsCount(**kwargs),
    #                '5yreiswarnings': officers.EISWarningsCount(**kwargs),
    #                'careereiswarnings': officers.EISWarningsCount(**kwargs),
    #                '1yreiswarningtypes': officers.EISWarningByTypeFrac(**kwargs),
    #                'careereiswarningtypes': officers.EISWarningByTypeFrac(**kwargs),
    #                '1yreiswarninginterventions': officers.EISWarningInterventionFrac(**kwargs),
    #                'careereiswarninginterventions': officers.EISWarningInterventionFrac(**kwargs),
    #                '1yrextradutyhours': officers.ExtraDutyHours(**kwargs),
    #                'careerextradutyhours': officers.ExtraDutyHours(**kwargs),
    #                '1yrextradutyneighb1': officers.ExtraDutyNeighborhoodFeatures1(**kwargs),
    #                'careerextradutyneighb1': officers.ExtraDutyNeighborhoodFeatures1(**kwargs),
    #                '1yrextradutyneighb2': officers.ExtraDutyNeighborhoodFeatures2(**kwargs),
    #                'careerextradutyneighb2': officers.ExtraDutyNeighborhoodFeatures2(**kwargs),
    #                '1yrneighb1': officers.AvgNeighborhoodFeatures1(**kwargs),
    #                'careerneighb1': officers.AvgNeighborhoodFeatures1(**kwargs),
    #                '1yrneighb2': officers.AvgNeighborhoodFeatures2(**kwargs),
    #                'careerneighb2': officers.AvgNeighborhoodFeatures2(**kwargs),
    #                '1yrprioralladverse': officers.CountPriorAdverse(**kwargs),
    #                'careerprioralladverse': officers.CountPriorAdverse(**kwargs),
    #                '1yrprioraccident': officers.CountPriorAccident(**kwargs),
    #                'careerprioraccident': officers.CountPriorAccident(**kwargs),
    #                '1yrnumfilteredadverse': officers.CountPriorFilteredAdverse(**kwargs),
    #                'careernumfilteredadverse': officers.CountPriorFilteredAdverse(**kwargs),
    #                '1yrroccoc': officers.CountRocCOC(**kwargs),
    #                'careerroccoc': officers.CountRocCOC(**kwargs),
    #                '1yrrocia': officers.CountRocIA(**kwargs),
    #                'careerrocia': officers.CountRocIA(**kwargs),
    #                '1yrpreventable': officers.CountPreventable(**kwargs),
    #                'careerpreventable': officers.CountPreventable(**kwargs),
    #                '1yrunjustified': officers.CountUnjustified(**kwargs),
    #                'careerunjustified': officers.CountUnjustified(**kwargs),
    #                '1yrsustaincompl': officers.CountSustainedComplaints(**kwargs),
    #                'careersustaincompl': officers.CountSustainedComplaints(**kwargs),
    #                '1yriaconcerns': officers.IAConcerns(**kwargs),
    #                'careeriaconcerns': officers.IAConcerns(**kwargs),
    #                'careeriarate': officers.IARate(**kwargs),
    #                '1yrdofcounts': officers.DOFTypeCounts(**kwargs),
    #                'careerdofcounts': officers.DOFTypeCounts(**kwargs),
    #                '1yrdirectivecounts': officers.DirectiveViolCounts(**kwargs),
    #                'careerdirectivecounts': officers.DirectiveViolCounts(**kwargs),
    #                '1yriaeventtypes': officers.IAEventTypeCounts(**kwargs),
    #                'careeriaeventtypes': officers.IAEventTypeCounts(**kwargs),
    #                '1yrinterventions': officers.SuspensionCounselingTime(**kwargs),
    #                'careerinterventions': officers.SuspensionCounselingTime(**kwargs),
    #                '1yrweaponsuse': officers.NormalizedCountsWeaponsUse(**kwargs),
    #                'careerweaponsuse': officers.NormalizedCountsWeaponsUse(**kwargs),
    #                '1yrunithistory': officers.CountUnit(**kwargs),
    #                'careerunithistory': officers.CountUnit(**kwargs),
    #                '1yrdivisionhistory': officers.CountDivision(**kwargs),
    #                'careerdivisionhistory': officers.CountDivision(**kwargs),}

    if feature not in dict_lookup.keys():
        raise UnknownFeatureError(feature)

    return dict_lookup[feature]
