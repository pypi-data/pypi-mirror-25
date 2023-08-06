#include <boost/foreach.hpp>

#include <boost/python.hpp>
#include <boost/python/list.hpp>
#include <boost/python/extract.hpp>

#include <vector>
#include <algorithm>
#include <iostream>
#include <sstream>
#include <iterator>
#include <boost/property_map/property_map.hpp>
#include <boost/graph/adjacency_list.hpp>

#include "edmonds_optimum_branching.hpp"

// Define a directed graph type that associates a weight with each
// edge. We store the weights using internal properties as described
// in BGL.
typedef boost::property<boost::edge_weight_t, double>       EdgeProperty;
typedef boost::adjacency_list<boost::listS,
                              boost::vecS,
                              boost::directedS,
                              boost::no_property,
                              EdgeProperty>                 Graph;
typedef boost::graph_traits<Graph>::vertex_descriptor       Vertex;
typedef boost::graph_traits<Graph>::edge_descriptor         Edge;

Graph build_graph(int N, boost::python::list edge_with_weights){
  long l = len(edge_with_weights);
  Graph g(N);
  for(int i=0; i<l; i++){
    boost::python::list edge = (boost::python::list)edge_with_weights[i];
    int source = boost::python::extract<int>(edge[0]);
    int target = boost::python::extract<int>(edge[1]);
    double weight = boost::python::extract<double>(edge[2]);

    add_edge(source, target, weight, g);
  }
  return g;
}

std::string graph_to_string(Graph &g){
    boost::property_map<Graph, boost::edge_weight_t>::type weights =
        get(boost::edge_weight_t(), g);
    
    // Print the graph (or rather the edges of the graph).
    std::stringstream ss;
    BOOST_FOREACH (Edge e, edges(g))
    {
      ss << "(" << boost::source(e, g) << ", "
	 << boost::target(e, g) << ")\t"
	 << get(weights, e) << "\n";
    }
  
    return ss.str();;
}


boost::python::list minimum_branching(Graph & g, boost::python::list roots){
  // copying the roots
  std::vector<Vertex> roots_iter;
  long length = len(roots);
  for(long i=0; i<length; i++){
    int node_id = boost::python::extract<int>(roots[i]);
    roots_iter.push_back((Vertex)node_id);
  }
    
  boost::property_map<Graph, boost::edge_weight_t>::type weights =
    get(boost::edge_weight_t(), g);
  boost::property_map<Graph, boost::vertex_index_t>::type vertex_indices =
      get(boost::vertex_index_t(), g);
  
  std::vector<Edge> branching;
  
  // bool TOptimumIsMaximum,
  // bool TAttemptToSpan,
  // bool TGraphIsDense
  edmonds_optimum_branching<false, true, true>(g,
					       vertex_indices,
					       weights,
					       roots_iter.begin(),
					       roots_iter.end(),
					       std::back_inserter(branching));
  boost::python::list l;
  BOOST_FOREACH(Edge e, branching){
    int source = (int)boost::source(e, g);
    int target = (int)boost::target(e, g);
    l.append(boost::python::make_tuple(source, target));
  }
  return l;  
}


BOOST_PYTHON_MODULE(_core) {
  using namespace boost::python;

  class_<Graph>("Graph");
  def("build_graph", build_graph);
  def("graph_to_string", graph_to_string);
  def("minimum_branching", minimum_branching);
};


// int
// main(int argc, char *argv[])
// {
//     const int N = 4;

//     // Graph with N vertices    
//     Graph G(N);

//     // Create a vector to keep track of all the vertices and enable us
//     // to index them. As a side note, observe that this is not
//     // necessary since Vertex is probably an integral type. However,
//     // this may not be true of arbitrary graphs and I think this code
//     // is a better illustration of a more general case.
//     std::vector<Vertex> the_vertices;
//     BOOST_FOREACH (Vertex v, vertices(G))
//     {
//         the_vertices.push_back(v);
//     }
    
//     // add a few edges with weights to the graph
//     add_edge(the_vertices[0], the_vertices[1], 3.0, G);
//     add_edge(the_vertices[0], the_vertices[2], 1.5, G);
//     add_edge(the_vertices[0], the_vertices[3], 1.8, G);
//     add_edge(the_vertices[1], the_vertices[2], 4.3, G);
//     add_edge(the_vertices[2], the_vertices[3], 2.2, G);

//     // This is how we can get a property map that gives the weights of
//     // the edges.
//     boost::property_map<Graph, boost::edge_weight_t>::type weights =
//         get(boost::edge_weight_t(), G);
    
//     // This is how we can get a property map mapping the vertices to
//     // integer indices.
//     boost::property_map<Graph, boost::vertex_index_t>::type vertex_indices =
//         get(boost::vertex_index_t(), G);


//     // Print the graph (or rather the edges of the graph).
//     std::cout << "This is the graph:\n";
//     BOOST_FOREACH (Edge e, edges(G))
//     {
//         std::cout << "(" << boost::source(e, G) << ", "
//                   << boost::target(e, G) << ")\t"
//                   << get(weights, e) << "\n";
//     }

//     // Find the maximum branching.
//     // std::vector<Edge> branching;
//     // edmonds_optimum_branching<true, false, false>(G,
//     //                                               vertex_indices,
//     //                                               weights,
//     //                                               static_cast<Vertex *>(0),
//     //                                               static_cast<Vertex *>(0),
//     //                                               std::back_inserter(branching));
    
//     // // Print the edges of the maximum branching
//     // std::cout << "This is the maximum branching\n";
//     // BOOST_FOREACH (Edge e, branching)
//     // {
//     //     std::cout << "(" << boost::source(e, G) << ", "
//     //               << boost::target(e, G) << ")\t"
//     //               << get(weights, e) << "\n";
//     // }
//     return 0;
// }

