#!/usr/bin/env python
from builtins import range
from builtins import object
from nose.tools import *
from networkx import *
from networkx.generators.random_graphs import *

class TestGeneratorsRandom(object):
    def smoke_test_random_graph(self):
        seed = 42
        G=gnp_random_graph(100,0.25,seed)
        G=binomial_graph(100,0.25,seed)
        G=erdos_renyi_graph(100,0.25,seed)
        G=fast_gnp_random_graph(100,0.25,seed)
        G=gnm_random_graph(100,20,seed)
        G=dense_gnm_random_graph(100,20,seed)

        G=watts_strogatz_graph(10,2,0.25,seed)
        assert_equal(len(G), 10)
        assert_equal(G.number_of_edges(), 10)

        G=connected_watts_strogatz_graph(10,2,0.1,seed)
        assert_equal(len(G), 10)
        assert_equal(G.number_of_edges(), 10)

        G=watts_strogatz_graph(10,4,0.25,seed)
        assert_equal(len(G), 10)
        assert_equal(G.number_of_edges(), 20)

        G=newman_watts_strogatz_graph(10,2,0.0,seed)
        assert_equal(len(G), 10)
        assert_equal(G.number_of_edges(), 10)

        G=newman_watts_strogatz_graph(10,4,0.25,seed)
        assert_equal(len(G), 10)
        assert_true(G.number_of_edges() >= 20)

        G=barabasi_albert_graph(100,1,seed)
        G=barabasi_albert_graph(100,3,seed)
        assert_equal(G.number_of_edges(),(97*3))

        G=powerlaw_cluster_graph(100,1,1.0,seed)
        G=powerlaw_cluster_graph(100,3,0.0,seed)
        assert_equal(G.number_of_edges(),(97*3))

        G=duplication_divergence_graph(100,1.0,seed)
        assert_equal(len(G), 100)
        assert_raises(networkx.exception.NetworkXError,
                      duplication_divergence_graph, 100, 2)
        assert_raises(networkx.exception.NetworkXError,
                      duplication_divergence_graph, 100, -1)

        G=random_regular_graph(10,20,seed)

        assert_raises(networkx.exception.NetworkXError,
                      random_regular_graph, 3, 21)

        constructor=[(10,20,0.8),(20,40,0.8)]
        G=random_shell_graph(constructor,seed)

        G=nx.random_lobster(10,0.1,0.5,seed)

    def test_random_zero_regular_graph(self):
        """Tests that a 0-regular graph has the correct number of nodes and
        edges.

        """
        G = random_regular_graph(0, 10)
        assert_equal(len(G), 10)
        assert_equal(len(G.edges()), 0)

    def test_gnp(self):
        for generator in [gnp_random_graph, binomial_graph, erdos_renyi_graph,
                          fast_gnp_random_graph]:
            G = generator(10, -1.1)
            assert_equal(len(G), 10)
            assert_equal(len(G.edges()), 0)

            G = generator(10, 0.1)
            assert_equal(len(G), 10)

            G = generator(10, 0.1, seed=42)
            assert_equal(len(G), 10)

            G = generator(10, 1.1)
            assert_equal(len(G), 10)
            assert_equal(len(G.edges()), 45)

            G = generator(10, -1.1, directed=True)
            assert_true(G.is_directed())
            assert_equal(len(G), 10)
            assert_equal(len(G.edges()), 0)

            G = generator(10, 0.1, directed=True)
            assert_true(G.is_directed())
            assert_equal(len(G), 10)

            G = generator(10, 1.1, directed=True)
            assert_true(G.is_directed())
            assert_equal(len(G), 10)
            assert_equal(len(G.edges()), 90)

            # assert that random graphs generate all edges for p close to 1
            edges = 0
            runs = 100
            for i in range(runs):
                edges += len(generator(10, 0.99999, directed=True).edges())
            assert_almost_equal(edges/float(runs), 90, delta=runs*2.0/100)

    def test_gnm(self):
        G=gnm_random_graph(10,3)
        assert_equal(len(G),10)
        assert_equal(len(G.edges()),3)

        G=gnm_random_graph(10,3,seed=42)
        assert_equal(len(G),10)
        assert_equal(len(G.edges()),3)

        G=gnm_random_graph(10,100)
        assert_equal(len(G),10)
        assert_equal(len(G.edges()),45)

        G=gnm_random_graph(10,100,directed=True)
        assert_equal(len(G),10)
        assert_equal(len(G.edges()),90)

        G=gnm_random_graph(10,-1.1)
        assert_equal(len(G),10)
        assert_equal(len(G.edges()),0)

    def test_watts_strogatz_big_k(self):
        assert_raises(networkx.exception.NetworkXError,
                watts_strogatz_graph, 10, 10, 0.25)
        assert_raises(networkx.exception.NetworkXError,
                newman_watts_strogatz_graph, 10, 10, 0.25)
        # could create an infinite loop, now doesn't
        # infinite loop used to occur when a node has degree n-1 and needs to rewire
        watts_strogatz_graph(10, 9, 0.25, seed=0)
        newman_watts_strogatz_graph(10, 9, 0.5, seed=0)
