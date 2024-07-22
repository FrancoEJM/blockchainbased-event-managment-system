from typing import List, Dict
from models import blc_models as blc_md


def convert_nodes(nodes: List[blc_md.NODOS]) -> List[Dict]:
    result = []
    for node in nodes:
        result.append(
            {"ip": f"{node.ip}:{node.port}", "tiempo_esperado": node.tiempo_esperado}
        )
    return result
