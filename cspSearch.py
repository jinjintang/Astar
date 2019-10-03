# cspSearch.py - Representations of a Search Problem from a CSP.
# AIFCA Python3 code Version 0.7.7 Documentation at http://aipython.org

# Artificial Intelligence: Foundations of Computational Agents
# http://artint.info
# Copyright David L Poole and Alan K Mackworth 2017.
# This work is licensed under a Creative Commons
# Attribution-NonCommercial-ShareAlike 4.0 International License.
# See: http://creativecommons.org/licenses/by-nc-sa/4.0/deed.en

from cspProblem import CSP, Constraint
from searchProblem import Arc, Search_problem
def dict_union(d1,d2):
    """returns a dictionary that contains the keys of d1 and d2.
    The value for each key that is in d2 is the value from d2,
    otherwise it is the value from d1.
    This does not have side effects.
    """
    d = dict(d1)    # copy d1
    d.update(d2)
    return d

class Search_from_CSP(Search_problem):
    """A search problem directly from the CSP.

    A node is a variable:value dictionary"""
    def __init__(self, csp, variable_order=None):
        self.csp=csp
        if variable_order:
            assert set(variable_order) == set(csp.variables)
            assert len(variable_order) == len(csp.variables)
            self.variables = variable_order
        else:
            self.variables = list(csp.variables)

    def is_goal(self, node):
        """returns whether the current node is a goal for the search
        """
        return len(node)==len(self.csp.variables)
    
    def start_node(self):
        """returns the start node for the search
        """

        return Arc({},{},0)
    
    def heuristic(self,n):
       
        if len(n)==len(self.csp.variables):
            return 0
        c=0
        i=0
        used=list(n.values())
        for v in self.variables[len(n):]:
            for d in self.csp.domains[v]:
                if d not in used:
                    c+=self.csp.cost[(v,d)]
                    i+=1
        return c/i


    def neighbors(self, node):
        """returns a list of the neighboring nodes of node.
        """
        var = self.variables[len(node)] # the next variable
        res = []
        for val in self.csp.domains[var]:
            new_env = dict_union(node,{var:val})  #dictionary union
            if self.csp.consistent(new_env):
                res.append(Arc(node,new_env,self.csp.cost[(var,val)]))
        return res


from searchGeneric import Searcher

def dfs_solver(csp):
    """depth-first search solver"""
    path = Searcher(Search_from_CSP(csp)).search()
    if path is not None:
        return path.end()
    else:
        return None


