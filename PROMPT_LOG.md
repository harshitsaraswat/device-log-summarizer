# Prompt Log (Section 3: Chart)

## Initial prompt
> "go and create it as a college task, not that much high priority. It should
> be simple, easy."

(Sent along with the assessment PDF. This produced `section3_chart.py`, which
loads `summary.json` and plots average temperature per device with matplotlib.)

## Bug / formatting mistake in the first attempt
- The value label on the tallest bar ("75.2") touched the top border of the
  chart, because the y-axis had no space above the highest bar.
- The x-axis labels were rotated 45 degrees, which wasn't needed for short
  names like `DEV_A` and made the chart look messy.

## Follow-up prompt used to fix it
> "Fill in PROMPT_LOG.md, keep it easy and simple."

While working on this, the chart was checked and fixed:
`ax.set_ylim(0, max(temps) * 1.1)` adds headroom above the bars, and the
label rotation was removed. I re-ran the script and checked the new chart.
