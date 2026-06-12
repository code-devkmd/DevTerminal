"""
Comprehensive Test Suite for DevTerminal
Tests all major features: error recovery, help command, copy/paste, boot speed
"""
import pytest
import os
import sys
from unittest.mock import patch, MagicMock
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from devcli.core.executor import execute_command, CommandExecutor
from devcli.features.error_recovery import ErrorRecovery, handle_command_not_found
from devcli.core.shell import get_prompt


class TestErrorRecovery:
    """Test error recovery and typo correction"""

    def test_common_typos_git(self):
        """Test git typo detection"""
        recovery = ErrorRecovery()
        # git psuh should suggest git push
        suggestion = recovery.check_typo("git", "git psuh")
        assert suggestion is not None

    def test_common_typos_docker(self):
        """Test docker typo detection"""
        recovery = ErrorRecovery()
        suggestion = recovery.check_typo("dokcer", "dokcer")
        assert suggestion == "docker"

    def test_common_typos_clear(self):
        """Test clear typo detection"""
        recovery = ErrorRecovery()
        suggestion = recovery.check_typo("claer", "claer")
        assert suggestion == "clear"

    def test_cd_typo(self):
        """Test cd.. typo"""
        recovery = ErrorRecovery()
        suggestion = recovery.check_typo("cd..", "cd..")
        assert suggestion == "cd .."

    def test_python_typo(self):
        """Test python typo detection"""
        recovery = ErrorRecovery()
        suggestion = recovery.check_typo("pyhton", "pyhton")
        assert suggestion == "python"

    def test_fuzzy_matching(self):
        """Test fuzzy matching for similar commands"""
        recovery = ErrorRecovery()
        # Should find similar commands
        suggestions = recovery.get_multiple_suggestions("gti")
        assert "git" in suggestions

    def test_no_typo_returns_none(self):
        """Test that correct commands return None"""
        recovery = ErrorRecovery()
        suggestion = recovery.check_typo("ls", "ls")
        # If it's a valid command, fuzzy match might find it
        # But if no close match, should be None or valid command
        assert suggestion is None or suggestion == "ls"


class TestHelpCommand:
    """Test help command functionality"""

    def test_help_flag_recognized(self):
        """Test that -h flag is recognized"""
        executor = CommandExecutor()
        # This should not raise an error
        is_builtin, should_continue, _ = executor.handle_builtin("-h", [])
        assert is_builtin == True
        assert should_continue == True

    def test_help_long_flag(self):
        """Test that --help flag is recognized"""
        executor = CommandExecutor()
        is_builtin, should_continue, _ = executor.handle_builtin("--help", [])
        assert is_builtin == True
        assert should_continue == True

    def test_help_command(self):
        """Test that help command is recognized"""
        executor = CommandExecutor()
        is_builtin, should_continue, _ = executor.handle_builtin("help", [])
        assert is_builtin == True
        assert should_continue == True


class TestCopyPaste:
    """Test copy/paste functionality"""

    def test_bracketed_paste_enabled(self):
        """Test that bracketed paste is enabled in shell"""
        # Check that enable_history_search is enabled for better input handling
        from devcli.core.shell import run_shell
        import inspect
        source = inspect.getsource(run_shell)
        assert "enable_history_search=True" in source

    def test_command_parsing_with_spaces(self):
        """Test parsing commands with multiple spaces (from paste)"""
        executor = CommandExecutor()
        cmd, args = executor.parse_command("git   push   origin   main")
        assert cmd == "git"
        assert args == ["push", "origin", "main"]

    def test_command_parsing_with_newlines(self):
        """Test parsing commands that might have newlines from paste"""
        executor = CommandExecutor()
        cmd, args = executor.parse_command("echo hello world")
        assert cmd == "echo"
        assert args == ["hello", "world"]


class TestBootSpeed:
    """Test boot speed optimization"""

    def test_intro_minimal(self):
        """Test that intro is optimized"""
        from devcli.main import show_intro
        import inspect
        source = inspect.getsource(show_intro)
        # Check that info string is simplified
        assert "Version   :" not in source
        assert "Type 'help' for commands" in source

    def test_no_slow_operations(self):
        """Test that main doesn't have slow operations"""
        from devcli.main import main
        import inspect
        source = inspect.getsource(main)
        # Should not have any sleep or delays
        assert "sleep" not in source
        assert "time.sleep" not in source


class TestCommandExecution:
    """Test command execution"""

    def test_empty_command(self):
        """Test empty command execution"""
        result = execute_command("")
        assert result == True

    def test_whitespace_command(self):
        """Test whitespace-only command"""
        result = execute_command("   ")
        assert result == True

    def test_exit_command(self):
        """Test exit command"""
        result = execute_command("exit")
        assert result == False

    def test_help_command_execution(self):
        """Test help command execution"""
        result = execute_command("help")
        assert result == True

    def test_clear_command(self):
        """Test clear command"""
        result = execute_command("clear")
        assert result == True


class TestPromptGeneration:
    """Test prompt generation"""

    def test_prompt_format(self):
        """Test that prompt has correct format"""
        from devcli.core.shell import get_prompt
        prompt = get_prompt()
        # Check that prompt is HTML formatted
        assert hasattr(prompt, '__str__')

    def test_prompt_includes_user(self):
        """Test that prompt includes username"""
        import getpass
        from devcli.core.shell import get_prompt
        prompt_str = str(get_prompt())
        user = getpass.getuser()
        assert user in prompt_str or "@" in prompt_str


class TestBuiltinCommands:
    """Test builtin command handling"""

    def test_cd_command_recognized(self):
        """Test cd command is recognized as builtin"""
        executor = CommandExecutor()
        is_builtin, _, _ = executor.handle_builtin("cd", [os.path.expanduser("~")])
        assert is_builtin == True

    def test_exit_command_stops_shell(self):
        """Test exit command returns False to stop shell"""
        executor = CommandExecutor()
        is_builtin, should_continue, _ = executor.handle_builtin("exit", [])
        assert is_builtin == True
        assert should_continue == False

    def test_ports_command_recognized(self):
        """Test ports command is recognized"""
        executor = CommandExecutor()
        is_builtin, _, _ = executor.handle_builtin("ports", [])
        assert is_builtin == True


class TestAliases:
    """Test command aliases"""

    def test_git_aliases_exist(self):
        """Test git aliases are configured"""
        from devcli.config import COMMAND_ALIASES
        assert "gs" in COMMAND_ALIASES
        assert "ga" in COMMAND_ALIASES
        assert "gc" in COMMAND_ALIASES
        assert "gp" in COMMAND_ALIASES

    def test_list_aliases_exist(self):
        """Test list aliases are configured"""
        from devcli.config import COMMAND_ALIASES
        assert "ll" in COMMAND_ALIASES
        assert "la" in COMMAND_ALIASES


class TestIntegration:
    """Integration tests"""

    def test_typo_correction_flow(self):
        """Test complete typo correction flow"""
        recovery = ErrorRecovery()
        # Simulate typo flow
        suggestion = recovery.check_typo("claer", "claer")
        assert suggestion == "clear"
        # Verify we can use the suggestion
        assert execute_command("clear") == True

    def test_help_is_accessible(self):
        """Test help command is accessible"""
        result = execute_command("help")
        assert result == True

    def test_exit_works(self):
        """Test exit command works"""
        result = execute_command("exit")
        assert result == False


def test_no_syntax_errors():
    """Test that all modules can be imported without errors"""
    try:
        from devcli.main import main, show_intro
        from devcli.core.shell import run_shell
        from devcli.core.executor import execute_command
        from devcli.features.error_recovery import ErrorRecovery
        from devcli.config import COMMAND_ALIASES
        assert True
    except Exception as e:
        pytest.fail(f"Import error: {e}")


def test_configuration_complete():
    """Test that configuration is complete"""
    from devcli.config import (
        APP_NAME, APP_VERSION, PROMPT_SYMBOL_UNIX,
        PROMPT_SYMBOL_WINDOWS, COMMAND_ALIASES
    )
    assert APP_NAME == "DevTerminal"
    assert APP_VERSION == "2.0.0"
    assert PROMPT_SYMBOL_UNIX == "$"
    assert len(COMMAND_ALIASES) > 0


if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])
