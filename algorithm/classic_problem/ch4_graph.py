from __future__ import annotations
from dataclasses import dataclass
from typing import Generic, List, Optional, Tuple, TypeVar


@dataclass
class Edge:
    u: int  ## from vertex u, index of vertex
    v: int  ## to vertex v, index of vertex

    def reversed(self) -> Edge:
        return Edge(self.v, self.u)
    
    def __str__(self) -> str:
        return f'{self.u} -> {self.v}'


@dataclass
class WeightedEdge(Edge):
    weight : float
    
    def reversed(self) -> WeightedEdge:
        return WeightedEdge(self.v, self.u, self.weight)

    def __lt__(self, other : WeightedEdge) -> bool:
        return self.weight < other.weight
    
    def __str__(self) -> str:
        return f'{self.u} {self.weight} -> {self.v}'


V = TypeVar('V')

class Graph(Generic[V]):
    def __init__(self, vertices : List[V] = []) -> None:
        self._vertices = vertices
        self._edges : List[List[Edge]] = [[] for _ in vertices]
    
    @property
    def vertex_count(self) -> int:
        return len(self._vertices)
    
    @property
    def edge_count(self) -> int:
        return sum(map(len, self._edges))
    
    ## Add vertex to graph and return index
    def add_vertex(self, vertex: V) -> int:
        self._vertices.append(vertex)
        self._edges.append([])  ## Add empty edge
        return self.vertex_count - 1
    
    ## Add undirected edge
    def add_edge(self, edge: Edge) -> None:
        self._edges[edge.u].append(edge)
        self._edges[edge.v].append(edge.reversed())
    
    ## Add edge with index of vertex
    def add_edge_by_indices(self, u: int, v: int) -> None:
        edge : Edge = Edge(u, v)
        self.add_edge(edge)
    
    def add_edge_by_vertices(self, first: V, second: V) -> None:
        u = self._vertices.index(first)
        v = self._vertices.index(second)
        self.add_edge_by_indices(u, v)
    
    def vertex_at(self, index: int) -> V:
        return self._vertices[index]

    def index_of(self, vertex: V) -> int:
        return self._vertices.index(vertex)

    def neighbors_for_index(self, index: int) -> List[V]:
        #return [ self.vertex_at(edge.v) for edge in self._edges[index] ]
        return list(map(self.vertex_at, [edge.v for edge in self._edges[index]]))
    
    def neighbors_for_vertex(self, vertex: V) -> List[V]:
        return self.neighbors_for_index(self.index_of(vertex))
    
    def edges_for_index(self, index: int) -> List[Edge]:
        return self._edges[index]
    
    def edges_for_vertex(self, vertex: V) -> List[Edge]:
        return self.edges_for_index(self.vertex_at(vertex))
    
    def __str__(self) -> str:
        desc : str = ""
        for i in range(self.vertex_count):
            desc += f"{self.vertex_at(i)} -> {self.neighbors_for_index(i)}\n"
        return desc


class WeightedGraph(Generic[V], Graph[V]):
    def __init__(self, vertices : List[V] = []) -> None:
        self._vertices : List[V] = vertices
        self._edges : List[List[WeightedEdge]] = [[] for _ in vertices]

    def add_edge_by_indices(self,
        u : int,
        v : int,
        weight : float
        ) -> None:
        
        edge = WeightedEdge(u, v, weight)
        self.add_edge(edge)

    def add_edge_by_vertices(self,
        first : V,
        second : V,
        weight : float
        ) -> None:
        
        u : int = self.index_of(first)
        v : int = self.index_of(second)
        self.add_edge_by_indices(u, v, weight)

    def neighbors_for_index_with_weights(self,
        index : int
        ) -> List[Tuple[V, float]]:

        distance_tuples : List[Tuple[V, float]] = []
        for edge in self.edges_for_index(index):
            distance_tuples.append(
                (self.vertex_at(edge.v), edge.weight))
        
        return distance_tuples
    
    def __str__(self) -> str:
        desc = ''
        for i in range(self.vertex_count):
            desc += f'{self.vertex_at(i)} -> {self.neighbors_for_index_with_weights(i)}\n'
        return desc
        

if __name__ == '__main__':
    ## test graph
    city_graph : Graph[str] = Graph(['시애틀', '샌프란시스코', '로스앤젤레스',
    '리버사이드', '피닉스', '시카고', '보스턴', '뉴욕', '애틀랜타', '마이애미', 
    '댈러스', '휴스턴', '디트로이트', '필라델피아', '워싱턴'])
    
    city_graph.add_edge_by_vertices('시애틀', '시카고')
    city_graph.add_edge_by_vertices('시애틀', '샌프란시스코')
    city_graph.add_edge_by_vertices('시카고', '리버사이드')
    city_graph.add_edge_by_vertices('시카고', '댈러스')
    city_graph.add_edge_by_vertices('시카고', '애틀랜타')
    city_graph.add_edge_by_vertices('시카고', '디트로이트')
    city_graph.add_edge_by_vertices('샌프란시스코', '리버사이드')
    city_graph.add_edge_by_vertices('샌프란시스코', '로스앤젤레스')
    city_graph.add_edge_by_vertices('리버사이드', '로스앤젤레스')
    city_graph.add_edge_by_vertices('리버사이드', '피닉스')
    city_graph.add_edge_by_vertices('댈러스', '피닉스')
    city_graph.add_edge_by_vertices('댈러스', '휴스턴')
    city_graph.add_edge_by_vertices('댈러스', '애틀랜타')
    city_graph.add_edge_by_vertices('애틀랜타', '휴스턴')
    city_graph.add_edge_by_vertices('애틀랜타', '워싱턴')
    city_graph.add_edge_by_vertices('애틀랜타', '마이애미')
    city_graph.add_edge_by_vertices('디트로이트', '워싱턴')
    city_graph.add_edge_by_vertices('디트로이트', '뉴욕')
    city_graph.add_edge_by_vertices('디트로이트', '보스턴')
    city_graph.add_edge_by_vertices('로스앤젤레스', '피닉스')
    city_graph.add_edge_by_vertices('피닉스', '휴스턴')
    city_graph.add_edge_by_vertices('휴스턴', '마이애미')
    city_graph.add_edge_by_vertices('워싱턴', '필라델피아')
    city_graph.add_edge_by_vertices('워싱턴', '마이애미')
    city_graph.add_edge_by_vertices('뉴욕', '보스턴')
    city_graph.add_edge_by_vertices('뉴욕', '필라델피아')
    print(city_graph)
    
    ## find the shortest path from boston to miami using bfs algorithm
    import sys
    sys.path.insert(0, '.')
    from ch2_search import bfs, Node, node_to_path
    
    bfs_result: Optional[Node[V]] = bfs('보스턴', lambda x : x == '마이애미',
        city_graph.neighbors_for_vertex)
    
    if bfs_result is None:
        print('Not found with bfs algorithm')
    else:
        path: List[V] = node_to_path(bfs_result)
        print('보스턴에서 마이애미까지 최단 경로:')
        print(path)
        print()
    
    ## test weighted graph
    city_graph : WeightedGraph[str] = WeightedGraph(['시애틀', '샌프란시스코', '로스앤젤레스',
    '리버사이드', '피닉스', '시카고', '보스턴', '뉴욕', '애틀랜타', '마이애미', 
    '댈러스', '휴스턴', '디트로이트', '필라델피아', '워싱턴'])
    
    city_graph.add_edge_by_vertices('시애틀', '시카고', 1737)
    city_graph.add_edge_by_vertices('시애틀', '샌프란시스코', 678)
    city_graph.add_edge_by_vertices('시카고', '리버사이드', 1704)
    city_graph.add_edge_by_vertices('시카고', '댈러스', 805)
    city_graph.add_edge_by_vertices('시카고', '애틀랜타', 588)
    city_graph.add_edge_by_vertices('시카고', '디트로이트', 238)
    city_graph.add_edge_by_vertices('샌프란시스코', '리버사이드', 386)
    city_graph.add_edge_by_vertices('샌프란시스코', '로스앤젤레스', 348)
    city_graph.add_edge_by_vertices('리버사이드', '로스앤젤레스', 50)
    city_graph.add_edge_by_vertices('리버사이드', '피닉스', 307)
    city_graph.add_edge_by_vertices('댈러스', '피닉스', 887)
    city_graph.add_edge_by_vertices('댈러스', '휴스턴', 225)
    city_graph.add_edge_by_vertices('댈러스', '애틀랜타', 721)
    city_graph.add_edge_by_vertices('애틀랜타', '휴스턴', 702)
    city_graph.add_edge_by_vertices('애틀랜타', '워싱턴', 543)
    city_graph.add_edge_by_vertices('애틀랜타', '마이애미', 604)
    city_graph.add_edge_by_vertices('디트로이트', '워싱턴', 396)
    city_graph.add_edge_by_vertices('디트로이트', '뉴욕', 482)
    city_graph.add_edge_by_vertices('디트로이트', '보스턴', 613)
    city_graph.add_edge_by_vertices('로스앤젤레스', '피닉스', 357)
    city_graph.add_edge_by_vertices('피닉스', '휴스턴', 1015)
    city_graph.add_edge_by_vertices('휴스턴', '마이애미', 968)
    city_graph.add_edge_by_vertices('워싱턴', '필라델피아', 123)
    city_graph.add_edge_by_vertices('워싱턴', '마이애미', 923)
    city_graph.add_edge_by_vertices('뉴욕', '보스턴', 190)
    city_graph.add_edge_by_vertices('뉴욕', '필라델피아', 81)
    print(city_graph)
