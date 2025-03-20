# SF Rec Field Reservation Bot

This bot automates the process of reserving fields at SF Rec facilities.

## TODO

- Test
- API
- UI

## Prereqs

- Create account
- Add payment

## Setup

1. Install dependencies:

```bash
pip install -r requirements.txt
```

2. Set up your environment variables:

Create a `.env` file in the project root. Copy over the `.env.example` and edit to your preference:

```bash
# Credentials
SF_REC_EMAIL=your_email@example.com
SF_REC_PASSWORD=your_password

# Time Preferences
DESIRED_TIME_MILITARY="20:00:00"
ALT_DESIRED_TIMES_MILITARY="19:00:00,21:00:00"

# Field Preferences
DESIRED_FIELD_STARTS_WITH="FIELD - Main" 
FACILITY_GROUP_ID=28

# Activity Settings
SPORT="Soccer"
RESERVATION_NAME="Local Sports Club Practice"
GROUP_QUANTITY=20

# Reservation Settings
DESIRED_WEEKDAY="WEDNESDAY"
DESIRED_TIME="20:00"
RESERVATION_FREQUENCY="WEEKLY"

# Scheduling Settings
SCHEDULE_WEEKDAY="MONDAY"  # When to run the job
SCHEDULE_TIME="09:00"     # What time to run the job
SCHEDULE_FREQUENCY="WEEKLY"  # How often to run the job

# Deployment Settings
HEADLESS=true
MAX_RETRIES=3
RETRY_DELAY=5
```

## Running the Bot

### One-time Run

To run the bot once:

```bash
python -m main
```

### Scheduled Run

To run the bot on a schedule:

```bash
python -m scheduler
```

The scheduler will run the bot according to the configured schedule (default: every Monday at 9:00 AM). It will:

1. Check for available fields at the specified time
2. Try alternate times if the primary time is unavailable
3. Automatically fill out the reservation form
4. Log all activities and any errors

## Deployment

This bot is configured to run on Fly.io. To deploy:

1. Install the [Fly CLI](https://fly.io/docs/hands-on/install-flyctl/)

2. Login to Fly.io:
```bash
fly auth login
```

3. Create a new Fly.io app (first time only):
```bash
fly apps create sf-rec
```

4. Deploy the application:
```bash
fly deploy
```

### Managing Secrets

The bot uses a git pre-push hook to automatically sync your local `.env` file with Fly.io secrets when pushing to main/master. You have two options for managing secrets:

1. **Using the Pre-push Hook** (Recommended):
   - Your secrets will automatically sync when pushing to main/master
   - You'll be shown what secrets will be synced and asked for confirmation
   - Use `git push --dry-run` to preview what would be synced without making changes

2. **Using Fly.io Dashboard**:
   - Go to https://fly.io/apps/sf-rec/secrets
   - Manually manage your secrets through the web interface
   - Use the same variable names as shown in the `.env.example` file

## Monitoring

Monitor your deployment using:
```bash
fly logs
```

## Logging

Logs are written to `sf_rec.log` in the project root directory when running locally.
When deployed to Fly.io, logs are available through the Fly.io dashboard or CLI.

## Notes

- The bot uses Playwright for browser automation
- Make sure you have a stable internet connection
- The bot will automatically handle login and form filling
- Payment information should be saved in your account
- The bot runs in headless mode by default (configurable via HEADLESS environment variable)
- The scheduler runs independently of the reservation time (e.g., you can schedule the bot to run on Monday mornings to book Wednesday evening slots)
