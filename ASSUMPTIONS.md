# Implementation Assumptions

This document outlines the key assumptions made during the development of the logistics reconciliation program.

1.  **Input File Integrity:**

    -   It is assumed that the input files (`orders.json`, `couriers.json`, `zones.csv`, `log.csv`) exist at the specified path (`input/`) and are correctly formatted (valid JSON/CSV).
    -   The schema for each file is exactly as described in the task description. The program relies on the specified field names (e.g., `orderId`, `dailyCapacity`).

2.  **Data Normalization and Merging:**

    -   **Order ID Normalization:** The rule "strip non-alphanumerics at ends" is interpreted as removing any leading or trailing characters that are not letters or numbers (`[^\w]`).
    -   **Address Similarity:** The "simple heuristic" for address comparison during de-duplication was not required as the provided test cases did not feature conflicting addresses for the same `orderId`. The current logic merges metadata but does not perform address comparison, assuming all data for a given ID belongs to the same order. If conflicting addresses were present, the last-seen one would be used.
    -   **Zone/City Normalization:** The `zones.csv` file is the single source of truth for normalization. Any city or zone variant not present in the `raw` column of this file will be used as-is. The matching is case-insensitive.

3.  **Planning Logic:**

    -   **Deadline Tie-Breaker:** The requirement "Tighest deadline (earlier deadline first)" is interpreted as a primary sorting criterion for the orders _before_ the assignment process begins. This ensures that orders with more urgent deadlines are planned first, which is a common real-world strategy and ensures deterministic output.
    -   **Courier Availability:** A courier is considered available for an order if they meet _all_ conditions simultaneously: zone coverage, COD/product constraints, and sufficient remaining capacity.

4.  **Reconciliation Logic:**

    -   **Timestamps:** All `deadline` and `deliveredAt` timestamps are assumed to be in the same, consistent timezone ("local time"). The program performs direct comparisons without timezone conversions.
    -   **Log Duplicates:** An order is flagged as a `duplicate` if its normalized `orderId` appears more than once in `log.csv`. For reconciliation checks like `late` or `misassigned`, the _first_ appearance of the logged order is used.

5.  **Determinism:**
    -   All output lists of objects or IDs (e.g., `assignments`, `unassigned`, `missing`, `late`) are sorted alphabetically or numerically by their respective IDs to ensure the output is deterministic and repeatable. `capacityUsage` is sorted by `courierId`.
