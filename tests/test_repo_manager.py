"""
Tests for repo_manager module

Tests the DraftRepoManager class that handles git operations for the
C++ draft standard repository.
"""

import tempfile
from pathlib import Path
from unittest.mock import Mock, patch, call
import subprocess
import pytest

from cpp_std_converter.repo_manager import DraftRepoManager, RepoManagerError


@pytest.fixture
def temp_dir():
    """Create a temporary directory for test repositories"""
    with tempfile.TemporaryDirectory() as tmpdir:
        yield Path(tmpdir)


@pytest.fixture
def mock_repo(temp_dir):
    """Create a mock repository structure"""
    repo_dir = temp_dir / "draft"
    repo_dir.mkdir()
    (repo_dir / ".git").mkdir()
    (repo_dir / "source").mkdir()
    return repo_dir


def test_initialization_default_path():
    """Test DraftRepoManager initialization with default path"""
    manager = DraftRepoManager()
    assert manager.repo_dir == Path.home() / "cplusplus-draft"
    assert manager.source_dir == Path.home() / "cplusplus-draft" / "source"


def test_initialization_custom_path(temp_dir):
    """Test DraftRepoManager initialization with custom path"""
    custom_path = temp_dir / "custom_draft"
    manager = DraftRepoManager(custom_path)
    assert manager.repo_dir == custom_path
    assert manager.source_dir == custom_path / "source"


def test_exists_true(mock_repo):
    """Test exists() returns True for existing repository"""
    manager = DraftRepoManager(mock_repo)
    assert manager.exists() is True


def test_exists_false_no_dir(temp_dir):
    """Test exists() returns False when directory doesn't exist"""
    manager = DraftRepoManager(temp_dir / "nonexistent")
    assert manager.exists() is False


def test_exists_false_no_git(temp_dir):
    """Test exists() returns False when .git directory is missing"""
    repo_dir = temp_dir / "no_git"
    repo_dir.mkdir()
    manager = DraftRepoManager(repo_dir)
    assert manager.exists() is False


@patch('subprocess.run')
def test_clone_success(mock_run, temp_dir):
    """Test successful repository cloning"""
    repo_dir = temp_dir / "new_repo"
    manager = DraftRepoManager(repo_dir)

    # Mock successful clone
    mock_run.return_value = Mock(returncode=0)

    manager.clone(shallow=False)

    # Verify git clone was called with correct arguments
    mock_run.assert_called_once()
    args = mock_run.call_args[0][0]
    assert args[0] == "git"
    assert args[1] == "clone"
    assert DraftRepoManager.REPO_URL in args
    assert str(repo_dir) in args
    assert "--depth" not in args


@patch('subprocess.run')
def test_clone_shallow(mock_run, temp_dir):
    """Test shallow clone"""
    repo_dir = temp_dir / "new_repo"
    manager = DraftRepoManager(repo_dir)

    mock_run.return_value = Mock(returncode=0)

    manager.clone(shallow=True)

    # Verify --depth=1 was added
    args = mock_run.call_args[0][0]
    assert "--depth" in args
    assert "1" in args


@patch('subprocess.run')
def test_clone_already_exists(mock_run, mock_repo):
    """Test that clone does nothing if repository already exists"""
    manager = DraftRepoManager(mock_repo)

    manager.clone()

    # git clone should not be called
    mock_run.assert_not_called()


@patch('subprocess.run')
def test_clone_failure(mock_run, temp_dir):
    """Test clone failure handling"""
    repo_dir = temp_dir / "new_repo"
    manager = DraftRepoManager(repo_dir)

    # Mock failed clone
    mock_run.side_effect = subprocess.CalledProcessError(
        1, "git clone", stderr="fatal: unable to access repository"
    )

    with pytest.raises(RepoManagerError) as exc_info:
        manager.clone()

    assert "Failed to clone repository" in str(exc_info.value)
    assert "fatal: unable to access repository" in str(exc_info.value)


@patch('subprocess.run')
def test_checkout_success(mock_run, mock_repo):
    """Test successful checkout"""
    manager = DraftRepoManager(mock_repo)

    # Mock successful fetch and checkout
    mock_run.return_value = Mock(returncode=0)

    manager.checkout("n4659")

    # Should call git fetch and git checkout
    assert mock_run.call_count == 2
    calls = mock_run.call_args_list

    # First call: git fetch --tags
    fetch_args = calls[0][0][0]
    assert "git" in fetch_args
    assert "fetch" in fetch_args
    assert "--tags" in fetch_args

    # Second call: git checkout n4659
    checkout_args = calls[1][0][0]
    assert "git" in checkout_args
    assert "checkout" in checkout_args
    assert "n4659" in checkout_args


@patch('subprocess.run')
def test_checkout_no_repository(mock_run, temp_dir):
    """Test checkout fails if repository doesn't exist"""
    manager = DraftRepoManager(temp_dir / "nonexistent")

    with pytest.raises(RepoManagerError) as exc_info:
        manager.checkout("n4659")

    assert "does not exist" in str(exc_info.value)
    mock_run.assert_not_called()


@patch('subprocess.run')
def test_checkout_failure(mock_run, mock_repo):
    """Test checkout failure handling"""
    manager = DraftRepoManager(mock_repo)

    # Mock successful fetch but failed checkout
    mock_run.side_effect = [
        Mock(returncode=0),  # fetch succeeds
        subprocess.CalledProcessError(1, "git checkout", stderr="error: pathspec 'invalid' did not match")
    ]

    with pytest.raises(RepoManagerError) as exc_info:
        manager.checkout("invalid")

    assert "Failed to checkout" in str(exc_info.value)
    assert "did not match" in str(exc_info.value)


@patch('subprocess.run')
def test_get_current_ref_on_branch(mock_run, mock_repo):
    """Test get_current_ref when on a branch"""
    manager = DraftRepoManager(mock_repo)

    # Mock git rev-parse and git symbolic-ref
    mock_run.side_effect = [
        Mock(stdout="abc123def456\n", returncode=0),  # rev-parse HEAD
        Mock(stdout="main\n", returncode=0),  # symbolic-ref --short HEAD
    ]

    result = manager.get_current_ref()

    assert result["sha"] == "abc123def456"
    assert result["ref"] == "main"
    assert result["short_sha"] == "abc123d"


@patch('subprocess.run')
def test_get_current_ref_on_tag(mock_run, mock_repo):
    """Test get_current_ref when on a tag (detached HEAD)"""
    manager = DraftRepoManager(mock_repo)

    # Mock git commands for detached HEAD on tag
    mock_run.side_effect = [
        Mock(stdout="abc123def456\n", returncode=0),  # rev-parse HEAD
        subprocess.CalledProcessError(1, "symbolic-ref"),  # symbolic-ref fails (detached)
        Mock(stdout="n4659\n", returncode=0),  # describe --tags --exact-match
    ]

    result = manager.get_current_ref()

    assert result["sha"] == "abc123def456"
    assert result["ref"] == "n4659"
    assert result["short_sha"] == "abc123d"


@patch('subprocess.run')
def test_get_current_ref_detached_no_tag(mock_run, mock_repo):
    """Test get_current_ref when detached HEAD with no tag"""
    manager = DraftRepoManager(mock_repo)

    # Mock git commands for detached HEAD without tag
    mock_run.side_effect = [
        Mock(stdout="abc123def456\n", returncode=0, stderr=None),  # rev-parse HEAD
        subprocess.CalledProcessError(1, "symbolic-ref", stderr=""),  # symbolic-ref fails
        Mock(stdout="", returncode=1, stderr=""),  # describe --tags fails (not exception)
    ]

    result = manager.get_current_ref()

    assert result["sha"] == "abc123def456"
    assert result["ref"] == "detached"
    assert result["short_sha"] == "abc123d"


@patch('subprocess.run')
def test_get_current_ref_no_repository(mock_run, temp_dir):
    """Test get_current_ref fails if repository doesn't exist"""
    manager = DraftRepoManager(temp_dir / "nonexistent")

    with pytest.raises(RepoManagerError) as exc_info:
        manager.get_current_ref()

    assert "does not exist" in str(exc_info.value)


@patch('subprocess.run')
def test_get_tags_no_pattern(mock_run, mock_repo):
    """Test getting all tags"""
    manager = DraftRepoManager(mock_repo)

    # Mock git fetch and git tag
    mock_run.side_effect = [
        Mock(returncode=0),  # git fetch --tags
        Mock(stdout="n4659\nn4861\nn5014\n", returncode=0),  # git tag --list
    ]

    tags = manager.get_tags()

    assert tags == ["n4659", "n4861", "n5014"]

    # Verify commands
    calls = mock_run.call_args_list
    assert "fetch" in str(calls[0])
    assert "tag" in str(calls[1])
    assert "--list" in str(calls[1])


@patch('subprocess.run')
def test_get_tags_with_pattern(mock_run, mock_repo):
    """Test getting tags with pattern filter"""
    manager = DraftRepoManager(mock_repo)

    mock_run.side_effect = [
        Mock(returncode=0),  # fetch
        Mock(stdout="n4659\nn4861\nn5014\n", returncode=0),  # tag --list n*
    ]

    tags = manager.get_tags(pattern="n*")

    assert tags == ["n4659", "n4861", "n5014"]

    # Verify pattern was passed
    tag_args = mock_run.call_args_list[1][0][0]
    assert "n*" in tag_args


@patch('subprocess.run')
def test_get_tags_empty_result(mock_run, mock_repo):
    """Test getting tags when there are no tags"""
    manager = DraftRepoManager(mock_repo)

    mock_run.side_effect = [
        Mock(returncode=0),  # fetch
        Mock(stdout="", returncode=0),  # no tags
    ]

    tags = manager.get_tags()

    assert tags == []


@patch('subprocess.run')
def test_get_tags_failure(mock_run, mock_repo):
    """Test get_tags failure handling"""
    manager = DraftRepoManager(mock_repo)

    mock_run.side_effect = subprocess.CalledProcessError(
        1, "git tag", stderr="fatal: not a git repository"
    )

    with pytest.raises(RepoManagerError) as exc_info:
        manager.get_tags()

    assert "Failed to get tags" in str(exc_info.value)


def test_get_source_files(mock_repo):
    """Test getting source files"""
    manager = DraftRepoManager(mock_repo)

    # Create some .tex files
    (manager.source_dir / "basic.tex").touch()
    (manager.source_dir / "expressions.tex").touch()
    (manager.source_dir / "statements.tex").touch()
    (manager.source_dir / "README.md").touch()  # not a .tex file

    files = manager.get_source_files()

    assert len(files) == 3
    assert all(f.suffix == ".tex" for f in files)
    assert any(f.name == "basic.tex" for f in files)


def test_get_source_files_custom_pattern(mock_repo):
    """Test getting source files with custom pattern"""
    manager = DraftRepoManager(mock_repo)

    # Create various files
    (manager.source_dir / "test.tex").touch()
    (manager.source_dir / "test.md").touch()
    (manager.source_dir / "test.cpp").touch()

    # Get only .md files
    files = manager.get_source_files(pattern="*.md")

    assert len(files) == 1
    assert files[0].name == "test.md"


def test_get_source_files_no_source_dir(temp_dir):
    """Test get_source_files fails if source directory doesn't exist"""
    manager = DraftRepoManager(temp_dir / "no_source")

    with pytest.raises(RepoManagerError) as exc_info:
        manager.get_source_files()

    assert "Source directory not found" in str(exc_info.value)


@patch('subprocess.run')
def test_ensure_ready_clone_and_checkout(mock_run, temp_dir):
    """Test ensure_ready clones and checks out ref"""
    repo_dir = temp_dir / "new_repo"
    manager = DraftRepoManager(repo_dir)

    # Create the repo structure after clone
    def side_effect_create_repo(*args, **kwargs):
        # First call is clone - create repo structure
        if "clone" in str(args):
            repo_dir.mkdir(parents=True, exist_ok=True)
            (repo_dir / ".git").mkdir(exist_ok=True)
            (repo_dir / "source").mkdir(exist_ok=True)
        return Mock(returncode=0, stdout="", stderr="")

    mock_run.side_effect = side_effect_create_repo

    manager.ensure_ready(ref="n4659", shallow=True)

    # Should have called git clone (shallow) and git checkout
    assert mock_run.call_count >= 2

    # Check clone was called
    clone_call = mock_run.call_args_list[0]
    assert "clone" in str(clone_call)
    assert "--depth" in str(clone_call)


@patch('subprocess.run')
def test_ensure_ready_only_checkout_if_exists(mock_run, mock_repo):
    """Test ensure_ready only checks out if repo already exists"""
    manager = DraftRepoManager(mock_repo)

    mock_run.return_value = Mock(returncode=0)

    manager.ensure_ready(ref="n4659")

    # Should only call git fetch and git checkout (not clone)
    assert mock_run.call_count == 2
    calls_str = str(mock_run.call_args_list)
    assert "clone" not in calls_str
    assert "fetch" in calls_str
    assert "checkout" in calls_str


@patch('subprocess.run')
def test_ensure_ready_no_ref(mock_run, temp_dir):
    """Test ensure_ready with no ref just clones"""
    repo_dir = temp_dir / "new_repo"
    manager = DraftRepoManager(repo_dir)

    mock_run.return_value = Mock(returncode=0)

    manager.ensure_ready()

    # Should only clone (no checkout)
    assert mock_run.call_count == 1
    assert "clone" in str(mock_run.call_args_list[0])


def test_repo_url_constant():
    """Test that REPO_URL is correctly defined"""
    assert DraftRepoManager.REPO_URL == "https://github.com/cplusplus/draft.git"


def test_repo_manager_error_is_exception():
    """Test that RepoManagerError can be raised and caught"""
    with pytest.raises(RepoManagerError):
        raise RepoManagerError("test error")

    try:
        raise RepoManagerError("test message")
    except RepoManagerError as e:
        assert "test message" in str(e)
