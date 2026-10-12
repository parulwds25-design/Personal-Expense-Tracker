# Personal Expense Tracker

A Python command-line utility for recording and analyzing expenses. Assessment III updates add validated input, persistent CSV records, category and monthly summaries, deletion, total spending, and two generated charts.

## Setup and run

Use Python 3.10 or later. Install dependencies and start the application:

```bash
python -m pip install -r requirements.txt
python main.py
```

The app reads and writes `expenses.csv` using the existing `Date,Category,Amount,Description` format and `YYYY-MM-DD` dates. It preserves existing records. Choose **6. Generate graphs** to create `charts/category_spending.png` and `charts/monthly_spending.png`; the images open on desktop systems when supported.

## Features

- Add, view, search, and delete expenses.
- Summarize totals by category and month, and show the overall total.
- Validate dates and positive amounts.
- Save records across runs in CSV format.
- Generate a category bar chart and a monthly spending trend chart with Matplotlib.

## Program logic

`main()` routes menu choices to small functions. `load_expenses()` and `save_expenses()` handle CSV data, summary functions aggregate it, and `generate_graph()` saves both charts as PNG images.

## Assessment III demo

1. Add sample expenses across at least two categories and two months.
2. Demonstrate the summaries and select option 6 to show both charts.
3. Restart the program to show that records persist.
4. Commit the final code and submit the consolidated report PDF required by the course handout.
