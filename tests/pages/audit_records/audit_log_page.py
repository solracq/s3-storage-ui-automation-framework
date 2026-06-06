"""
Audit log page object skeleton.
"""

from tests.pages.base_page import BasePage


class AuditLogPage(BasePage):
    """
    Represent the admin audit log page.
    """

    URL_PATH = "/audit-logs"
