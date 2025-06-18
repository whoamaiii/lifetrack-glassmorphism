import os
import uuid
import pytest
import pandas as pd
from datetime import datetime, date, timedelta

# Pytest should handle adding the root directory to sys.path
from logic import (
    add_task,
    load_tasks,
    edit_task,
    update_task_status,
    delete_task,
    DEFAULT_TASKS_CSV_FILENAME # Import the default, though tests will use a temp file
)

BASE_TEST_CSV_FILENAME = "test_tasks.csv"

@pytest.fixture
def temp_csv_file():
    """
    Fixture to provide a path to a temporary CSV file for tasks during tests.
    It ensures the test CSV is created fresh and cleaned up after each test.
    """
    current_working_dir = os.getcwd()
    test_file_path = os.path.join(current_working_dir, BASE_TEST_CSV_FILENAME)

    # Ensure no pre-existing test file from a previous failed run
    if os.path.exists(test_file_path):
        try:
            os.remove(test_file_path)
        except Exception as e:
            # If removal fails, it might cause test issues, but proceed.
            print(f"[Fixture Setup] ERROR removing pre-existing file: {e}")
            
    yield test_file_path  # Provide the absolute temp filename to the test

    # Teardown: remove the temp CSV file after the test
    if os.path.exists(test_file_path):
        try:
            os.remove(test_file_path)
        except Exception as e:
            # If removal fails, it might affect subsequent unrelated runs if not cleaned manually.
            print(f"[Fixture Teardown] ERROR removing file post-test: {e}")

# --- Tests for add_task ---

def test_add_task_only_description(temp_csv_file):
    description = "Test task only description"
    add_task(description, filename=temp_csv_file)

    df = load_tasks(filename=temp_csv_file)
    assert len(df) == 1
    task = df.iloc[0]
    assert task['description'] == description
    assert task['status'] == 'pending'
    assert pd.isna(task['due_date'])
    assert pd.isna(task['priority'])
    assert isinstance(task['created_at'], datetime)

def test_add_task_with_due_date_and_priority(temp_csv_file):
    description = "Test task with all fields"
    due_date_str = "2024-12-31"
    priority = "high"
    add_task(description, due_date=due_date_str, priority=priority, filename=temp_csv_file)

    df = load_tasks(filename=temp_csv_file)
    assert len(df) == 1
    task = df.iloc[0]
    assert task['description'] == description
    assert task['status'] == 'pending'
    assert task['due_date'] == date(2024, 12, 31)
    assert task['priority'] == priority
    assert isinstance(task['created_at'], datetime)

def test_add_task_invalid_due_date_format(temp_csv_file):
    with pytest.raises(ValueError, match="Invalid due_date format"):
        add_task("Task with invalid due date", due_date="31-12-2024", filename=temp_csv_file)

def test_add_task_invalid_priority(temp_csv_file):
    with pytest.raises(ValueError, match="Invalid priority"):
        add_task("Task with invalid priority", priority="urgent", filename=temp_csv_file)

def test_add_task_empty_description(temp_csv_file):
    with pytest.raises(ValueError, match="Task description cannot be empty"):
        add_task("", filename=temp_csv_file)
    with pytest.raises(ValueError, match="Task description cannot be empty"):
        add_task("   ", filename=temp_csv_file)

def test_add_task_saves_created_at_as_iso_string(temp_csv_file):
    description = "Test created_at format"
    add_task(description, filename=temp_csv_file)

    assert os.path.exists(temp_csv_file)
    raw_df = pd.read_csv(temp_csv_file)
    assert len(raw_df) == 1
    created_at_str = raw_df.iloc[0]['created_at']
    try:
        datetime.fromisoformat(created_at_str)
    except ValueError:
        pytest.fail(f"created_at '{created_at_str}' is not a valid ISO format string in CSV.")

def test_add_task_saves_empty_string_for_missing_optional_fields(temp_csv_file):
    description = "Task missing optionals"
    add_task(description, filename=temp_csv_file)

    raw_df = pd.read_csv(temp_csv_file)
    assert len(raw_df) == 1
    row = raw_df.iloc[0]
    assert row['due_date'] == "" or pd.isna(row['due_date'])
    assert row['priority'] == "" or pd.isna(row['priority'])

# --- Tests for load_tasks ---

def test_load_tasks_non_existent_csv(temp_csv_file):
    if os.path.exists(temp_csv_file): # Ensure it's gone if fixture didn't catch it (it should)
        os.remove(temp_csv_file)
    df = load_tasks(filename=temp_csv_file)
    expected_columns = ['task_id', 'description', 'status', 'created_at', 'due_date', 'priority']
    assert df.empty
    assert list(df.columns) == expected_columns

def test_load_tasks_empty_csv(temp_csv_file):
    open(temp_csv_file, 'w').close()
    df = load_tasks(filename=temp_csv_file)
    expected_columns = ['task_id', 'description', 'status', 'created_at', 'due_date', 'priority']
    assert df.empty
    assert list(df.columns) == expected_columns

    pd.DataFrame(columns=expected_columns).to_csv(temp_csv_file, index=False)
    df_header_only = load_tasks(filename=temp_csv_file)
    assert df_header_only.empty
    assert list(df_header_only.columns) == expected_columns

def test_load_tasks_old_format_csv(temp_csv_file):
    old_format_data = [{'task_id': str(uuid.uuid4()), 'description': 'Old task 1', 'status': 'pending', 'created_at': datetime.now().isoformat()}]
    old_df = pd.DataFrame(old_format_data)
    old_df.to_csv(temp_csv_file, index=False, columns=['task_id', 'description', 'status', 'created_at'])

    df = load_tasks(filename=temp_csv_file)
    assert len(df) == 1
    task = df.iloc[0]
    assert task['description'] == 'Old task 1'
    assert pd.isna(task['due_date'])
    assert pd.isna(task['priority'])

def test_load_tasks_new_format_csv(temp_csv_file):
    task_id = str(uuid.uuid4())
    created_time = datetime.now()
    due_date_obj = date(2025, 1, 1)
    data = [{'task_id': task_id, 'description': 'New task with all fields', 'status': 'pending', 'created_at': created_time.isoformat(), 'due_date': due_date_obj.isoformat(), 'priority': 'medium'}]
    pd.DataFrame(data).to_csv(temp_csv_file, index=False)

    df = load_tasks(filename=temp_csv_file)
    assert len(df) == 1
    task = df.iloc[0]
    assert task['task_id'] == task_id
    assert task['description'] == 'New task with all fields'
    assert task['created_at'].replace(microsecond=0) == created_time.replace(microsecond=0)
    assert task['due_date'] == due_date_obj
    assert task['priority'] == 'medium'

def test_load_tasks_status_filter(temp_csv_file):
    tasks_data = [
        {'task_id': str(uuid.uuid4()), 'description': 'Pending Task', 'status': 'pending', 'created_at': datetime.now().isoformat(), 'due_date': '', 'priority': ''},
        {'task_id': str(uuid.uuid4()), 'description': 'Completed Task', 'status': 'completed', 'created_at': datetime.now().isoformat(), 'due_date': '', 'priority': ''},
    ]
    pd.DataFrame(tasks_data).to_csv(temp_csv_file, index=False)

    df_pending = load_tasks(status_filter='pending', filename=temp_csv_file)
    assert len(df_pending) == 1
    assert df_pending.iloc[0]['description'] == 'Pending Task'

    df_completed = load_tasks(status_filter='completed', filename=temp_csv_file)
    assert len(df_completed) == 1
    assert df_completed.iloc[0]['description'] == 'Completed Task'

def test_load_tasks_parses_dates_correctly(temp_csv_file):
    created_at_dt = datetime(2023, 1, 10, 12, 30, 50, 123456)
    due_date_dt = date(2023, 2, 15)
    data = [
        {'task_id': str(uuid.uuid4()), 'description': 'Date parsing test', 'status': 'pending', 'created_at': created_at_dt.isoformat(), 'due_date': due_date_dt.isoformat(), 'priority': 'low'},
        {'task_id': str(uuid.uuid4()), 'description': 'No due date test', 'status': 'pending', 'created_at': datetime.now().isoformat(), 'due_date': '', 'priority': 'low'}
    ]
    pd.DataFrame(data).to_csv(temp_csv_file, index=False)

    df = load_tasks(filename=temp_csv_file)
    task1 = df[df['description'] == 'Date parsing test'].iloc[0]
    task2 = df[df['description'] == 'No due date test'].iloc[0]

    assert isinstance(task1['created_at'], datetime)
    assert task1['created_at'] == created_at_dt
    assert isinstance(task1['due_date'], date)
    assert task1['due_date'] == due_date_dt
    assert pd.isna(task2['due_date'])

def test_load_tasks_missing_optional_columns_in_csv_file(temp_csv_file):
    tasks_data = [{'task_id': str(uuid.uuid4()), 'description': 'Task 1 old format', 'status': 'pending', 'created_at': datetime.now().isoformat()}]
    pd.DataFrame(tasks_data, columns=['task_id', 'description', 'status', 'created_at']).to_csv(temp_csv_file, index=False)

    df = load_tasks(filename=temp_csv_file)
    assert len(df) == 1
    assert 'due_date' in df.columns
    assert 'priority' in df.columns
    assert pd.isna(df.iloc[0]['due_date'])
    assert pd.isna(df.iloc[0]['priority'])

def test_load_tasks_mixed_tasks_new_and_old_format_in_csv(temp_csv_file):
    task_id_old, task_id_new = str(uuid.uuid4()), str(uuid.uuid4())
    created_old, created_new = datetime.now() - timedelta(days=1), datetime.now()
    due_date_new = date.today()
    csv_content = (
        "task_id,description,status,created_at,due_date,priority\n"
        f"{task_id_old},Old Mixed Task,pending,{created_old.isoformat()},,\n"
        f"{task_id_new},New Mixed Task,pending,{created_new.isoformat()},{due_date_new.isoformat()},high\n"
    )
    with open(temp_csv_file, 'w') as f:
        f.write(csv_content)

    df = load_tasks(filename=temp_csv_file)
    assert len(df) == 2
    old_task = df[df['task_id'] == task_id_old].iloc[0]
    new_task = df[df['task_id'] == task_id_new].iloc[0]
    assert pd.isna(old_task['due_date'])
    assert pd.isna(old_task['priority'])
    assert new_task['due_date'] == due_date_new
    assert new_task['priority'] == "high"

@pytest.fixture
def sample_tasks_fixture(temp_csv_file):
    task1_id, task2_id, task3_id = str(uuid.uuid4()), str(uuid.uuid4()), str(uuid.uuid4())
    tasks_data = [
        {'task_id': task1_id, 'description': 'Task 1 for edit', 'status': 'pending', 'created_at': (datetime.now() - timedelta(days=2)).isoformat(), 'due_date': '2024-01-01', 'priority': 'low'},
        {'task_id': task2_id, 'description': 'Task 2 for status update', 'status': 'pending', 'created_at': (datetime.now() - timedelta(days=1)).isoformat(), 'due_date': '2024-02-01', 'priority': 'medium'},
        {'task_id': task3_id, 'description': 'Task 3 for deletion', 'status': 'completed', 'created_at': datetime.now().isoformat(), 'due_date': '', 'priority': 'high'},
    ]
    pd.DataFrame(tasks_data).to_csv(temp_csv_file, index=False) # Use the yielded path
    return {'task1_id': task1_id, 'task2_id': task2_id, 'task3_id': task3_id}

# --- Tests for edit_task ---

def test_edit_task_all_fields(temp_csv_file, sample_tasks_fixture):
    task_id = sample_tasks_fixture['task1_id']
    new_desc, new_status, new_due_date_str, new_priority = "Updated description", "completed", "2024-12-25", "high"
    edit_task(task_id, description=new_desc, status=new_status, due_date=new_due_date_str, priority=new_priority, filename=temp_csv_file)
    df = load_tasks(filename=temp_csv_file)
    edited_task = df[df['task_id'] == task_id].iloc[0]
    assert edited_task['description'] == new_desc
    assert edited_task['status'] == new_status
    assert edited_task['due_date'] == date(2024, 12, 25)
    assert edited_task['priority'] == new_priority

def test_edit_task_clear_due_date_and_priority(temp_csv_file, sample_tasks_fixture):
    task_id = sample_tasks_fixture['task1_id']
    edit_task(task_id, due_date="", priority="", filename=temp_csv_file)
    df = load_tasks(filename=temp_csv_file)
    edited_task = df[df['task_id'] == task_id].iloc[0]
    assert pd.isna(edited_task['due_date'])
    assert pd.isna(edited_task['priority'])

def test_edit_task_invalid_due_date(temp_csv_file, sample_tasks_fixture):
    task_id = sample_tasks_fixture['task1_id']
    with pytest.raises(ValueError, match="Invalid due_date format"):
        edit_task(task_id, due_date="invalid-date-format", filename=temp_csv_file)

def test_edit_task_invalid_priority(temp_csv_file, sample_tasks_fixture):
    task_id = sample_tasks_fixture['task1_id']
    with pytest.raises(ValueError, match="Invalid priority"):
        edit_task(task_id, priority="super-high", filename=temp_csv_file)

def test_edit_task_non_existent_id(temp_csv_file):
    add_task("Dummy task to ensure CSV is not empty", filename=temp_csv_file) # Ensure CSV not empty
    non_existent_id = str(uuid.uuid4())
    with pytest.raises(ValueError, match=f"Task with ID '{non_existent_id}' not found"):
        edit_task(non_existent_id, description="New desc", filename=temp_csv_file)

def test_edit_task_preserves_other_fields(temp_csv_file, sample_tasks_fixture):
    task_id = sample_tasks_fixture['task1_id']
    original_task = load_tasks(filename=temp_csv_file)[lambda df: df['task_id'] == task_id].iloc[0]
    new_description = "Only description updated"
    edit_task(task_id, description=new_description, filename=temp_csv_file)
    edited_task = load_tasks(filename=temp_csv_file)[lambda df: df['task_id'] == task_id].iloc[0]
    assert edited_task['description'] == new_description
    assert edited_task['status'] == original_task['status']
    assert edited_task['due_date'] == original_task['due_date']
    assert edited_task['priority'] == original_task['priority']
    assert edited_task['created_at'] == original_task['created_at']

# --- Tests for update_task_status ---

def test_update_task_status_valid(temp_csv_file, sample_tasks_fixture):
    task_id = sample_tasks_fixture['task2_id']
    original_task = load_tasks(filename=temp_csv_file)[lambda df: df['task_id'] == task_id].iloc[0]
    new_status = "completed"
    update_task_status(task_id, new_status, filename=temp_csv_file)
    updated_task = load_tasks(filename=temp_csv_file)[lambda df: df['task_id'] == task_id].iloc[0]
    assert updated_task['status'] == new_status
    assert updated_task['description'] == original_task['description']
    assert updated_task['due_date'] == original_task['due_date']
    assert updated_task['priority'] == original_task['priority']

def test_update_task_status_invalid_id(temp_csv_file):
    add_task("Dummy task to ensure CSV is not empty", filename=temp_csv_file) # Ensure CSV not empty
    non_existent_id = str(uuid.uuid4())
    with pytest.raises(ValueError, match=f"Task with ID '{non_existent_id}' not found"):
        update_task_status(non_existent_id, "completed", filename=temp_csv_file)

def test_update_task_status_invalid_status_value(temp_csv_file, sample_tasks_fixture):
    task_id = sample_tasks_fixture['task2_id']
    with pytest.raises(ValueError, match="Invalid status 'on_fire'"):
        update_task_status(task_id, "on_fire", filename=temp_csv_file)

# --- Tests for delete_task ---

def test_delete_task_existing(temp_csv_file, sample_tasks_fixture):
    task_to_delete_id = sample_tasks_fixture['task3_id']
    df_before = load_tasks(filename=temp_csv_file)
    assert task_to_delete_id in df_before['task_id'].values
    initial_task_count = len(df_before)
    delete_task(task_to_delete_id, filename=temp_csv_file)
    df_after = load_tasks(filename=temp_csv_file)
    assert task_to_delete_id not in df_after['task_id'].values
    assert len(df_after) == initial_task_count - 1

def test_delete_task_non_existent_id(temp_csv_file):
    add_task("Dummy task to ensure CSV is not empty", filename=temp_csv_file) # Ensure CSV not empty
    non_existent_id = str(uuid.uuid4())
    with pytest.raises(ValueError, match=f"Task with ID '{non_existent_id}' not found"):
        delete_task(non_existent_id, filename=temp_csv_file)

def test_delete_last_task(temp_csv_file):
    description = "The only task"
    add_task(description, filename=temp_csv_file)
    df_before = load_tasks(filename=temp_csv_file)
    assert len(df_before) == 1
    task_id = df_before.iloc[0]['task_id']
    delete_task(task_id, filename=temp_csv_file)
    df_after = load_tasks(filename=temp_csv_file)
    assert df_after.empty
    expected_columns = ['task_id', 'description', 'status', 'created_at', 'due_date', 'priority']
    assert list(df_after.columns) == expected_columns
    if os.path.exists(temp_csv_file):
        raw_df_after_delete = pd.read_csv(temp_csv_file)
        assert raw_df_after_delete.empty
        assert list(raw_df_after_delete.columns) == expected_columns
    else:
        pytest.fail("Test CSV file was deleted or not created with headers for empty tasks after last task deletion.")
