import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.metrics import roc_auc_score, average_precision_score, brier_score_loss
from sklearn.ensemble import GradientBoostingClassifier

def main():
    entities = pd.read_csv("data/raw/entities.csv")
    features = pd.read_csv("data/processed/graph_features.csv")
    df = entities.merge(features, on="entity_id", how="inner")

    y = df["default_flag"]
    X = df.drop(columns=["entity_id", "sector", "country", "default_flag"])

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=.25, random_state=2026, stratify=y
    )

    model = GradientBoostingClassifier(random_state=2026)
    model.fit(X_train, y_train)
    p = model.predict_proba(X_test)[:, 1]

    print({
        "roc_auc": round(roc_auc_score(y_test, p), 4),
        "pr_auc": round(average_precision_score(y_test, p), 4),
        "brier": round(brier_score_loss(y_test, p), 4)
    })

if __name__ == "__main__":
    main()