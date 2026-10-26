"""A small, explainable ad-budget optimization agent.

This script is intentionally API-free so beginners can run it in Colab.
"""

from pathlib import Path
import numpy as np
import pandas as pd

SYSTEM_PROMPT = """You are an explainable advertising budget optimization agent.
Use prior campaign performance to recommend the next day's budget across Search,
Social, and Display. Maximize expected conversions, obey every budget guardrail,
and explain each recommendation in plain language. Never use future data.
"""


class AdOptimizationAgent:
    """Recommend daily channel budgets using prior performance and guardrails."""

    def __init__(self, daily_budget=300.0, min_budget=60.0, max_budget=180.0,
                 max_change=0.20, lookback_days=7):
        self.daily_budget = daily_budget
        self.min_budget = min_budget
        self.max_budget = max_budget
        self.max_change = max_change
        self.lookback_days = lookback_days
        self.channels = ["Search", "Social", "Display"]

    def show_system_prompt(self):
        """Tool: display the agent's role and operating instructions."""
        return SYSTEM_PROMPT.strip()

    def read_data(self, csv_path):
        """Tool: read and validate the campaign CSV."""
        data = pd.read_csv(csv_path)
        required = {"date", "channel", "spend", "impressions", "clicks", "conversions"}
        missing = required - set(data.columns)
        if missing:
            raise ValueError(f"Missing required columns: {sorted(missing)}")
        data["date"] = pd.to_datetime(data["date"])
        if set(data["channel"].unique()) != set(self.channels):
            raise ValueError(f"The CSV must contain exactly these channels: {self.channels}")
        return data.sort_values(["date", "channel"]).reset_index(drop=True)

    def calculate_metrics(self, data):
        """Tool: calculate channel performance metrics."""
        metrics = data.groupby("channel", as_index=False).agg(
            spend=("spend", "sum"), impressions=("impressions", "sum"),
            clicks=("clicks", "sum"), conversions=("conversions", "sum"))
        metrics["ctr"] = metrics["clicks"] / metrics["impressions"]
        metrics["cvr"] = metrics["conversions"] / metrics["clicks"]
        metrics["conversion_yield"] = metrics["conversions"] / metrics["spend"]
        metrics["cpa"] = metrics["spend"] / metrics["conversions"]
        return metrics

    def _guardrailed_allocation(self, scores, previous):
        """Allocate the full budget while enforcing floor, ceiling, and change caps."""
        raw = self.daily_budget * scores / scores.sum()
        max_shift = previous * self.max_change
        proposed = previous + np.clip(raw - previous, -max_shift, max_shift)
        proposed = np.clip(proposed, self.min_budget, self.max_budget)

        # Redistribute rounding/constraint residual without breaking the caps.
        for _ in range(20):
            residual = self.daily_budget - proposed.sum()
            if abs(residual) < 0.01:
                break
            room = (self.max_budget - proposed) if residual > 0 else (proposed - self.min_budget)
            room = np.maximum(room, 0)
            if room.sum() == 0:
                break
            proposed += residual * room / room.sum()
            proposed = np.clip(proposed, self.min_budget, self.max_budget)
        return proposed

    def recommend_budgets(self, data):
        """Tool: make one recommendation per day and log the reason."""
        dates = sorted(data["date"].unique())
        previous = pd.Series(self.daily_budget / len(self.channels), index=self.channels)
        allocations = []
        logs = []

        for date in dates:
            history = data[data["date"] < date].tail(self.lookback_days * len(self.channels))
            if history.empty:
                metrics = pd.DataFrame({"channel": self.channels, "conversion_yield": [1, 1, 1]})
                scores = pd.Series(1.0, index=self.channels)
                reason_template = "No prior data was available, so the agent used an equal split."
            else:
                metrics = self.calculate_metrics(history)
                scores = metrics.set_index("channel")["conversion_yield"].reindex(self.channels).fillna(0)
                scores = scores.clip(lower=0.0001)
                reason_template = "Budget follows prior conversion yield while respecting guardrails."

            proposed = self._guardrailed_allocation(scores.to_numpy(), previous.to_numpy())
            for channel, budget in zip(self.channels, proposed):
                change = budget - previous[channel]
                if change > 0.01:
                    detail = f"{channel} increased by ${change:.2f} because its prior conversion yield was strong."
                elif change < -0.01:
                    detail = f"{channel} decreased by ${abs(change):.2f} to fund stronger channels while keeping the minimum floor."
                else:
                    detail = f"{channel} stayed near ${budget:.2f} because the change cap and allocation balance limited movement."
                logs.append({"date": date.date().isoformat(), "channel": channel,
                             "previous_budget": previous[channel], "recommended_budget": budget,
                             "reason": detail})
                allocations.append({"date": date.date().isoformat(), "channel": channel,
                                    "recommended_budget": budget})
            previous = pd.Series(proposed, index=self.channels)

        return pd.DataFrame(allocations), pd.DataFrame(logs)

    def evaluate(self, data, allocations):
        """Tool: compare optimized budgets with an equal-split baseline."""
        rates = data.groupby("channel").agg(conversions=("conversions", "sum"), spend=("spend", "sum"))
        rates["conversion_yield"] = rates["conversions"] / rates["spend"]
        result = allocations.copy()
        result["expected_conversions"] = result.apply(
            lambda row: row["recommended_budget"] * rates.loc[row["channel"], "conversion_yield"], axis=1)
        optimized_conversions = result["expected_conversions"].sum()
        optimized_spend = result["recommended_budget"].sum()

        baseline = data[["date", "channel"]].copy()
        baseline["baseline_budget"] = self.daily_budget / len(self.channels)
        baseline["expected_conversions"] = baseline.apply(
            lambda row: row["baseline_budget"] * rates.loc[row["channel"], "conversion_yield"], axis=1)
        baseline_conversions = baseline["expected_conversions"].sum()
        baseline_spend = baseline["baseline_budget"].sum()

        comparison = pd.DataFrame([
            {"strategy": "Optimized agent", "expected_conversions": optimized_conversions,
             "spend": optimized_spend, "blended_cpa": optimized_spend / optimized_conversions},
            {"strategy": "Equal-split baseline", "expected_conversions": baseline_conversions,
             "spend": baseline_spend, "blended_cpa": baseline_spend / baseline_conversions},
        ])
        comparison["conversion_lift_vs_baseline"] = (
            comparison["expected_conversions"] / baseline_conversions - 1
        )
        return comparison, result


def run(csv_path="ad_campaign_data.csv"):
    agent = AdOptimizationAgent()
    data = agent.read_data(csv_path)
    metrics = agent.calculate_metrics(data)
    allocations, decision_log = agent.recommend_budgets(data)
    comparison, detail = agent.evaluate(data, allocations)

    print("\nCHANNEL PERFORMANCE METRICS")
    print(metrics.round(4).to_string(index=False))
    print("\nFINAL DAY BUDGETS")
    print(allocations[allocations["date"] == allocations["date"].max()].round(2).to_string(index=False))
    print("\nEVALUATION")
    print(comparison.round(4).to_string(index=False))
    print("\nDECISION LOG SAMPLE")
    print(decision_log.head(9).to_string(index=False))
    return data, metrics, allocations, decision_log, comparison, detail


if __name__ == "__main__":
    run()
