from robocorp.tasks import task
from robocorp import browser
from RPA.Archive import Archive

from RPA.HTTP import HTTP
from RPA.PDF import PDF
from RPA.Tables import Tables

@task
def order_robots_from_RobotSpareBin():
    """
    Orders robots from RobotSpareBin Industries Inc.
    Saves the order HTML receipt as a PDF file.
    Saves the screenshot of the ordered robot.
    Embeds the screenshot of the robot to the PDF receipt.
    Creates ZIP archive of the receipts and the images.
    """

    browser.configure(
        slowmo=100
    )
    open_website()
    download_order_csv()
    archive_receipts()
   
def open_website():
    """Open Website"""
    browser.goto("https://robotsparebinindustries.com/#/robot-order")
    browser.page().wait_for_load_state(state="networkidle")

def download_order_csv():
    """Download the needed csv-file and make it a table"""
    http = HTTP()
    http.download(url="https://robotsparebinindustries.com/orders.csv", overwrite=True)
    orders = Tables().read_table_from_csv(path="orders.csv", header=True)
    for row in orders:
        fill_order_form(row)

def close_annoying_modal():
    """Closes annoying modal"""
    browser.page()
    page=browser.page()
    locator_modal = page.get_by_role("button", name="OK")
    if locator_modal.is_visible():
        locator_modal.click()

def fill_order_form(orders):
    """Closes the modal at the beginning, fill in the order form and submit it"""
    browser.page()
    page = browser.page()
    browser.page().wait_for_load_state(state="networkidle")

    close_annoying_modal()
    page.select_option("#head", orders["Head"])
    page.set_checked("#id-body-"+str(orders['Body']), True)
    page.fill(".form-control:nth-child(3)", orders["Legs"])
    page.fill("#address", orders["Address"])
    page.click("#order")
    alert_handler(orders)

def alert_handler(orders):
    browser.page()
    page=browser.page()
    pdf = PDF()
    browser.page().wait_for_load_state(state="networkidle")
    
    while page.locator(".alert-danger").is_visible() == True:
            page.click("#order")

    page.locator("#receipt").screenshot(path="output/receipt" + str(orders["Order number"]) + ".png")
    page.locator("#robot-preview-image").screenshot(path="output/preview" + str(orders["Order number"]) + ".png")
 
    list_of_files = [
    'output/receipt' + str(orders["Order number"]) + '.png', 
    'output/preview' + str(orders["Order number"]) + '.png']
    pdf.add_files_to_pdf(
    files=list_of_files, 
    target_document="output/receipts" + str(orders["Order number"]) + ".pdf")
    page.click("#order-another")

def archive_receipts():
    Archive()
    archive=Archive()

    archive.archive_folder_with_zip("output/", archive_name="Receipts.zip")