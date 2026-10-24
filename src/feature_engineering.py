import pandas as pd
from pathlib import Path

def build_graph_features(transactions: pd.DataFrame, entity_ids=None) -> pd.DataFrame:
    rows = []
    entities = set(transactions["sender"]).union(set(transactions["receiver"]))
    if entity_ids is not None:
        entities.update(entity_ids)
    months = sorted(transactions["month"].unique())
    for entity in sorted(entities):
        inc = transactions[transactions.receiver == entity]
        out = transactions[transactions.sender == entity]
        total_in = inc.operating_volume.sum()
        total_out = out.operating_volume.sum()
        top3 = 0
        if len(inc) and total_in > 0:
            top3 = inc.groupby("sender").operating_volume.sum().sort_values(ascending=False).head(3).sum() / total_in
        # Missing inflows within an observed month are zero, not missing periods.
        inflow_by_m = inc.groupby("month").operating_volume.sum().reindex(months, fill_value=0)
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
    root = Path(__file__).resolve().parents[1]
    tx = pd.read_csv(root / "data/raw/transactions.csv")
    entities = pd.read_csv(root / "data/raw/entities.csv")
    features = build_graph_features(tx, entity_ids=entities.entity_id)
    features.to_csv(root / "data/processed/graph_features_rebuilt.csv", index=False)
    print(features.head())
