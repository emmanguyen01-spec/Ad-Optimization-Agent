# Scaling Note

To run this agent in the cloud, a scheduled job could execute the Python workflow once per day using Google Cloud Run Jobs, AWS Lambda with a scheduler, or an Azure Function. The campaign platform would provide the previous day's spend, impressions, clicks, and conversions through a protected API. The agent would write its recommended budgets and decision logs to a database or cloud storage location for review before any live campaign update.

Monitoring should track whether the data arrived on time, whether required columns are present, whether budgets stay within guardrails, total conversions, CPA, CTR, latency, and errors. Each run should have a timestamp and unique run ID so a human can reproduce the decision. Alerts should be sent when a channel receives missing or unusual data, when CPA changes sharply, or when the agent fails.

Cost controls include a fixed daily budget cap, API rate limits, a maximum number of retries, scheduled execution only once per day, and a human approval step before publishing changes. A production version should begin in recommendation-only mode and use a rollback plan before it is allowed to change live advertising budgets automatically.
