from pathlib import Path
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas


BASE_DIR = Path(__file__).resolve().parent.parent
RAW_DIR = BASE_DIR / "data" / "raw"
PDF_DIR = RAW_DIR / "pdfs"
NOTES_DIR = RAW_DIR / "notes"
VIDEOS_DIR = RAW_DIR / "videos"


def ensure_dirs() -> None:
    PDF_DIR.mkdir(parents=True, exist_ok=True)
    NOTES_DIR.mkdir(parents=True, exist_ok=True)
    VIDEOS_DIR.mkdir(parents=True, exist_ok=True)


def create_pdf(file_path: Path, title: str, lines: list[str]) -> None:
    c = canvas.Canvas(str(file_path), pagesize=letter)
    width, height = letter

    y = height - 50
    c.setFont("Helvetica-Bold", 16)
    c.drawString(50, y, title)
    y -= 30

    c.setFont("Helvetica", 11)
    for line in lines:
        if y < 60:
            c.showPage()
            y = height - 50
            c.setFont("Helvetica", 11)
        c.drawString(50, y, line)
        y -= 18

    c.save()


def create_notes() -> None:
    jira_notes = """JIRA ACCESS REQUEST NOTES

New hires must request JIRA access within the first two business days.
Steps:
1. Open the IT Service Portal.
2. Select 'Engineering Tools Access'.
3. Choose JIRA Standard Access.
4. Add your manager name and employee ID.
5. Submit the request.

Typical approval time: 4 to 8 business hours.

If access is blocked after approval:
- Contact #it-support on Slack
- Raise a Priority 3 incident
"""

    deployment_notes = """DEPLOYMENT CHECKLIST

Before deployment:
- Confirm code has passed all CI checks
- Validate environment variables
- Review rollback plan
- Notify the release channel in Slack

During deployment:
- Monitor application logs
- Check API health endpoints
- Validate frontend load time
- Confirm database migrations

After deployment:
- Run smoke tests
- Record release notes
- Update ticket status in JIRA
"""

    (NOTES_DIR / "jira_access_notes.txt").write_text(jira_notes, encoding="utf-8")
    (NOTES_DIR / "deployment_checklist.md").write_text(deployment_notes, encoding="utf-8")


def create_video_transcript() -> None:
    transcript = """TEAM_INTRO_VIDEO_TRANSCRIPT

[00:00] Welcome to the engineering onboarding session.
[00:18] In your first week, focus on system access, team introductions, and environment setup.
[00:42] You should complete VPN setup, email activation, Slack onboarding, and JIRA access.
[01:10] To request repository access, open the internal access portal and search for GitHub Enterprise permissions.
[01:40] For development environment setup, install Python, VS Code, Docker Desktop, and the internal CLI tools.
[02:10] Expense reimbursement requests are submitted through the Finance Portal under 'Employee Expenses'.
[02:40] Managers approve expense reports before Finance reviews them.
[03:00] If you are blocked, contact your onboarding buddy or the team manager.
"""

    (VIDEOS_DIR / "team_intro_video_transcript.txt").write_text(transcript, encoding="utf-8")


def create_sample_pdfs() -> None:
    onboarding_lines = [
        "Welcome to Acme Digital Solutions.",
        "This onboarding handbook helps new employees complete first-week tasks.",
        "Day 1 priorities include laptop setup, email activation, Slack access, and VPN setup.",
        "Day 2 priorities include JIRA access, GitHub Enterprise access, and meeting your onboarding buddy.",
        "Day 3 priorities include reviewing the deployment process and reading engineering documentation.",
        "If you need help, contact HR Operations or your manager.",
        "All onboarding tasks should be completed by the end of week one.",
        "Use the internal employee portal to find company policies and training materials.",
    ]

    expense_lines = [
        "Expense Policy Guide",
        "Employees can submit reimbursable expenses through the Finance Portal.",
        "Eligible expenses include travel, approved meals, conference fees, and office supplies.",
        "All expenses must be submitted within 30 days of purchase.",
        "Receipts are required for any expense above $25.",
        "Managers must approve submitted expenses before Finance processing begins.",
        "Reimbursement is typically completed within 5 to 7 business days after approval.",
        "For rejected expenses, employees should review policy comments and resubmit if needed.",
    ]

    create_pdf(PDF_DIR / "onboarding_handbook.pdf", "Onboarding Handbook", onboarding_lines)
    create_pdf(PDF_DIR / "expense_policy.pdf", "Expense Policy", expense_lines)


def main() -> None:
    ensure_dirs()
    create_sample_pdfs()
    create_notes()
    create_video_transcript()
    print("Sample company knowledge files created successfully.")


if __name__ == "__main__":
    main()
