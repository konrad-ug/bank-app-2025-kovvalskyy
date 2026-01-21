from flask import Flask, request, jsonify
from src.account_registry import AccountRegistry
from src.account import Account
from src.repositories.mongo_accounts_repository import MongoAccountsRepository

app = Flask(__name__)
registry = AccountRegistry()
repo = MongoAccountsRepository()

@app.route("/api/accounts", methods=['POST'])
def create_account():
    data = request.get_json()
    print(f"Create account request: {data}")
    account = Account(data["name"], data["surname"], data["pesel"])
    if not registry.add_account(account):
        return jsonify({"message": "Account with this PESEL already exists"}), 409
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

@app.route("/api/accounts/<pesel>/transfer", methods=["POST"])
def transfer(pesel):
    account = registry.search_account(pesel)
    if not account:
        return jsonify({"message": "Account not found"}), 404

    data = request.get_json(silent=True) or {}
    transfer_type = data.get("type")
    amount = data.get("amount")

    allowed_types = {"incoming", "outgoing", "express"}
    if transfer_type not in allowed_types:
        return jsonify({"message": "Unknown transfer type"}), 400

    try:
        amount = float(amount)
    except (TypeError, ValueError):
        return jsonify({"message": "Invalid amount"}), 400

    type_to_method = {
        "incoming": account.transfer_in,
        "outgoing": account.transfer_out,
        "express": account.express_out,
    }

    success = type_to_method[transfer_type](amount)

    if success:
        return jsonify({"message": "Processing transfer"}), 200

    return jsonify({"message": "Transfer rejected"}), 422

@app.route("/api/accounts/save", methods=["POST"])
def save_accounts():
    repo.save_all(registry.show_registry())
    return jsonify({"message": "saved"}), 200


@app.route("/api/accounts/load", methods=["POST"])
def load_accounts():
    accounts = repo.load_all()
    registry.clear()
    registry.set_accounts(accounts)
    return jsonify({"message": "loaded"}), 200