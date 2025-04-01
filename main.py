from playwright.sync_api import sync_playwright, Page
import requests
import re
from src._utils.utils import get_customer_id
from src._utils.date_utils import (
    calculate_request_date,
    military_to_american,
    format_date_for_calendar,
)
from src._utils.logger import setup_logger
from src._utils.field_utils import find_available_fields, FieldInfo, TimeSlotDetail
from src._utils.env import settings

logger = setup_logger()


def main():
    """
    Main function to automate the SF Rec field reservation process.
    Handles login, field selection, form filling, and checkout.
    """
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=settings.headless)
        context = browser.new_context()
        page = context.new_page()

        customer_id = login(page)

        # TODO: add retry logic here
        reservation_form(page, customer_id)
        details_and_policy_questions(page)
        confirm_booking(page)
        checkout_form(page)

        context.close()
        browser.close()


def login(page: Page):
    """
    Handles the login process for SF Rec website.

    Args:
        page (Page): Playwright page object
    """
    page.goto(
        "https://anc.apm.activecommunities.com/sfrecpark/signin",
        wait_until="networkidle",
    )

    # email
    email_input = page.locator(
        "#main-content-body > div.layout__container--default.an-main__wrapper > div.an-module-container.module-sign > div > div > div > div:nth-child(1) > div.input-group.input-group--m.input-group--ng.intput__clear--detault > input"
    )
    email_input.fill(settings.sf_rec_email)

    # password
    password_input = page.locator(
        "#main-content-body > div.layout__container--default.an-main__wrapper > div.an-module-container.module-sign > div > div > div > div:nth-child(2) > div.input-group.input-group--m.input-group--ng.intput__clear--detault > input"
    )
    password_input.fill(settings.sf_rec_password)

    # submit button
    signin_button = page.locator(".btn-super")
    signin_button.click()

    page.wait_for_timeout(3000)  # Add delay to ensure login is complete

    # get customer id
    return get_customer_id(page)


def reservation_form(page: Page, customer_id: int):
    """
    Navigates to the reservation page, selects date, adds reservation name, and finds + selects available fields.
    Checks both primary and alternate times for availability.

    Args:
        page (Page): Playwright page object
        customer_id (int): The customer's ID for the API request
    """
    page.goto(
        f"https://anc.apm.activecommunities.com/sfrecpark/reservation/landing/quick?groupId={settings.facility_group_id}",
    )

    request_date = calculate_request_date()

    # calendar
    calendar_button = page.locator(".filter-section__date-time input")
    calendar_button.click()
    calendar = page.locator(".an-calendar")

    # Try to find the date in the current month view
    formatted_date = format_date_for_calendar(request_date)
    max_attempts = 3  # Maximum number of months to look ahead
    attempt = 0

    while attempt < max_attempts:
        desired_date = calendar.get_by_label(formatted_date)
        if desired_date.is_visible():
            desired_date.click()
            break

        next_button = calendar.get_by_role("button", name="Next")
        next_button.click()
        page.wait_for_timeout(500)  # Wait for calendar to update
        attempt += 1

    if attempt >= max_attempts:
        raise ValueError(
            f"Could not find date {request_date} in calendar after {max_attempts} attempts"
        )

    page.wait_for_timeout(3000)

    # reservation name
    name_input = page.locator("div.event-input .input-group__field")
    name_input.fill(settings.reservation_name)

    # get availability
    response = get_availability_details(page, request_date, customer_id)
    availability = response["body"]["availability"]
    time_slots = availability["time_slots"]
    all_fields = availability["resources"]

    fields = [
        FieldInfo(
            resource_id=field["resource_id"],
            resource_name=field["resource_name"],
            time_slots=time_slots,
            time_slot_details=[
                TimeSlotDetail(**detail, time=time)
                for detail, time in zip(field["time_slot_details"], time_slots)
            ],
        )
        for field in all_fields
    ]

    # Find available fields
    available_field, selected_time = find_available_fields(
        fields=fields,
        primary_time=settings.desired_time_military,
        alternate_times=settings.alt_desired_times_military,
        field_prefix=settings.desired_field_starts_with,
    )

    if not available_field:
        logger.error(
            f"No fields available at {settings.desired_time_military} or any alternate times: {', '.join(settings.alt_desired_times_military)}"
        )
        exit()

    # select field
    aria_label = available_field.resource_name
    start_time = military_to_american(selected_time)
    timeslot_selector = re.compile(f"^{aria_label} {start_time}")

    field_cell = page.get_by_label(timeslot_selector)

    table_header = field_cell.locator("..").locator("..")

    quantity_stepper = table_header.locator("input")
    quantity_stepper.fill(str(settings.group_quantity))

    field_cell.click()

    page.wait_for_timeout(1000)

    confirm_button = page.locator(".booking-detail__btn--continue")
    confirm_button.click()


def get_availability_details(page: Page, request_date: str, customer_id: int):
    """
    Makes an API request to get field availability details.

    Args:
        page (Page): Playwright page object
        request_date (str): Date to check availability for

    Returns:
        dict: JSON response containing availability details
    """
    try:
        # cserf token and cookies
        csrf_token = page.evaluate("window.__csrfToken")

        cookies = page.context.cookies()
        cookie_dict: dict[str, str] = {}
        for cookie in cookies:
            if "name" in cookie and "value" in cookie:
                cookie_dict[cookie["name"]] = cookie["value"]

        # get availability data
        response = requests.post(
            url="https://anc.apm.activecommunities.com/sfrecpark/rest/reservation/quickreservation/availability?locale=en-US",
            json={
                "facility_group_id": settings.facility_group_id,
                "customer_id": customer_id,
                "company_id": 0,
                "reserve_date": request_date,
                "resident": False,
                "reload": False,
                "change_time_range": False,
            },
            cookies=cookie_dict,
            headers={
                "Content-Type": "application/json",
                "Accept": "application/json",
                "x-csrf-token": csrf_token,
                "x-requested-with": "XMLHttpRequest",
            },
        )

        response.raise_for_status()

        return response.json()
    except Exception as e:
        raise e


def details_and_policy_questions(page: Page):
    """
    Fills out the reservation details form including activity type and policy questions.

    Note:
        All selectors are from using the dev tools -> Super ugly

    Args:
        page (Page): Playwright page object
        activity (str): Type of activity to select
    """

    # modal
    modal = page.locator(".modal.is-open")
    modal.wait_for(state="visible", timeout=10000)

    # activity dropdown
    activity_dropdown = page.locator(
        "#main-content-body > div > div.an-module-container > div > div > div.modal-wrap > div.modal.is-open.quick-need-to-answer > section > div.modal-body > div.enroll-question > div.an-survey > fieldset > div > div:nth-child(1) > fieldset > div > div.afx-col.question-answer-container.enroll-question-answer > div > div > div.dropdown__button.input__field"
    )
    activity_dropdown.click()
    activity_option = page.locator(f"li[title='{settings.sport}']")
    activity_option.scroll_into_view_if_needed()
    activity_option.click()

    # policy questions
    policy_question_selectors = [
        "#main-content-body > div > div.an-module-container > div > div > div.modal-wrap > div.modal.is-open.quick-need-to-answer > section > div.modal-body > div.enroll-question > div.an-survey > fieldset > div > div:nth-child(2) > fieldset > div > div.afx-col.question-answer-container.enroll-question-answer > div > div > div.dropdown__button.input__field",
        "#main-content-body > div > div.an-module-container > div > div > div.modal-wrap > div.modal.is-open.quick-need-to-answer > section > div.modal-body > div.enroll-question > div.an-survey > fieldset > div > div:nth-child(3) > fieldset > div > div.afx-col.question-answer-container.enroll-question-answer > div > div > div.dropdown__button.input__field",
        "#main-content-body > div > div.an-module-container > div > div > div.modal-wrap > div.modal.is-open.quick-need-to-answer > section > div.modal-body > div.enroll-question > div.an-survey > fieldset > div > div:nth-child(4) > fieldset > div > div.afx-col.question-answer-container.enroll-question-answer > div > div > div.dropdown__button.input__field",
        "#main-content-body > div > div.an-module-container > div > div > div.modal-wrap > div.modal.is-open.quick-need-to-answer > section > div.modal-body > div.enroll-question > div.an-survey > fieldset > div > div:nth-child(5) > fieldset > div > div.afx-col.question-answer-container.enroll-question-answer > div > div > div.dropdown__button.input__field",
    ]
    for selector in policy_question_selectors:
        dropdown = page.locator(selector)
        dropdown.click()

        dropdown_parent = dropdown.locator("..")

        yes_option = dropdown_parent.locator("li[title='Yes']")
        yes_option.scroll_into_view_if_needed()
        yes_option.click()

    # waiver checkbox
    waiver_checkbox = page.locator(
        "label:has-text('I have read and agree to ATHLETIC FIELD TERMS AND CONDITIONS') input[type='checkbox']"
    )
    waiver_checkbox.check()

    # save button
    save_button = page.get_by_role("button", name="Save")
    save_button.click()


def confirm_booking(page: Page):
    """
    Confirms the booking by clicking through confirmation buttons.

    Args:
        page (Page): Playwright page object
    """

    # confirm button
    confirm_button = page.locator(".booking-detail__btn--continue")
    confirm_button.click()

    # confirm button
    confirm_button = page.locator(".modal-box .btn-strong")
    confirm_button.click()

    page.wait_for_timeout(3000)
    page.wait_for_load_state("networkidle")


def checkout_form(page: Page):
    """
    Fills out the payment form in the checkout iframe.

    Args:
        page (Page): Playwright page object
    """

    # Need to wait for iframe to be present
    iframe = page.frame_locator("iframe[name='primaryPCIPaymentIframe']")

    # cvv
    cvv = iframe.locator(".form-control")
    cvv.wait_for(state="visible")
    cvv.fill(settings.cvv)

    # submit button
    pay_button = page.locator(".pay__button")
    pay_button.click()

    page.wait_for_timeout(10000)


if __name__ == "__main__":
    main()
