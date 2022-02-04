import itertools

import numpy
import numpy as np
import scipy.stats as stats
import pandas as pd
import sys
from statsmodels.stats.weightstats import ztest


class FairER:
    # the input is a list of objects of class Workload
    # alpha is used for One-Way Anova Test 
    def __init__(self, workloads, alpha, threshold, single_fairness=True):
        self.workloads = workloads
        self.alpha = alpha
        self.threshold = threshold
        self.single_fairness = single_fairness

        # creates a two dimensional matrix, subgroups x workload fairness value
        # used only for distribution
        def separate_distributions_from_workloads(self, subgroups, workloads_is_fair):
            num_of_subgroups = len(subgroups)
            subgroup_precisions = []
            for i in range(num_of_subgroups):
                subgroup_precisions[i] = []
            for i in range(num_of_subgroups):
                for workload_distr in workloads_is_fair:
                    subgroup_precisions.append(workload_distr[i])
            return subgroup_precisions

        def is_fair(self, subgroups, measure, aggregate):
            if len(self.workloads) == 1:
                workload_is_fair = self.workloads[0].is_fair(subgroups, measure, aggregate, single_fairness)
                if aggregate is not "distribution":
                    return aggregate > self.threshold
                else:
                    return [subgroup_is_fair > self.threshold for subgroup_is_fair in workload_is_fair]
            else:
                workloads_is_fair = []
                for workload in self.workloads:
                    workloads_is_fair.append(workload.is_fair(subgroups, measure, aggregate, single_fairness))
                # general idea of how the entity matching is performed
                if aggregate is not "distribution":
                    p_value = ztest(workloads_is_fair, value=self.threshold)[1]
                    return p_value <= self.alpha
                # specific for each measure
                else:
                    subgroup_precisions = self.separate_distributions_from_workloads(subgroups, workloads_is_fair)
                    subroups_is_fair = []
                    for subgroup_precision in subgroup_precisions:
                        p_value = ztest(subgroup_precision, value=self.threshold)[1]
                        subroups_is_fair.append(p_value <= self.alpha)
                    return subroups_is_fair
