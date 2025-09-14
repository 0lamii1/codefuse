from decimal import Decimal
from django.shortcuts import get_object_or_404
from app.models import Transaction, Wallet, Transaction 

def update_wallet_transaction(status: str, reference: str):
    transaction = get_object_or_404(Transaction, reference=reference)

    if status.lower() == "success":
        transaction.status = Transaction.TransactionStatus.SUCCESS

        wallet = transaction.wallet
        wallet.balance = wallet.balance + transaction.amount
        wallet.save()

    elif status.lower() == "abandoned":
        transaction.status = Transaction.TransactionStatus.CANCELLED

    elif status.lower() == "failed":
        transaction.status = Transaction.TransactionStatus.FAILED

    transaction.save()


def verify_debit(amount, user):
    wallet = get_object_or_404(Wallet, user=user)
    amount = Decimal(amount)

    if wallet.balance >= amount:
        wallet.balance = wallet.balance - amount
        wallet.save()
        return True
    return False
