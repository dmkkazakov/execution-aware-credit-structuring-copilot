import pandas as pd
import numpy as np

def build_graph_features(transactions: pd.DataFrame) -> pd.DataFrame:
    rows = []
    entities = sorted(set(transactions["sender"]).union(set(transactions["receiver"])))
    for entity in entities:
        inc = transactions[transactions.receiver == entity]
        out = transactions[transactions.sender == entity]
        total_in = inc.operating_volume.sum()
        total_out = out.operating_volume.sum()
        top3 = 0
        if len(inc) and total_in > 0:
            top3 = inc.groupby("sender").operating_volume.sum().sort_values(ascending=False).head(3).sum() / total_in
        inflow_by_m = inc.groupby("month").operating_volume.sum()
        volatility = inflow_by_m.std() / (inflow_by_m.mean() + 1e-6) if len(inflow_by_m) > 1 else 0
        rows.append({
            "entity_id": entity,
            "total_inflow": total_in,
            "total_outflow": total_out,
            "top3_inflow_concentration": top3,
            "treasury_dependency_ratio": inc.treasury_flow.sum() / (total_in + 1e-6),
            "inflow_volatility": volatility,
            "bottleneck_exposure": inc.bottleneck_flag.mean() if len(inc) else 0,
            "hidden_channel_exposure": inc.hidden_channel_flag.mean() if len(inc) else 0,
        })
    return pd.DataFrame(rows)

if __name__ == "__main__":
    tx = pd.read_csv("data/raw/transactions.csv")
    features = build_graph_features(tx)
    features.to_csv("data/processed/graph_features_rebuilt.csv", index=False)
    print(features.head())