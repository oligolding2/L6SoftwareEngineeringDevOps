import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parent.parent))

from functions import *
from exceptions import *
import pytest
from config import Config

def test_validate_field():
        
        # Check that the function is functioning correctly for a valid case

    assert validate_field("validcase", "testuser", min_length=6,max_length=12,allow_numbers=False) == "testuser"
        
        # Check function correctly throws an exception for a case where value is too short

    with pytest.raises(ValueError,match="must be at least"):
        validate_field("tooshortcase", "testuser", min_length=10, max_length=15,allow_numbers=False)

        # Check function correctly throws an exception for a case where value is too long

    with pytest.raises(ValueError,match="cannot exceed"):
        validate_field("toolongcase", "testuser", min_length=2, max_length=6,allow_numbers=False)

        # Check function correctly throws an exception for a case which contains numbers

    with pytest.raises(ValueError,match="must not contain"):
        validate_field("numericcase", "34563", min_length=2, max_length=6,allow_numbers=False)
        
        # Check function throws error for an empty case

    with pytest.raises(ValueError,match="cannot be empty"):
        validate_field("emptycase", value="")


def test_append(mocker):
    owner = "Test Owner"
    location = "Test Location"
    value = "Test Value"
    user = "Test User"
    executor_mocker = mocker.patch("functions.executor",return_value="Success")
    assert append(owner,location,value,user) == "Success"

    executor_mocker.assert_called_once_with(
        f"INSERT INTO mortgage (owner,location,value,inserted_by) VALUES (?,?,?,?)",
        (owner, location, value, user),
        "add",
    )


def test_read_single_retrieval(mocker):
    executor_mocker = mocker.patch("functions.executor")

    #Test single retrieval
    mock_data_single_retrieval = ("1", "Test Owner", "Test Location", "Test Value")
    executor_mocker.return_value = mock_data_single_retrieval
    assert read("1",search_all=False) == mock_data_single_retrieval
    executor_mocker.assert_called_once_with(
        "SELECT mortgage_id, owner, location, value FROM mortgage WHERE mortgage_id = ?",
        ("1",),
        "read"
    )

    # Test retrieval of all rows in table
def test_read_retrieve_all(mocker):
    executor_mocker = mocker.patch("functions.executor")
    mock_data_retrieve_all = [
        ("1", "Test Owner1", "Test Location1", "Test Value1"),
        ("2", "Test Owner2", "Test Location2", "Test Value2")
    ]
    executor_mocker.return_value = mock_data_retrieve_all
    assert read(None, search_all=True) == mock_data_retrieve_all
    executor_mocker.assert_called_once_with(
        "SELECT mortgage_id, owner, location, value FROM mortgage",
        None,
        "read"
    )

def test_read_invalid_retrieval(mocker):

    executor_mocker = mocker.patch("functions.executor")

    mock_data_invalid_retrieval = []
    executor_mocker.return_value = mock_data_invalid_retrieval

    with pytest.raises(ValueError, match="No record found"):
        read("9999",search_all=False)
    
    executor_mocker.assert_called_once_with(
        "SELECT mortgage_id, owner, location, value FROM mortgage WHERE mortgage_id = ?",
        ("9999",),
        "read"
    )


def test_delete_valid_id(mocker):
    executor_mocker = mocker.patch("functions.executor")
    mock_return_value = "Record deleted successfully."
    executor_mocker.return_value = mock_return_value

    assert delete("9999") == mock_return_value

    executor_mocker.assert_called_once_with(
        "DELETE FROM mortgage WHERE mortgage_id = ?",
        ("9999",),
        "delete"
    )

def test_update_single_field(mocker):
    executor_mocker = mocker.patch("functions.executor")
    mock_return_value = "Success"
    executor_mocker.return_value = mock_return_value

    assert update("1", name="Test New User") == mock_return_value

    executor_mocker.assert_called_once_with(
        "UPDATE mortgage SET owner = ? WHERE mortgage_id = ?",
        ("Test New User", "1"),
        "update"
    )

def test_update_multiple_fields(mocker):
    executor_mocker = mocker.patch("functions.executor")
    mock_return_value = "Success"
    executor_mocker.return_value = mock_return_value

    assert update("1", name="Test New User", location="Test New Location", value="Test New Value") == mock_return_value

    executor_mocker.assert_called_once_with(
        "UPDATE mortgage SET owner = ?, location = ?, value = ? WHERE mortgage_id = ?",
        ("Test New User", "Test New Location", "Test New Value", "1"),
        "update"
    )

def test_update_no_fields(mocker):
    executor_mocker = mocker.patch("functions.executor")
    with pytest.raises(ValueError, match="No fields provided for update."):
        update("123")
    executor_mocker.assert_not_called()

def test_create_user_valid_admin(mocker):
    executor_mocker = mocker.patch("functions.executor")
    mocker_return_value = "Success"

    executor_mocker.return_value = mocker_return_value

    assert create_user("validadmin","validpassword",Config.ADMIN_TOKEN) == mocker_return_value

    args, _ = executor_mocker.call_args
    user_id, username, password, admin = args[1]
    assert 0 <= user_id <= 9999999

    executor_mocker.assert_called_once_with(
        "INSERT INTO users (user_id, username, password, admin) VALUES (?, ?, ?, ?)",
        (user_id,  # Randomly generated user ID
        "validadmin",
        "validpassword",
        1),
        "add"
    )


def test_create_user_invalid_admin(mocker):
    with pytest.raises(CredentialError,match="Invalid admin token provided."):
        create_user(username="invalidadmin",password="validpassword",admin_token="invalidadmintoken")



def test_create_user_regular_user(mocker):
    executor_mocker = mocker.patch("functions.executor")
    executor_mocker.return_value = "Success"
    assert create_user("testuser","testpassword",None) == "Success"

    args, _ = executor_mocker.call_args
    user_id, username, password, admin = args[1]
    assert 0 <= user_id <= 9999999
    executor_mocker.assert_called_once_with(
        "INSERT INTO users (user_id, username, password, admin) VALUES (?, ?, ?, ?)",
        (user_id,  # Randomly generated user ID
        "testuser",
        "testpassword",
        0),
        "add"
    )

def test_login_user_valid_credentials(mocker):
    executor_mocker = mocker.patch("functions.executor")
    mocker_return_value = ("1","validuser","testvalidpassword",0)
    executor_mocker.return_value = mocker_return_value

    assert login_user("validuser","testvalidpassword") == mocker_return_value

    executor_mocker.assert_called_once_with(
        "SELECT * FROM users WHERE username = ? AND password = ?",
        ("validuser", "testvalidpassword"),
        "login"
    )

def test_login_user_invalid_credentials(mocker):
    executor_mocker = mocker.patch("functions.executor",return_value = None)

    with pytest.raises(CredentialError,match="no results found in database."):
        login_user("invaliduser","invalidpassword")

    executor_mocker.assert_called_once_with(
        "SELECT * FROM users WHERE username = ? AND password = ?",
        ("invaliduser", "invalidpassword"),
        "login"
    )

    


    

