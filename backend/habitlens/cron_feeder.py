from backend.habitlens.utils import obtain_mock_dataframe
from backend.habitlens.reporting import update_ai_reports
from backend.habitlens.correlation import phrased_correlation_insights


def run_weekly_correlation_report(start_date: str, end_date: str):
    df = obtain_mock_dataframe()
    phrases = phrased_correlation_insights(df, target_attribute="Productivity Score")

    summary = f"""Weekly correlation insights for {start_date} to {end_date}.
Target: Productivity Score
Top findings:"""

    update_ai_reports(
        start_date=start_date,
        end_date=end_date,
        summary_text=summary,
        extra_paragraphs=phrases,
        image_url=None,
    )


if __name__ == "__main__":
    run_weekly_correlation_report("2025-07-12", "2025-07-18")
