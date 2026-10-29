"""Reproducible, explicitly synthetic demonstrations; NO live venue data."""
from __future__ import annotations

from dataclasses import asdict
from itertools import product

import numpy as np

from .transport import (
    binary_paths, cartesian_paths, marginal_features,
    martingale_features, price_interval,
)


def binary_three_event():
    states = binary_paths(3)
    a, b, c = states.T
    features = np.vstack((a, b, c, a*b, b*c, a*c)).astype(float)
    prices = np.array([.60, .55, .45, .40, .30, .22])
    triple = (a*b*c).astype(float)
    single = price_interval(triple, features[:3], prices[:3], prices[:3])
    neighbors = price_interval(triple, features[:5], prices[:5], prices[:5])
    full = price_interval(triple, features, prices, prices)
    # Conditional probability is linear here because P(A and B)=0.40 is fixed.
    conditional_lo = full.lower / .40
    conditional_hi = full.upper / .40
    return {
        'states': states, 'features': features, 'prices': prices, 'payoff': triple,
        'single': single, 'neighbors': neighbors, 'full': full,
        'conditional': (conditional_lo, conditional_hi),
    }


def two_date_underlying(extra_joint_quote: float | None = None):
    levels = [[90.,110.],[70.,90.,110.,130.]]
    marginals = [
        {90.:.50,110.:.50},
        {70.:.25,90.:.25,110.:.25,130.:.25},
    ]
    states = cartesian_paths(levels)
    features, prices = marginal_features(states, marginals)
    # Rally at first monitoring date, followed by a fall to 90 or below.
    payoff = ((states[:,0] == 110) & (states[:,1] <= 90)).astype(float)
    if extra_joint_quote is not None:
        joint = ((states[:,0] == 110) & (states[:,1] == 130)).astype(float)
        features = np.vstack((features,joint))
        prices = np.r_[prices, float(extra_joint_quote)]
    ot = price_interval(payoff, features, prices, prices)
    mart = martingale_features(states)
    mot = price_interval(payoff, features, prices, prices,
                         extra_equalities=mart, extra_values=np.zeros(len(mart)))
    return {'states':states, 'features':features, 'prices':prices,
            'payoff':payoff, 'martingale_features':mart, 'ot':ot, 'mot':mot}


def three_date_underlying():
    levels = [[90.,110.], [70.,90.,110.,130.],
              [50.,70.,90.,110.,130.,150.]]
    marginals = [
        {90.:.5,110.:.5},
        {70.:.25,90.:.25,110.:.25,130.:.25},
        {50.:.125,70.:.125,90.:.25,110.:.25,130.:.125,150.:.125},
    ]
    states = cartesian_paths(levels)
    features, prices = marginal_features(states, marginals)
    mart = martingale_features(states)
    payoff = ((states[:,0] == 110) & (states[:,1] <= 90)
              & (states[:,2] >= 130)).astype(float)
    ot = price_interval(payoff, features, prices, prices)
    mot = price_interval(payoff, features, prices, prices,
                         extra_equalities=mart, extra_values=np.zeros(len(mart)))
    # Discrete monitoring: looks only at dates 1, 2, 3, not intraperiod hits.
    barrier = (np.max(states, axis=1) >= 130).astype(float)
    barrier_ot = price_interval(barrier, features, prices, prices)
    barrier_mot = price_interval(barrier, features, prices, prices,
                                extra_equalities=mart, extra_values=np.zeros(len(mart)))
    return {'states':states, 'features':features, 'prices':prices, 'payoff':payoff,
            'martingale_features': mart, 'ot':ot, 'mot':mot,
            'barrier':barrier, 'barrier_ot':barrier_ot,
            'barrier_mot':barrier_mot}


def run_all():
    b = binary_three_event()
    d2 = two_date_underlying()
    d2_joint = two_date_underlying(extra_joint_quote=.20)
    d3 = three_date_underlying()
    result = {
        'dataset':'synthetic only; all prices in probability units',
        'binary_three_event':{
            'individual_marginals_only':[b['single'].lower,b['single'].upper],
            'plus_AB_BC':[b['neighbors'].lower,b['neighbors'].upper],
            'plus_AC':[b['full'].lower,b['full'].upper],
            'conditional_C_given_AB':list(b['conditional']),
        },
        'two_date_rally_decline':{
            'ordinary_ot':[d2['ot'].lower,d2['ot'].upper],
            'martingale_ot':[d2['mot'].lower,d2['mot'].upper],
            'martingale_ot_plus_joint_130_quote':[d2_joint['mot'].lower,d2_joint['mot'].upper],
        },
        'three_date_rally_decline_rebound':{
            'ordinary_ot':[d3['ot'].lower,d3['ot'].upper],
            'martingale_ot':[d3['mot'].lower,d3['mot'].upper],
        },
        'three_date_discretely_monitored_upper_barrier_130':{
            'ordinary_ot':[d3['barrier_ot'].lower,d3['barrier_ot'].upper],
            'martingale_ot':[d3['barrier_mot'].lower,d3['barrier_mot'].upper],
        },
    }
    return result


if __name__ == '__main__':
    import json
    print(json.dumps(run_all(),indent=2))
