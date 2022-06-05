from __future__ import annotations

import time
import warnings
from itertools import combinations, permutations
from typing import Dict, List, Tuple

import networkx as nx
from numpy import ndarray

from causallearn.graph.GraphClass import CausalGraph
from causallearn.utils.PCUtils.BackgroundKnowledge import BackgroundKnowledge
from causallearn.utils.cit import *
from causallearn.utils.PCUtils import Helper, Meek, SkeletonDiscovery, UCSepset
from causallearn.utils.PCUtils.BackgroundKnowledgeOrientUtils import \
    orient_by_background_knowledge


def pc(data: ndarray, alpha=0.05, indep_test=fisherz, stable: bool = True, uc_rule: int = 0, uc_priority: int = 2,
       mvpc: bool = False, correction_name: str = 'MV_Crtn_Fisher_Z',
       background_knowledge: BackgroundKnowledge | None = None, verbose: bool = False, show_progress: bool = True):
    if data.shape[0] < data.shape[1]:
        warnings.warn("The number of features is much larger than the sample size!")

    if mvpc:  # missing value PC
        if indep_test == fisherz:
            indep_test = mv_fisherz
        return mvpc_alg(data=data, alpha=alpha, indep_test=indep_test, correction_name=correction_name, stable=stable,
                        uc_rule=uc_rule, uc_priority=uc_priority, background_knowledge=background_knowledge,
                        verbose=verbose,
                        show_progress=show_progress)
    else:
        return pc_alg(data=data, alpha=alpha, indep_test=indep_test, stable=stable, uc_rule=uc_rule,
                      uc_priority=uc_priority, background_knowledge=background_knowledge, verbose=verbose,
                      show_progress=show_progress)


def pc_alg(data: ndarray, alpha: float, indep_test, stable: bool, uc_rule: int, uc_priority: int,
           background_knowledge: BackgroundKnowledge | None = None,
           verbose: bool = False,
           show_progress: bool = True) -> CausalGraph:
    """
    Parameters
    ----------
    data : data set (numpy ndarray)
    alpha : float, p_value (0,1)
    indep_test : 独立性检验
            [fisherz, chisq, gsq, kci]
           - fisherz: Fisher's Z conditional independence test
           - chisq: Chi-squared conditional independence test
           - gsq: G-squared conditional independence test
           - kci: Kernel-based conditional independence test
    uc_rule : 对撞屏蔽
           0: run uc_sepset
           1: run maxP
           2: run definiteMaxP
    uc_priority :未屏蔽对撞处理
           -1: whatever is default in uc_rule
           0: overwrite
           1: orient bi-directed
           2. prioritize existing colliders
           3. prioritize stronger colliders
           4. prioritize stronger* colliers
    verbose : True iff verbose output should be printed.
    show_progress : True iff the algorithm progress should be show in console.

    Returns
    -------
    """

    start = time.time()
    cg_1 = SkeletonDiscovery.skeleton_discovery(data, alpha, indep_test, stable,
                                                background_knowledge=background_knowledge, verbose=verbose,
                                                show_progress=show_progress)

    if background_knowledge is not None:
        orient_by_background_knowledge(cg_1, background_knowledge)

    if uc_rule == 0:
        if uc_priority != -1:
            cg_2 = UCSepset.uc_sepset(cg_1, uc_priority, background_knowledge=background_knowledge)
        else:
            cg_2 = UCSepset.uc_sepset(cg_1, background_knowledge=background_knowledge)
        cg = Meek.meek(cg_2, background_knowledge=background_knowledge)

    elif uc_rule == 1:
        if uc_priority != -1:
            cg_2 = UCSepset.maxp(cg_1, uc_priority, background_knowledge=background_knowledge)
        else:
            cg_2 = UCSepset.maxp(cg_1, background_knowledge=background_knowledge)
        cg = Meek.meek(cg_2, background_knowledge=background_knowledge)

    elif uc_rule == 2:
        if uc_priority != -1:
            cg_2 = UCSepset.definite_maxp(cg_1, alpha, uc_priority, background_knowledge=background_knowledge)
        else:
            cg_2 = UCSepset.definite_maxp(cg_1, alpha, background_knowledge=background_knowledge)
        cg_before = Meek.definite_meek(cg_2, background_knowledge=background_knowledge)
        cg = Meek.meek(cg_before, background_knowledge=background_knowledge)
    else:
        raise ValueError("uc_rule should be in [0, 1, 2]")
    end = time.time()

    cg.PC_elapsed = end - start

    return cg


def mvpc_alg(data: ndarray, alpha: float, indep_test, correction_name: str, stable: bool, uc_rule: int,
             uc_priority: int, background_knowledge: BackgroundKnowledge | None = None,
             verbose: bool = False,
             show_progress: bool = True) -> CausalGraph:

    """
    missing value Peter-Clark Algorithm
    """
    start = time.time()

    ## Step 1: detect the direct causes of missingness indicators
    prt_m = get_prt_mpairs(data, alpha, indep_test, stable)
    # print('Finish detecting the parents of missingness indicators.  ')

    ## Step 2:
    ## a) Run PC algorithm with the 1st step skeleton;
    cg_pre = SkeletonDiscovery.skeleton_discovery(data, alpha, indep_test, stable,
                                                  background_knowledge=background_knowledge,
                                                  verbose=verbose, show_progress=show_progress)
    if background_knowledge is not None:
        orient_by_background_knowledge(cg_pre, background_knowledge)

    cg_pre.to_nx_skeleton()

    ## b) Correction of the extra edges
    cg_corr = skeleton_correction(data, alpha, correction_name, cg_pre, prt_m, stable)

    if background_knowledge is not None:
        orient_by_background_knowledge(cg_corr, background_knowledge)

    ## Step 3: Orient the edges
    if uc_rule == 0:
        if uc_priority != -1:
            cg_2 = UCSepset.uc_sepset(cg_corr, uc_priority, background_knowledge=background_knowledge)
        else:
            cg_2 = UCSepset.uc_sepset(cg_corr, background_knowledge=background_knowledge)
        cg = Meek.meek(cg_2, background_knowledge=background_knowledge)

    elif uc_rule == 1:
        if uc_priority != -1:
            cg_2 = UCSepset.maxp(cg_corr, uc_priority, background_knowledge=background_knowledge)
        else:
            cg_2 = UCSepset.maxp(cg_corr, background_knowledge=background_knowledge)
        cg = Meek.meek(cg_2, background_knowledge=background_knowledge)

    elif uc_rule == 2:
        if uc_priority != -1:
            cg_2 = UCSepset.definite_maxp(cg_corr, alpha, uc_priority, background_knowledge=background_knowledge)
        else:
            cg_2 = UCSepset.definite_maxp(cg_corr, alpha, background_knowledge=background_knowledge)
        cg_before = Meek.definite_meek(cg_2, background_knowledge=background_knowledge)
        cg = Meek.meek(cg_before, background_knowledge=background_knowledge)
    else:
        raise ValueError("uc_rule should be in [0, 1, 2]")
    end = time.time()

    cg.PC_elapsed = end - start

    return cg


def get_prt_mpairs(data: ndarray, alpha: float, indep_test, stable: bool = True) -> Dict[str, list]:
    """
    Detect the parents of missingness indicators
    If a missingness indicator has no parent, it will not be included in the result
    :return:
    cg: a CausalGraph object
    """
    prt_m = {'prt': [], 'm': []}

    m_indx = get_mindx(data)

    for r in m_indx:
        prt_r = detect_parent(r, data, alpha, indep_test, stable)
        if isempty(prt_r):
            pass
        else:
            prt_m['prt'].append(prt_r)
            prt_m['m'].append(r)
    return prt_m


def isempty(prt_r) -> bool:
    """Test whether the parent of a missingness indicator is empty"""
    return len(prt_r) == 0


def get_mindx(data: ndarray) -> List[int]:
    """
    :return:
    m_indx: list, the index of missingness indicators
    """

    m_indx = []
    _, ncol = np.shape(data)
    for i in range(ncol):
        if np.isnan(data[:, i]).any():
            m_indx.append(i)
    return m_indx


def detect_parent(r: int, data_: ndarray, alpha: float, indep_test, stable: bool = True) -> ndarray:
    """
    Detect the parents of a missingness indicator
    """
    data = data_.copy()

    assert type(data) == np.ndarray
    assert 0 < alpha < 1

    data[:, r] = np.isnan(data[:, r]).astype(float)  # True is missing; false is not missing
    if sum(data[:, r]) == 0 or sum(data[:, r]) == len(data[:, r]):
        return np.empty(0)

    no_of_var = data.shape[1]
    cg = CausalGraph(no_of_var)
    cg.data = data
    cg.set_ind_test(indep_test)
    cg.corr_mat = np.corrcoef(data, rowvar=False) if indep_test == fisherz else []

    node_ids = range(no_of_var)
    pair_of_variables = list(permutations(node_ids, 2))

    depth = -1
    while cg.max_degree() - 1 > depth:
        depth += 1
        edge_removal = []
        for (x, y) in pair_of_variables:

            if x != r:
                continue


            Neigh_x = cg.neighbors(x)
            if y not in Neigh_x:
                continue
            else:
                Neigh_x = np.delete(Neigh_x, np.where(Neigh_x == y))

            if len(Neigh_x) >= depth:
                for S in combinations(Neigh_x, depth):
                    p = cg.ci_test(x, y, S)
                    if p > alpha:
                        if not stable:  # Unstable: Remove x---y right away
                            edge1 = cg.G.get_edge(cg.G.nodes[x], cg.G.nodes[y])
                            if edge1 is not None:
                                cg.G.remove_edge(edge1)
                            edge2 = cg.G.get_edge(cg.G.nodes[y], cg.G.nodes[x])
                            if edge2 is not None:
                                cg.G.remove_edge(edge2)
                        else:  # Stable: x---y will be removed only
                            edge_removal.append((x, y))  # after all conditioning sets at
                            edge_removal.append((y, x))  # depth l have been considered
                            Helper.append_value(cg.sepset, x, y, S)
                            Helper.append_value(cg.sepset, y, x, S)
                        break

        for (x, y) in list(set(edge_removal)):
            edge1 = cg.G.get_edge(cg.G.nodes[x], cg.G.nodes[y])
            if edge1 is not None:
                cg.G.remove_edge(edge1)


    cg.to_nx_skeleton()
    cg_skel_adj = nx.to_numpy_array(cg.nx_skel).astype(int)
    prt = get_parent(r, cg_skel_adj)

    return prt


def get_parent(r: int, cg_skel_adj: ndarray) -> ndarray:
    """
    Get the neighbors of missingness indicators which are the parents
    """
    num_var = len(cg_skel_adj[0, :])
    indx = np.array([i for i in range(num_var)])
    prt = indx[cg_skel_adj[r, :] == 1]
    return prt


## *********** END ***********
#######################################################################################################################

def skeleton_correction(data: ndarray, alpha: float, test_with_correction_name: str, init_cg: CausalGraph, prt_m: dict,
                        stable: bool = True) -> CausalGraph:
    """
    Perform skeleton discovery
    """

    assert type(data) == np.ndarray
    assert 0 < alpha < 1
    assert test_with_correction_name in ["MV_Crtn_Fisher_Z", "MV_Crtn_G_sq"]

    ## *********** Adaption 1 ***********
    no_of_var = data.shape[1]

    ## Initialize the graph with the result of test-wise deletion skeletion search
    cg = init_cg

    cg.data = data
    if test_with_correction_name in ["MV_Crtn_Fisher_Z", "MV_Crtn_G_sq"]:
        cg.set_ind_test(mc_fisherz, True)
    # No need of the correlation matrix if using test-wise deletion test
    cg.corr_mat = np.corrcoef(data, rowvar=False) if test_with_correction_name == "MV_Crtn_Fisher_Z" else []
    cg.prt_m = prt_m

    node_ids = range(no_of_var)
    pair_of_variables = list(permutations(node_ids, 2))

    depth = -1
    while cg.max_degree() - 1 > depth:
        depth += 1
        edge_removal = []
        for (x, y) in pair_of_variables:
            Neigh_x = cg.neighbors(x)
            if y not in Neigh_x:
                continue
            else:
                Neigh_x = np.delete(Neigh_x, np.where(Neigh_x == y))

            if len(Neigh_x) >= depth:
                for S in combinations(Neigh_x, depth):
                    p = cg.ci_test(x, y, S)
                    if p > alpha:
                        if not stable:  # Unstable: Remove x---y right away
                            edge1 = cg.G.get_edge(cg.G.nodes[x], cg.G.nodes[y])
                            if edge1 is not None:
                                cg.G.remove_edge(edge1)
                            edge2 = cg.G.get_edge(cg.G.nodes[y], cg.G.nodes[x])
                            if edge2 is not None:
                                cg.G.remove_edge(edge2)
                        else:  # Stable: x---y will be removed only
                            edge_removal.append((x, y))  # after all conditioning sets at
                            edge_removal.append((y, x))  # depth l have been considered
                            Helper.append_value(cg.sepset, x, y, S)
                            Helper.append_value(cg.sepset, y, x, S)
                        break

        for (x, y) in list(set(edge_removal)):
            edge1 = cg.G.get_edge(cg.G.nodes[x], cg.G.nodes[y])
            if edge1 is not None:
                cg.G.remove_edge(edge1)

    return cg


def get_adjacancy_matrix(g: CausalGraph) -> ndarray:
    return nx.to_numpy_array(g.nx_graph).astype(int)


def matrix_diff(cg1: CausalGraph, cg2: CausalGraph) -> (float, List[Tuple[int, int]]):
    adj1 = get_adjacancy_matrix(cg1)
    adj2 = get_adjacancy_matrix(cg2)
    count = 0
    diff_ls = []
    for i in range(len(adj1[:, ])):
        for j in range(len(adj2[:, ])):
            if adj1[i, j] != adj2[i, j]:
                diff_ls.append((i, j))
                count += 1
    return count / 2, diff_ls
