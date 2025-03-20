from playwright.sync_api import Page


# Extractions
def get_customer_id(page: Page) -> int:
    """
    Gets the customer ID from the login page by searching through the Redux state structure.

    Args:
        page (Page): Playwright page object

    Returns:
        int: The customer ID from the user's account

    Raises:
        ValueError: If the customer ID cannot be found
    """
    nodes = page.evaluate("window.__reduxInitialState")["loginUser"]["_root"][
        "entries"
    ][0][1]["_root"]["nodes"]

    for node in nodes:
        if "entry" in node and node["entry"][0] == "customerid":
            return node["entry"][1]

    raise ValueError("Could not find customer ID in page state")
