from flask import Flask, request, jsonify
from src.account_registry import AccountRegistry
from src.account import Account

app = Flask(__name__)
registry = AccountRegistry()

@app.route("/api/accounts", methods=['POST'])
def create_account():
    data = request.get_json()
    print(f"Create account request: {data}")

    if registry.search_account(data["pesel"]) is not None:
        return jsonify({"message": "Account with this PESEL already exists"}), 409

    account = Account(data["name"], data["surname"], data["pesel"])
    registry.add_account(account)
    return jsonify({"message": "Account created"}), 201

@app.route("/api/accounts", methods=['GET'])
def get_all_accounts():
    print("Get all accounts request received")
    accounts = registry.show_registry()
    accounts_data = [{"name": acc.first_name, "surname": acc.last_name, "pesel":
        acc.pesel, "balance": acc.balance} for acc in accounts]
    return jsonify(accounts_data), 200

@app.route("/api/accounts/count", methods=['GET'])
def get_account_count():
    print("Get account count request received")
    count = registry.count_accounts()
    return jsonify({"count": count}), 200

@app.route("/api/accounts/<pesel>", methods=['GET'])
def get_account_by_pesel(pesel):
    account = registry.search_account(pesel)
    if account is not None:
        return jsonify({
            "name": account.first_name,
            "surname": account.last_name,
            "pesel": account.pesel,
            "balance": account.balance
        }), 200

    return jsonify({"message": "Account not found"}), 404

@app.route("/api/accounts/<pesel>", methods=['PATCH'])
def update_account(pesel):
    data = request.get_json()
    if not data or (not data.get("name") and not data.get("surname")):
        return jsonify({"message": "Request body must contain 'name' and/or 'surname'"}), 400
    account = registry.search_account(pesel)
    if not account:
        return jsonify({"message": "Account not found"}), 404
    if "name" in data:
        account.first_name = data["name"]
    if "surname" in data:
        account.last_name = data["surname"]
    return jsonify({"message": "Account updated"}), 200

@app.route("/api/accounts/<pesel>", methods=['DELETE'])
def delete_account(pesel):
    account = registry.search_account(pesel)
    if not account:
        return jsonify({"message": "Account not found"}), 404
    registry.delete_account(pesel)
    return jsonify({"message": "Account deleted"}), 200