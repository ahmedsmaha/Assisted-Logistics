AI_NOTES

Prompts used (examples):

1. "Help me write Python code to normalize order IDs like ' Ord-001 ' and 'ord001' to a canonical form 'ORD-001', parse multiple date formats, and dedupe orders by ID."
2. "Design tie-breaking logic for courier assignment: prefer lower priority, then lower assigned weight, then lexicographically smaller courier ID."

What I changed/verified after suggestions:

-   Chose deterministic ordering: orders sorted by deadline then ID; couriers sorted by priority, assigned load, courierId.
-   Implemented simple Levenshtein-based address conflict detection and emit warnings.

One thing GPT suggested that I corrected:

-   Initial idea treated dailyCapacity as number-of-orders; I changed it to treat dailyCapacity as weight-capacity per the problem description and sample tests.

# AI Notes: Using an AI Assistant for Development

This document describes how an AI assistant (like GPT-4 or Gemini) was leveraged effectively to build the logistics reconciliation program. The focus was on using the AI for boilerplate code, complex logic formulation, and debugging, rather than for end-to-end code generation.

### Prompt 1: Structuring the Data Cleaning Logic

-   **Prompt:** "I need to write a Python function to clean and merge a list of messy order dictionaries. The task is to group orders by a normalized `orderId`. For each group of duplicates, I need to merge them into a single order by preferring non-empty fields, and for the `deadline` field, I must always choose the earliest timestamp. Can you outline the logic and data structures for this?"

-   **How it Helped:** This prompt was crucial for structuring Part A. The AI suggested using a dictionary to group orders by the normalized ID (`orders_by_id = {}`), which is an efficient way to handle duplicates. It also provided a clear, step-by-step process for iterating through the duplicate groups and merging them, preventing bugs related to incorrect merging logic.

-   **My Change/Refinement:** The AI's initial code for merging was generic. I had to specifically adapt it to handle the `deadline` by writing a robust `parse_deadline` helper function that could manage multiple date formats (`YYYY-MM-DD` and `YYYY/MM/DD`), a requirement the AI missed initially. I also integrated the specific normalization rules from the requirements (`orderId` trimming, `paymentType` coercion, etc.).

### Prompt 2: Implementing the Tie-Breaking Logic

-   **Prompt:** "Write a Python snippet that filters a list of 'eligible courier' objects. The selection must follow three strict tie-breaking rules in order: 1. Select couriers with the lowest 'priority' value. 2. From that group, select those with the lowest current workload (an integer). 3. If a tie still exists, select the courier whose 'courierId' comes first alphabetically."

-   **How it Helped:** The tie-breaking logic is sequential and can be tricky to implement correctly. The AI provided a clean and correct implementation using a series of list comprehensions and a final sort. This saved time and avoided a common source of errors where tie-breakers might be applied in the wrong order.

-   **My Change/Refinement:** The AI-generated snippet was a standalone function. I integrated this logic directly into the main assignment loop of my program, making it work with my `capacity_usage` dictionary, which tracks the workloads in real-time. This ensured the logic was applied contextually for each order being assigned.

### One Thing the AI Got Wrong (and I Fixed)

-   **The Problem:** I asked the AI to generate the full reconciliation logic (Part C). Its initial version correctly identified `missing` and `late` orders. However, for calculating `overloadedCouriers`, it mistakenly used the _planned_ total weight from `plan.json` instead of the _actual_ total weight derived from the `log.csv` deliveries.

-   **The Fix:** The requirement is to check if the _actual delivered weight_ exceeds capacity. I corrected the AI's logic by creating a new dictionary, `actual_courier_loads`, and iterating through the `log.csv` data. For each delivery, I looked up the order's weight in the `clean_orders.json` map and added it to the actual load of the delivering courier. This ensured the overload check was based on ground truth (the log) rather than the plan. This demonstrates the need for careful review of AI-generated code against precise requirements.
