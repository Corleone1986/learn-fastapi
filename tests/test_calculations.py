import pytest
from app.calculations import add , BankAccount, InsufficientFunds


@pytest.fixture
def zero_bank_account():
    return BankAccount()


@pytest.fixture
def bank_account():
    return BankAccount(50)

@pytest.mark.parametrize("num1 , num2 , expected", [
    (2 , 3 , 5),
    (7 , 3 , 10),
    (15, 4 , 19)
])
def test_add(num1 , num2 , expected):
    assert add(num1, num2) == expected


def test_bank_set_initial_amount(bank_account):
    # bank_account = BankAccount(50)
    assert bank_account.balance == 50


def test_bank_defult_amount(zero_bank_account):
    assert zero_bank_account.balance == 0



def test_deposit(bank_account):
    # bank_account = BankAccount(50)
    bank_account.deposit(10)
    assert bank_account.balance == 60
   

def test_withdraw(bank_account):
    # bank_account = BankAccount(50)
    bank_account.withdraw(10)
    assert bank_account.balance == 40

def test_collect_interest(bank_account):
    # bank_account = BankAccount(50)
    bank_account.collect_interest()
    assert round(bank_account.balance, 6) == 55

@pytest.mark.parametrize("deposited , withdraw , expected", [
    (200 , 100 , 100),
    (500, 300 , 200),
    (1200, 500 , 700)
])
def test_bank_transection(zero_bank_account,deposited,withdraw, expected ):
    zero_bank_account.deposit(deposited)
    zero_bank_account.withdraw(withdraw)
    assert zero_bank_account.balance == expected


def test_insufficient_fund(bank_account):
    with pytest.raises(ZeroDivisionError): #  or pytest.raises(InsufficientFunds)
        bank_account.withdraw(200)

