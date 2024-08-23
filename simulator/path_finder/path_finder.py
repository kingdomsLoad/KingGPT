from collections import deque
from typing import Dict, List, Any

Graph = Dict[str, List[str]]
Paths = Dict[str, List[List[str]]]
AllPaths = Dict[str, Paths]

async def bfs_all_paths(graph: Graph) -> AllPaths:
    all_paths: Dict[str, Dict[str, List[List[str]]]] = {}
    for start in graph:
        paths: Dict[str, List[List[str]]] = {start: [[start]]}
        queue: deque = deque([start])
        while queue:
            node = queue.popleft()
            for neighbor in graph[node]:
                if neighbor not in paths:
                    paths[neighbor] = [path + [neighbor] for path in paths[node]]
                    queue.append(neighbor)
                else:
                    new_paths = [path + [neighbor] for path in paths[node] if neighbor not in path]
                    paths[neighbor].extend(new_paths)
        all_paths[start] = paths
    return all_paths

# 그래프 정의 (인접 리스트 형태)
graph: Graph = {
    'LoginPage': ['MainPage'],
    'MainPage': ['DeckEditPage'],
    'DeckEditPage': ['MainPage', 'EvalPage', 'BattlePage'],
    'EvalPage': ['DeckEditPage'],
    'BattlePage': ['DeckEditPage']
}

# 모든 경로 계산
all_paths: AllPaths = bfs_all_paths(graph)

# 결과 출력
async def print_result():
    for start_node in graph:
        for end_node in graph:
            if start_node != end_node:
                paths: List[List[str]] = all_paths[start_node].get(end_node, [])
                if paths:
                    print(f'경로 {start_node} -> {end_node}: {paths[0]}')  # 첫 번째 경로만 출력
                else:
                    print(f'경로 {start_node} -> {end_node}: 존재하지 않음')