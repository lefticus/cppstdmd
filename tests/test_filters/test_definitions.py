"""Tests for cpp-definitions.lua filter"""
import subprocess
from pathlib import Path
import sys

# Import inject_macros helper from conftest
sys.path.insert(0, str(Path(__file__).parent.parent))
from conftest import inject_macros
import pytest

FILTER_PATH = Path("src/cpp_std_converter/filters/cpp-definitions.lua")

def run_pandoc_with_filter(latex_content):
    """Helper to run Pandoc with definitions filter"""
    # Inject simplified_macros.tex preprocessing
    latex_with_macros = inject_macros(latex_content)

    cmd = [
        "pandoc",
        "--from=latex+raw_tex",
        "--to=gfm",
        f"--lua-filter={FILTER_PATH}",
    ]
    result = subprocess.run(
        cmd,
        input=latex_with_macros,
        capture_output=True,
        text=True,
    )
    return result.stdout, result.returncode

def test_basic_definition():
    """Test basic definition with term and label"""
    latex = r"""\definition{access}{defns.access}
read or modify the value of an object"""
    output, code = run_pandoc_with_filter(latex)
    assert code == 0
    assert "#### 1 access" in output
    assert '<a id="defns.access">[defns.access]</a>' in output
    assert "read or modify the value of an object" in output

def test_definition_with_context():
    """Test definition with context label"""
    latex = r"""\definition{access}{defns.access}
\defncontext{execution-time action}
read or modify the value of an object"""
    output, code = run_pandoc_with_filter(latex)
    assert code == 0
    assert "#### 1 access" in output
    assert "⟨execution-time action⟩" in output
    assert "read or modify the value of an object" in output

def test_definition_with_note():
    """Test definition with defnote"""
    latex = r"""\definition{access}{defns.access}
\defncontext{execution-time action}
read or modify the value of an object

\begin{defnote}
Only read and write operations on scalar types are atomic.
\end{defnote}"""
    output, code = run_pandoc_with_filter(latex)
    assert code == 0
    assert "#### 1 access" in output
    assert "Note 1 to entry" in output
    assert "end note" in output
    assert "Only read and write operations" in output

def test_multiline_definition():
    """Test definition split across multiple lines (term on one line, label on next)"""
    latex = r"""\definition{implementation-defined strict total order over pointers}
{defns.order.ptr}
\defncontext{library}
strict total ordering over all pointer values"""
    output, code = run_pandoc_with_filter(latex)
    assert code == 0
    assert "#### 1 implementation-defined strict total order over pointers" in output
    assert '<a id="defns.order.ptr">[defns.order.ptr]</a>' in output
    assert "⟨library⟩" in output
    assert "strict total ordering" in output

def test_definition_as_rawblock():
    """Test definition appearing as RawBlock before Para"""
    latex = r"""\definition{arbitrary-positional stream}{defns.arbitrary.stream}

\defncontext{library}
stream that can seek to any integral position"""
    output, code = run_pandoc_with_filter(latex)
    assert code == 0
    assert "#### 1 arbitrary-positional stream" in output
    assert '<a id="defns.arbitrary.stream">[defns.arbitrary.stream]</a>' in output
    assert "⟨library⟩" in output

def test_definition_counter():
    """Test that definition counter increments correctly"""
    latex = r"""\definition{first}{defns.first}
First definition

\definition{second}{defns.second}
Second definition

\definition{third}{defns.third}
Third definition"""
    output, code = run_pandoc_with_filter(latex)
    assert code == 0
    assert "#### 1 first" in output
    assert "#### 2 second" in output
    assert "#### 3 third" in output

def test_note_counter_reset():
    """Test that note counter resets for each definition"""
    latex = r"""\definition{first}{defns.first}
First definition

\begin{defnote}
First note
\end{defnote}

\begin{defnote}
Second note
\end{defnote}

\definition{second}{defns.second}
Second definition

\begin{defnote}
Third note (should be Note 1 again)
\end{defnote}"""
    output, code = run_pandoc_with_filter(latex)
    assert code == 0
    # First definition should have Note 1 and Note 2
    lines = output.split('\n')
    notes = [line for line in lines if 'Note' in line and 'to entry' in line]
    assert len(notes) == 3
    # Check that note counter resets
    assert "Note 1 to entry" in output
    assert "Note 2 to entry" in output

@pytest.fixture(scope="module")
def draft_repo_n4950():
    """Fixture to ensure draft repository exists and is on n4950 (C++23)"""
    from cpp_std_converter.repo_manager import DraftRepoManager

    repo_manager = DraftRepoManager()

    # Ensure repo exists
    if not repo_manager.exists():
        try:
            repo_manager.clone(shallow=False)
        except Exception as e:
            pytest.skip(f"Could not clone draft repository: {e}")

    # Checkout n4950 (C++23) for consistent test state
    try:
        repo_manager.checkout("n4950")
    except Exception as e:
        pytest.skip(f"Could not checkout n4950: {e}")

    return repo_manager


def test_intro_defs_full_conversion(draft_repo_n4950):
    """Test conversion of full intro.defs section"""
    intro_tex = draft_repo_n4950.source_dir / "intro.tex"
    if not intro_tex.exists():
        pytest.skip(f"intro.tex not found at {intro_tex}")

    cmd = [
        "pandoc",
        str(intro_tex),
        "--from=latex+raw_tex",
        "--to=gfm",
        f"--lua-filter={FILTER_PATH}",
    ]
    result = subprocess.run(cmd, capture_output=True, text=True)
    assert result.returncode == 0

    # n4950 (C++23) has 68 definitions
    import re
    definition_count = len(re.findall(r'^#### \d+\s+\w', result.stdout, re.MULTILINE))
    assert definition_count == 68, f"Expected 68 definitions in n4950, got {definition_count}"

    # Check specific definitions
    assert "#### 1 access" in result.stdout
    assert "#### 27 implementation-defined strict total order over pointers" in result.stdout
    assert "#### 68 well-formed program" in result.stdout

    # Check context labels appear
    assert "⟨execution-time action⟩" in result.stdout
    assert "⟨library⟩" in result.stdout
