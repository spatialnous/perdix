"""
******
Layout
******

Node positioning algorithms for graph drawing.

The default scales and centering for these layouts are
typically squares with side [0, 1] or [0, scale].
The two circular layout routines (circular_layout and
shell_layout) have size [-1, 1] or [-scale, scale].
"""
# Authors: Aric Hagberg <aric.hagberg@gmail.com>,
#          Dan Schult <dschult@colgate.edu>

#    Copyright (C) 2004-2016 by
#    Aric Hagberg <hagberg@lanl.gov>
#    Dan Schult <dschult@colgate.edu>
#    Pieter Swart <swart@lanl.gov>
#    All rights reserved.
#    BSD license.
import collections
import networkx as nx

__all__ = ['circular_layout',
           'random_layout',
           'shell_layout',
           'spring_layout',
           'spectral_layout',
           'fruchterman_reingold_layout']


def random_layout(G, dim=2, scale=1., center=None):
    """Position nodes uniformly at random.

    For every node, a position is generated by choosing each of dim
    coordinates uniformly at random on the default interval [0.0, 1.0),
    or on an interval of length `scale` centered at `center`.

    NumPy (http://scipy.org) is required for this function.

    Parameters
    ----------
    G : NetworkX graph or list of nodes
       A position will be assigned to every node in G.

    dim : int
       Dimension of layout.

    scale : float (default 1)
        Scale factor for positions

    center : array-like (default scale*0.5 in each dim)
       Coordinate around which to center the layout.

    Returns
    -------
    pos : dict
       A dictionary of positions keyed by node

    Examples
    --------
    >>> G = nx.lollipop_graph(4, 3)
    >>> pos = nx.random_layout(G)
    """
    import numpy as np

    shape = (len(G), dim)
    pos = np.random.random(shape) * scale
    if center is not None:
        pos += np.asarray(center) - 0.5 * scale
    return dict(zip(G, pos))


def circular_layout(G, dim=2, scale=1., center=None):
    """Position nodes on a circle.

    Parameters
    ----------
    G : NetworkX graph or list of nodes

    dim : int
       Dimension of layout, currently only dim=2 is supported

    scale : float (default 1)
        Scale factor for positions, i.e. radius of circle.

    center : array-like (default origin)
       Coordinate around which to center the layout.

    Returns
    -------
    dict :
       A dictionary of positions keyed by node

    Examples
    --------
    >>> G=nx.path_graph(4)
    >>> pos=nx.circular_layout(G)

    Notes
    -----
    This algorithm currently only works in two dimensions and does not
    try to minimize edge crossings.

    """
    import numpy as np

    if len(G) == 0:
        return {}

    twopi = 2.0*np.pi
    theta = np.arange(0, twopi, twopi/len(G))
    pos = np.column_stack([np.cos(theta), np.sin(theta)]) * scale
    if center is not None:
        pos += np.asarray(center)

    return dict(zip(G, pos))

def shell_layout(G, nlist=None, dim=2, scale=1., center=None):
    """Position nodes in concentric circles.

    Parameters
    ----------
    G : NetworkX graph or list of nodes

    nlist : list of lists
       List of node lists for each shell.

    dim : int
       Dimension of layout, currently only dim=2 is supported

    scale : float (default 1)
        Scale factor for positions, i.e.radius of largest shell

    center : array-like (default origin)
       Coordinate around which to center the layout.

    Returns
    -------
    dict :
       A dictionary of positions keyed by node

    Examples
    --------
    >>> G = nx.path_graph(4)
    >>> shells = [[0], [1,2,3]]
    >>> pos = nx.shell_layout(G, shells)

    Notes
    -----
    This algorithm currently only works in two dimensions and does not
    try to minimize edge crossings.

    """
    import numpy as np

    if len(G) == 0:
        return {}

    if nlist is None:
        # draw the whole graph in one shell
        nlist = [list(G)]

    numb_shells = len(nlist)
    if len(nlist[0]) == 1:
        # single node at center
        radius = 0.0
        numb_shells -= 1
    else:
        # else start at r=1
        radius = 1.0
    # distance between shells
    gap = (scale / numb_shells) if numb_shells else scale
    radius *= gap

    npos={}
    twopi = 2.0*np.pi
    for nodes in nlist:
        theta = np.arange(0, twopi, twopi/len(nodes))
        pos = np.column_stack([np.cos(theta), np.sin(theta)]) * radius
        npos.update(zip(nodes, pos))
        radius += gap

    if center is not None:
        center = np.asarray(center)
        for n,p in npos.items():
            npos[n] = p + center

    return npos


def fruchterman_reingold_layout(G, dim=2, k=None,
                                pos=None,
                                fixed=None,
                                iterations=50,
                                weight='weight',
                                scale=1.0,
                                center=None):
    """Position nodes using Fruchterman-Reingold force-directed algorithm.

    Parameters
    ----------
    G : NetworkX graph

    dim : int
       Dimension of layout

    k : float (default=None)
       Optimal distance between nodes.  If None the distance is set to
       1/sqrt(n) where n is the number of nodes.  Increase this value
       to move nodes farther apart.

    pos : dict or None  optional (default=None)
       Initial positions for nodes as a dictionary with node as keys
       and values as a list or tuple.  If None, then use random initial
       positions.

    fixed : list or None  optional (default=None)
      Nodes to keep fixed at initial position.
      If any nodes are fixed, the scale and center features are not used.

    iterations : int  optional (default=50)
       Number of iterations of spring-force relaxation

    weight : string or None   optional (default='weight')
        The edge attribute that holds the numerical value used for
        the effective spring constant. If None, edge weights are 1.

    scale : float (default=1.0)
        Scale factor for positions. The nodes are positioned
        in a box of size `scale` in each dim centered at `center`.

    center : array-like (default scale/2 in each dim)
       Coordinate around which to center the layout.

    Returns
    -------
    dict :
       A dictionary of positions keyed by node

    Examples
    --------
    >>> G=nx.path_graph(4)
    >>> pos=nx.spring_layout(G)

    # this function has two names:
    # spring_layout and fruchterman_reingold_layout
    >>> pos=nx.fruchterman_reingold_layout(G)
    """
    import numpy as np

    if len(G) == 0:
        return {}

    if fixed is not None:
        nfixed = dict(zip(G, range(len(G))))
        fixed = np.asarray([nfixed[v] for v in fixed])

        if pos is None:
            msg = "Keyword pos must be specified if any nodes are fixed"
            raise ValueError(msg)

    if pos is not None:
        # Determine size of existing domain to adjust initial positions
        pos_coords = np.array(list(pos.values()))
        min_coords = pos_coords.min(0)
        domain_size = pos_coords.max(0) - min_coords
        shape = (len(G), dim)
        pos_arr = np.random.random(shape) * domain_size + min_coords
        for i,n in enumerate(G):
            if n in pos:
                pos_arr[i] = np.asarray(pos[n])
    else:
        pos_arr=None

    if k is None and fixed is not None:
        # Adjust k for domains larger than 1x1
        k=domain_size.max()/np.sqrt(len(G))
    try:
        # Sparse matrix
        if len(G) < 500:  # sparse solver for large graphs
            raise ValueError
        A = nx.to_scipy_sparse_matrix(G, weight=weight, dtype='f')
        pos = _sparse_fruchterman_reingold(A,dim,k,pos_arr,fixed,iterations)
    except:
        A = nx.to_numpy_matrix(G, weight=weight)
        pos = _fruchterman_reingold(A, dim, k, pos_arr, fixed, iterations)

    if fixed is None:
        pos = _rescale_layout(pos, scale)
        if center is not None:
            pos += np.asarray(center) - 0.5 * scale

    return dict(zip(G,pos))

spring_layout=fruchterman_reingold_layout

def _fruchterman_reingold(A,dim=2,k=None,pos=None,fixed=None,iterations=50):
    # Position nodes in adjacency matrix A using Fruchterman-Reingold
    # Entry point for NetworkX graph is fruchterman_reingold_layout()
    import numpy as np
    try:
        nnodes,_=A.shape
    except AttributeError:
        raise nx.NetworkXError(
            "fruchterman_reingold() takes an adjacency matrix as input")

    A=np.asarray(A) # make sure we have an array instead of a matrix

    if pos is None:
        # random initial positions
        pos=np.asarray(np.random.random((nnodes,dim)),dtype=A.dtype)
    else:
        # make sure positions are of same type as matrix
        pos=pos.astype(A.dtype)

    # optimal distance between nodes
    if k is None:
        k=np.sqrt(1.0/nnodes)
    # the initial "temperature"  is about .1 of domain area (=1x1)
    # this is the largest step allowed in the dynamics.
    # Calculate domain in case our fixed positions are bigger than 1x1
    t = max(max(pos.T[0]) - min(pos.T[0]), max(pos.T[1]) - min(pos.T[1]))*0.1
    # simple cooling scheme.
    # linearly step down by dt on each iteration so last iteration is size dt.
    dt=t/float(iterations+1)
    delta = np.zeros((pos.shape[0],pos.shape[0],pos.shape[1]),dtype=A.dtype)
    # the inscrutable (but fast) version
    # this is still O(V^2)
    # could use multilevel methods to speed this up significantly
    for iteration in range(iterations):
        # matrix of difference between points
        for i in range(pos.shape[1]):
            delta[:,:,i]= pos[:,i,None]-pos[:,i]
        # distance between points
        distance=np.sqrt((delta**2).sum(axis=-1))
        # enforce minimum distance of 0.01
        distance=np.where(distance<0.01,0.01,distance)
        # displacement "force"
        displacement=np.transpose(np.transpose(delta)*\
                                  (k*k/distance**2-A*distance/k))\
                                  .sum(axis=1)
        # update positions
        length=np.sqrt((displacement**2).sum(axis=1))
        length=np.where(length<0.01,0.01,length)
        delta_pos=np.transpose(np.transpose(displacement)*t/length)
        if fixed is not None:
            # don't change positions of fixed nodes
            delta_pos[fixed]=0.0
        pos+=delta_pos
        # cool temperature
        t-=dt
        if fixed is None:
            pos = _rescale_layout(pos)
    return pos


def _sparse_fruchterman_reingold(A, dim=2, k=None, pos=None, fixed=None,
                                 iterations=50):
    # Position nodes in adjacency matrix A using Fruchterman-Reingold
    # Entry point for NetworkX graph is fruchterman_reingold_layout()
    # Sparse version
    import numpy as np
    try:
        nnodes,_=A.shape
    except AttributeError:
        raise nx.NetworkXError(
            "fruchterman_reingold() takes an adjacency matrix as input")
    try:
        from scipy.sparse import spdiags,coo_matrix
    except ImportError:
        raise ImportError("_sparse_fruchterman_reingold() scipy numpy: http://scipy.org/ ")
    # make sure we have a LIst of Lists representation
    try:
        A=A.tolil()
    except:
        A=(coo_matrix(A)).tolil()

    if pos is None:
        # random initial positions
        pos=np.asarray(np.random.random((nnodes,dim)),dtype=A.dtype)
    else:
        # make sure positions are of same type as matrix
        pos=pos.astype(A.dtype)

    # no fixed nodes
    if fixed is None:
        fixed=[]

    # optimal distance between nodes
    if k is None:
        k=np.sqrt(1.0/nnodes)
    # the initial "temperature"  is about .1 of domain area (=1x1)
    # this is the largest step allowed in the dynamics.
    # Calculate domain in case our fixed positions are bigger than 1x1
    t = max(max(pos.T[0]) - min(pos.T[0]), max(pos.T[1]) - min(pos.T[1]))*0.1
    # simple cooling scheme.
    # linearly step down by dt on each iteration so last iteration is size dt.
    dt=t/float(iterations+1)

    displacement=np.zeros((dim,nnodes))
    for iteration in range(iterations):
        displacement*=0
        # loop over rows
        for i in range(A.shape[0]):
            if i in fixed:
                continue
            # difference between this row's node position and all others
            delta=(pos[i]-pos).T
            # distance between points
            distance=np.sqrt((delta**2).sum(axis=0))
            # enforce minimum distance of 0.01
            distance=np.where(distance<0.01,0.01,distance)
            # the adjacency matrix row
            Ai=np.asarray(A.getrowview(i).toarray())
            # displacement "force"
            displacement[:,i]+=\
                (delta*(k*k/distance**2-Ai*distance/k)).sum(axis=1)
        # update positions
        length=np.sqrt((displacement**2).sum(axis=0))
        length=np.where(length<0.01,0.01,length)
        pos+=(displacement*t/length).T
        # cool temperature
        t-=dt
        if fixed is None:
            pos = _rescale_layout(pos)
    return pos


def spectral_layout(G, dim=2, weight='weight', scale=1., center=None):
    """Position nodes using the eigenvectors of the graph Laplacian.

    Parameters
    ----------
    G : NetworkX graph or list of nodes

    dim : int
       Dimension of layout

    weight : string or None   optional (default='weight')
        The edge attribute that holds the numerical value used for
        the edge weight.  If None, then all edge weights are 1.

    scale : float optional (default 1)
        Scale factor for positions, i.e. nodes placed in a box with
        side [0, scale] or centered on `center` if provided.

    center : array-like (default scale/2 in each dim)
       Coordinate around which to center the layout.

    Returns
    -------
    dict :
       A dictionary of positions keyed by node

    Examples
    --------
    >>> G=nx.path_graph(4)
    >>> pos=nx.spectral_layout(G)

    Notes
    -----
    Directed graphs will be considered as undirected graphs when
    positioning the nodes.

    For larger graphs (>500 nodes) this will use the SciPy sparse
    eigenvalue solver (ARPACK).
    """
    # handle some special cases that break the eigensolvers
    import numpy as np

    if len(G) <= 2:
        if len(G) == 0:
            return {}
        elif len(G) == 1:
            if center is not None:
                pos = np.asarray(center)
            else:
                pos = np.ones((1,dim)) * scale * 0.5
        else: #len(G) == 2
            pos = np.array([np.zeros(dim), np.ones(dim) * scale])
            if center is not None:
                pos += np.asarray(center) - scale * 0.5
        return dict(zip(G,pos))
    try:
        # Sparse matrix
        if len(G)< 500:  # dense solver is faster for small graphs
            raise ValueError
        A = nx.to_scipy_sparse_matrix(G, weight=weight, dtype='d')
        # Symmetrize directed graphs
        if G.is_directed():
            A = A + np.transpose(A)
        pos = _sparse_spectral(A,dim)
    except (ImportError, ValueError):
        # Dense matrix
        A = nx.to_numpy_matrix(G, weight=weight)
        # Symmetrize directed graphs
        if G.is_directed():
            A = A + np.transpose(A)
        pos = _spectral(A, dim)

    pos = _rescale_layout(pos, scale)
    if center is not None:
        pos += np.asarray(center) - 0.5 * scale

    return dict(zip(G,pos))


def _spectral(A, dim=2):
    # Input adjacency matrix A
    # Uses dense eigenvalue solver from numpy
    try:
        import numpy as np
    except ImportError:
        raise ImportError("spectral_layout() requires numpy: http://scipy.org/ ")
    try:
        nnodes,_=A.shape
    except AttributeError:
        raise nx.NetworkXError(\
            "spectral() takes an adjacency matrix as input")

    # form Laplacian matrix
    # make sure we have an array instead of a matrix
    A=np.asarray(A)
    I=np.identity(nnodes,dtype=A.dtype)
    D=I*np.sum(A,axis=1) # diagonal of degrees
    L=D-A

    eigenvalues,eigenvectors=np.linalg.eig(L)
    # sort and keep smallest nonzero
    index=np.argsort(eigenvalues)[1:dim+1] # 0 index is zero eigenvalue
    return np.real(eigenvectors[:,index])

def _sparse_spectral(A,dim=2):
    # Input adjacency matrix A
    # Uses sparse eigenvalue solver from scipy
    # Could use multilevel methods here, see Koren "On spectral graph drawing"
    try:
        import numpy as np
        from scipy.sparse import spdiags
    except ImportError:
        raise ImportError("_sparse_spectral() requires scipy & numpy: http://scipy.org/ ")
    try:
        from scipy.sparse.linalg.eigen import eigsh
    except ImportError:
        # scipy <0.9.0 names eigsh differently
        from scipy.sparse.linalg import eigen_symmetric as eigsh
    try:
        nnodes,_=A.shape
    except AttributeError:
        raise nx.NetworkXError(\
            "sparse_spectral() takes an adjacency matrix as input")

    # form Laplacian matrix
    data=np.asarray(A.sum(axis=1).T)
    D=spdiags(data,0,nnodes,nnodes)
    L=D-A

    k=dim+1
    # number of Lanczos vectors for ARPACK solver.What is the right scaling?
    ncv=max(2*k+1,int(np.sqrt(nnodes)))
    # return smallest k eigenvalues and eigenvectors
    eigenvalues,eigenvectors=eigsh(L,k,which='SM',ncv=ncv)
    index=np.argsort(eigenvalues)[1:k] # 0 index is zero eigenvalue
    return np.real(eigenvectors[:,index])


def _rescale_layout(pos, scale=1.):
    # rescale to [0, scale) in each axis

    # Find max length over all dimensions
    maxlim=0
    for i in range(pos.shape[1]):
        pos[:,i] -= pos[:,i].min() # shift min to zero
        maxlim = max(maxlim, pos[:,i].max())
    if maxlim > 0:
        for i in range(pos.shape[1]):
            pos[:,i] *= scale / maxlim
    return pos

# fixture for nose tests
def setup_module(module):
    from nose import SkipTest
    try:
        import numpy
    except:
        raise SkipTest("NumPy not available")
    try:
        import scipy
    except:
        raise SkipTest("SciPy not available")
