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

# 모든 경로를 미리 계산하고 캐싱
import asyncio
all_paths: AllPaths = asyncio.run(bfs_all_paths(graph))

def get_path(start: str, end: str) -> List[str]:
    paths = all_paths.get(start, {}).get(end, [])
    return paths[0] if paths else []