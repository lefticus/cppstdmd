"""
Git repository management for C++ draft standard

Handles cloning, version switching, and metadata extraction from the
cplusplus/draft repository.
"""

import logging
import subprocess
from pathlib import Path

logger = logging.getLogger(__name__)


class RepoManagerError(Exception):
    """Exception raised for repository management errors"""

    pass


class DraftRepoManager:
    """Manages the C++ draft standard git repository"""

    REPO_URL = "https://github.com/cplusplus/draft.git"

    def __init__(self, repo_dir: Path | None = None):
        """
        Initialize repository manager

        Args:
            repo_dir: Path to the draft repository.
                     If None, uses ~/cplusplus-draft
        """
        if repo_dir is None:
            repo_dir = Path.home() / "cplusplus-draft"

        self.repo_dir = Path(repo_dir)
        self.source_dir = self.repo_dir / "source"

    def exists(self) -> bool:
        """Check if repository exists"""
        return self.repo_dir.exists() and (self.repo_dir / ".git").exists()

    def clone(self, shallow: bool = False) -> None:
        """
        Clone the C++ draft repository

        Args:
            shallow: If True, perform shallow clone (--depth=1) for faster download

        Raises:
            RepoManagerError: If clone fails
        """
        if self.exists():
            logger.info(f"Repository already exists at {self.repo_dir}")
            return

        logger.info(f"Cloning C++ draft repository to {self.repo_dir}...")

        cmd = ["git", "clone"]
        if shallow:
            cmd.extend(["--depth", "1"])
        cmd.extend([self.REPO_URL, str(self.repo_dir)])

        try:
            subprocess.run(cmd, check=True, capture_output=True, text=True)
            logger.info("Clone successful")
        except subprocess.CalledProcessError as e:
            raise RepoManagerError(f"Failed to clone repository:\n{e.stderr}") from e

    def checkout(self, ref: str) -> None:
        """
        Checkout a specific git ref (tag, branch, or SHA)

        Args:
            ref: Git reference to checkout

        Raises:
            RepoManagerError: If checkout fails
        """
        if not self.exists():
            raise RepoManagerError(
                f"Repository does not exist at {self.repo_dir}. Call clone() first."
            )

        logger.info(f"Checking out {ref}...")

        try:
            # Try to checkout the ref directly (works if ref exists locally)
            result = subprocess.run(
                ["git", "checkout", ref],
                cwd=self.repo_dir,
                capture_output=True,
                text=True,
            )

            if result.returncode == 0:
                logger.info(f"Checked out {ref}")
                return

            # If local checkout failed, try fetching and then checkout
            logger.debug(f"Local ref {ref} not found, attempting fetch...")
            try:
                subprocess.run(
                    ["git", "fetch", "--tags"],
                    cwd=self.repo_dir,
                    check=True,
                    capture_output=True,
                    text=True,
                    timeout=10,
                )

                # Try checkout again after fetch
                subprocess.run(
                    ["git", "checkout", ref],
                    cwd=self.repo_dir,
                    check=True,
                    capture_output=True,
                    text=True,
                )
                logger.info(f"Checked out {ref}")
            except (subprocess.CalledProcessError, subprocess.TimeoutExpired) as fetch_error:
                # Fetch failed (offline?), but original checkout also failed
                raise RepoManagerError(
                    f"Failed to checkout {ref}. Not found locally and fetch failed "
                    f"(offline?):\n{result.stderr}"
                ) from fetch_error

        except subprocess.CalledProcessError as e:
            raise RepoManagerError(f"Failed to checkout {ref}:\n{e.stderr}") from e

    def get_current_ref(self) -> dict[str, str]:
        """
        Get information about current git ref

        Returns:
            Dictionary with:
                - 'sha': Current commit SHA
                - 'ref': Current ref name (branch/tag) or 'detached'
                - 'short_sha': Short SHA (7 chars)

        Raises:
            RepoManagerError: If git commands fail
        """
        if not self.exists():
            raise RepoManagerError(f"Repository does not exist at {self.repo_dir}")

        try:
            # Get SHA
            result = subprocess.run(
                ["git", "rev-parse", "HEAD"],
                cwd=self.repo_dir,
                check=True,
                capture_output=True,
                text=True,
            )
            sha = result.stdout.strip()
            short_sha = sha[:7]

            # Get symbolic ref (branch/tag name)
            try:
                result = subprocess.run(
                    ["git", "symbolic-ref", "--short", "HEAD"],
                    cwd=self.repo_dir,
                    check=True,
                    capture_output=True,
                    text=True,
                )
                ref = result.stdout.strip()
            except subprocess.CalledProcessError:
                # Detached HEAD, try to get tag
                result = subprocess.run(
                    ["git", "describe", "--tags", "--exact-match"],
                    cwd=self.repo_dir,
                    capture_output=True,
                    text=True,
                )
                if result.returncode == 0:
                    ref = result.stdout.strip()
                else:
                    ref = "detached"

            return {
                "sha": sha,
                "ref": ref,
                "short_sha": short_sha,
            }

        except subprocess.CalledProcessError as e:
            raise RepoManagerError(f"Failed to get current ref:\n{e.stderr}") from e

    def get_tags(self, pattern: str | None = None) -> list[str]:
        """
        Get list of available tags

        Args:
            pattern: Optional glob pattern to filter tags (e.g., "n*" for all n-prefixed tags)

        Returns:
            List of tag names sorted alphabetically

        Raises:
            RepoManagerError: If git command fails
        """
        if not self.exists():
            raise RepoManagerError(f"Repository does not exist at {self.repo_dir}")

        try:
            # Try to fetch latest tags (optional, works offline if tags already exist)
            try:
                subprocess.run(
                    ["git", "fetch", "--tags"],
                    cwd=self.repo_dir,
                    check=True,
                    capture_output=True,
                    text=True,
                    timeout=10,
                )
                logger.debug("Fetched latest tags")
            except (subprocess.CalledProcessError, subprocess.TimeoutExpired):
                logger.debug("Fetch failed (offline?), using local tags")

            # List tags (works with whatever tags are available locally)
            cmd = ["git", "tag", "--list"]
            if pattern:
                cmd.append(pattern)

            result = subprocess.run(
                cmd,
                cwd=self.repo_dir,
                check=True,
                capture_output=True,
                text=True,
            )

            tags = [tag.strip() for tag in result.stdout.split("\n") if tag.strip()]
            return sorted(tags)

        except subprocess.CalledProcessError as e:
            raise RepoManagerError(f"Failed to get tags:\n{e.stderr}") from e

    def get_source_files(self, pattern: str = "*.tex") -> list[Path]:
        """
        Get list of source files in the repository

        Args:
            pattern: Glob pattern for files (default: *.tex)

        Returns:
            List of Path objects for matching files

        Raises:
            RepoManagerError: If source directory doesn't exist
        """
        if not self.source_dir.exists():
            raise RepoManagerError(f"Source directory not found: {self.source_dir}")

        return sorted(self.source_dir.glob(pattern))

    def ensure_ready(self, ref: str | None = None, shallow: bool = False) -> None:
        """
        Ensure repository is cloned and checked out to specified ref

        This is a convenience method that:
        1. Clones repo if it doesn't exist
        2. Checks out specified ref if provided

        Args:
            ref: Git reference to checkout (optional)
            shallow: Use shallow clone if cloning

        Raises:
            RepoManagerError: If any operation fails
        """
        if not self.exists():
            self.clone(shallow=shallow)

        if ref:
            self.checkout(ref)
