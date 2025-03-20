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

2. Set up your environment variables. You can do this in two ways:

### Option 1: Using a .env file (recommended for local development)

Create a `.env` file in the project root:

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
QUANTITY=20

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

### Option 2: Setting environment variables directly (recommended for deployment)

When deploying to Fly.io, you can set these variables using the Fly CLI:

```bash
# Credentials
fly secrets set EMAIL=your_email@example.com
fly secrets set PASSWORD=your_password

# Reservation Settings
fly secrets set DESIRED_WEEKDAY=WEDNESDAY
fly secrets set DESIRED_TIME=20:00
fly secrets set RESERVATION_FREQUENCY=WEEKLY

# Time Preferences
fly secrets set DESIRED_TIME_MILITARY=20:00:00
fly secrets set ALT_DESIRED_TIMES_MILITARY=19:00:00,21:00:00

# Field Preferences
fly secrets set DESIRED_FIELD_STARTS_WITH="FIELD - Main"
fly secrets set FACILITY_GROUP_ID=28

# Activity Settings
fly secrets set SPORT=Soccer
fly secrets set RESERVATION_NAME="Local Sports Club Practice"
fly secrets set QUANTITY=20

# Scheduling Settings
fly secrets set SCHEDULE_WEEKDAY=MONDAY
fly secrets set SCHEDULE_TIME=09:00
fly secrets set SCHEDULE_FREQUENCY=WEEKLY

# Deployment Settings
fly secrets set HEADLESS=true
fly secrets set MAX_RETRIES=3
fly secrets set RETRY_DELAY=5
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

This bot is configured to run on Fly.io, which provides a reliable platform for running scheduled tasks.

### Prerequisites

1. Install the [Fly CLI](https://fly.io/docs/hands-on/install-flyctl/)
2. Sign up for a [Fly.io account](https://fly.io/docs/hands-on/sign-up-for-fly/)
3. Login to Fly.io:

```bash
fly auth login
```

### Deployment Steps

1. Create a new Fly.io app:

```bash
fly apps create sf-rec
```

2. Set up your environment variables using the commands in Option 2 above.

3. Deploy the application:

```bash
fly deploy
```

4. Monitor the logs:

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
