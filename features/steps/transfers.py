from behave import step, then
import requests

URL = "http://localhost:5000"

@step('I make "{transfer_type}" transfer of "{amount}" to account with pesel: "{pesel}"')
def make_transfer(context, transfer_type, amount, pesel):
    json_body = {"amount": int(amount), "type": transfer_type}
    resp = requests.post(URL + f"/api/accounts/{pesel}/transfer", json=json_body)
    context.last_response = resp

@then('Last response status code equals: "{code}"')
def last_status_code_equals(context, code):
    assert hasattr(context, "last_response"), "No last_response in context. Did you call transfer step?"
    assert context.last_response.status_code == int(code)
