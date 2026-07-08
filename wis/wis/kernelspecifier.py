"""KernelSpecifier class used by WIS to handle the download ( to disk ) & load (to memory) of spice-kernels.

These will include both satellite-specific kernels, as well as those necessary for ground based observatories.
"""

# Third-party imports
# -----------------------------------------
import hashlib
import json
import logging
import os
import sys
import time
from datetime import datetime
from functools import cached_property
from typing import Any

import requests
import spiceypy as sp
from bs4 import BeautifulSoup
from pydantic import BaseModel, Field, PrivateAttr, model_validator

# Local imports
# -----------------------------------------
from wis.constants import Directories

logger = logging.getLogger(__name__)


class KernelSpecifier(BaseModel):
    """Holds the specification of where data is online for a given satellite / station-code.

    Also provides methods to download the data to local machine & to load the kernels
    into memory.
    """

    # Core identification attributes
    # -----------------------------------------
    obscodeMPC: str = Field(
        ...,
        description="MPC observatory code (e.g., 'C57' for TESS, '500' for geocenter, 'GROUND430' for DE430-based ground calculations)",
    )

    obscodeJPL: str = Field(
        ...,
        description="JPL/NAIF SPICE ID used in SPICE kernels (e.g., '-95' for TESS, '399' for Earth geocenter, 'GROUND430' for DE430)",
    )

    name: str = Field(
        ...,
        description="Human-readable name for logging and display (e.g., 'TESS', 'DE430', 'Kepler/K2')",
    )

    # Kernel file specification attributes
    # -----------------------------------------
    files: list[str] = Field(
        default=[],
        description="List of explicit URLs to download. Use for specific files like ephemeris .bsp files (e.g., 'https://.../de430.bsp')",
    )

    wildcards: dict[str, str] = Field(
        default={},
        description="Dictionary mapping URL directories to wildcard patterns for batch file discovery. Key: base URL, Value: wildcard pattern (e.g., {'https://.../pck/': 'earth_*_combined.bpc'})",
    )

    timecritical: list[str] = Field(
        default=[],
        description="List of URLs that require frequent refresh (checked every 24 hours). Use for time-sensitive files like earth_latest_high_prec.bpc that are updated frequently by JPL",
    )

    _kernel_filepath_map: dict[str, str] | None = PrivateAttr(default=None)

    @model_validator(mode="after")
    def validate_sources(self) -> "KernelSpecifier":
        """Validate that at least one file source is provided."""
        if not self.files and not self.wildcards:
            raise ValueError(
                f"KernelSpecifier '{self.name}' requires at least one file source: "
                "either 'files' or 'wildcards' must be non-empty"
            )
        return self

    def model_post_init(self, context: Any) -> None:  # noqa: ANN401
        """Initialize directories after validation passes."""
        directories = Directories()
        directories.obscode_data_subdir(self.obscodeJPL)

    @cached_property
    def _download_subdir(self) -> str:
        """Lazy property: returns the download subdirectory path."""
        return Directories().obscode_data_subdir(self.obscodeJPL)

    @property
    def _kernel_json(self) -> str:
        """Lazy property: returns the path to the kernel metadata JSON file."""
        return os.path.join(self._download_subdir, "kernel_filepath_map.json")

    @property
    def download_subdir(self) -> str:
        """Public accessor for download subdirectory."""
        return self._download_subdir

    @property
    def kernel_json(self) -> str:
        """Public accessor for kernel JSON path."""
        return self._kernel_json

    # ----------------------------------------------
    # Helper methods for metadata collection
    # ----------------------------------------------
    def _get_remote_file_metadata(self, url: str) -> dict:
        """Get metadata about a remote file using HTTP HEAD request."""
        metadata = {
            "remote_url": url,
            "discovery_date": datetime.now().isoformat(),
            "last_modified": None,
            "file_size": None,
        }

        try:
            response = requests.head(url, timeout=10)
            if response.status_code == 200:
                if "last-modified" in response.headers:
                    # The Last-Modified header is provided by JPL's web server but
                    # may not reliably indicate actual file content changes
                    metadata["last_modified"] = response.headers["last-modified"]
                if "content-length" in response.headers:
                    metadata["file_size"] = int(response.headers["content-length"])
        except requests.RequestException:
            # If HEAD request fails, we'll still have basic metadata
            pass

        return metadata

    def _calculate_file_hash(self, filepath: str) -> str | None:
        """Calculate MD5 hash of a local file."""
        try:
            with open(filepath, "rb") as f:
                file_hash = hashlib.md5()
                for chunk in iter(lambda: f.read(4096), b""):
                    file_hash.update(chunk)
                return file_hash.hexdigest()
        except OSError:
            return None

    def _format_file_size(self, size_bytes: int | None) -> str:
        """Format file size in human-readable format."""
        if size_bytes is None:
            return "unknown size"

        size_value = float(size_bytes)
        for unit in ["B", "KB", "MB", "GB"]:
            if size_value < 1024.0 or unit == "GB":
                if unit == "B":
                    return f"{int(size_value)}{unit}"
                else:
                    return f"{size_value:.1f}{unit}"
            size_value /= 1024.0
        return f"{size_value:.1f} GB"

    def _get_download_summary(self) -> dict:
        """Get summary of files to download with metadata."""
        files_to_download = self.kernels_that_need_to_be_downloaded()
        total_size = 0
        file_count = len(files_to_download)

        # Get metadata for all files
        kernel_metadata = self.get_kernel_metadata()

        for local_path in files_to_download:
            if local_path in kernel_metadata:
                file_size = kernel_metadata[local_path].get("file_size")
                if file_size:
                    total_size += file_size

        return {
            "file_count": file_count,
            "total_size": total_size,
            "files_to_download": files_to_download,
        }

    def _is_download_older_than(
        self,
        download_date: str | None,
        hours: int | None = None,
        days: int | None = None,
    ) -> bool:
        """Check if download is older than specified time period."""
        if not download_date:
            return True  # No download date means file needs updating

        try:
            download_time = datetime.fromisoformat(download_date).timestamp()
            current_time = time.time()

            if hours is not None:
                return (current_time - download_time) > (hours * 3600)
            elif days is not None:
                return (current_time - download_time) > (days * 24 * 3600)
            else:
                return False
        except (ValueError, TypeError):
            return True  # Invalid date format means file needs updating

    def _has_remote_file_changed(self, local_path: str, metadata: dict) -> bool:
        """Check if remote file has changed compared to local version."""
        remote_url = metadata.get("remote_url")
        if not remote_url:
            return False  # No URL to check

        # Get fresh metadata from remote
        fresh_metadata = self._get_remote_file_metadata(remote_url)

        # Method 1: File size changed (most reliable)
        # Compare local file size with fresh remote file size
        local_size = metadata.get("file_size")  # This is the local file size
        fresh_remote_size = fresh_metadata.get(
            "file_size"
        )  # This is the current remote size

        if local_size and fresh_remote_size and local_size != fresh_remote_size:
            return True

        # Method 2: Last modified changed (less reliable but useful)
        # Use original last_modified from discovery (never gets overwritten)
        original_last_modified = metadata.get("last_modified")
        fresh_last_modified = fresh_metadata.get("last_modified")

        return bool(
            original_last_modified
            and fresh_last_modified
            and original_last_modified != fresh_last_modified
        )

    # ----------------------------------------------
    # Property for lazy kernel filepath map initialization
    # ----------------------------------------------
    @property
    def kernel_filepath_map(self) -> dict[str, str]:
        """Lazy property: generate kernel filepath map on first access to avoid network calls on import."""
        if self._kernel_filepath_map is None:
            self._kernel_filepath_map = self.get_kernel_filepath_map()
        return self._kernel_filepath_map

    @kernel_filepath_map.setter
    def kernel_filepath_map(self, value: dict[str, str]) -> None:
        """Setter allows tests to inject mock kernel_filepath_map data."""
        self._kernel_filepath_map = value

    # ----------------------------------------------
    # Data directories / filepaths
    # ----------------------------------------------
    def generate_kernel_filepath_map(
        self,
    ) -> dict[str, dict]:
        """Create a dictionary of kernel filepaths with metadata.

        - maps the expected local filepaths (key) to metadata dicts (value).
        """
        kernel_filepath_map = {}

        # Process files from the .files list
        for url in self.files:
            local_path = os.path.join(self.download_subdir, url.split("/")[-1])
            kernel_filepath_map[local_path] = self._get_remote_file_metadata(url)

        # Process files from wildcards
        for url, wildcard in self.wildcards.items():
            for remote_url in self._listFD(url, wildcard=wildcard):
                local_path = os.path.join(
                    self.download_subdir, remote_url.split("/")[-1]
                )
                kernel_filepath_map[local_path] = self._get_remote_file_metadata(
                    remote_url
                )

        # Save the dictionary as a json file
        with open(self.kernel_json, "w") as f:
            json.dump(kernel_filepath_map, f)

        return kernel_filepath_map

    def get_kernel_filepath_map(
        self,
    ) -> dict[str, str]:
        """Load the dictionary of kernel filepaths mapping local paths to remote URLs."""
        # If the file does not exist, or the file is more than a week old, create a new one
        if (
            not os.path.exists(self.kernel_json)
            or (time.time() - os.path.getmtime(self.kernel_json)) > 7 * 24 * 3600
        ):
            self.generate_kernel_filepath_map()

        # Load the dictionary
        with open(self.kernel_json) as f:
            kernel_data = json.load(f)

        # Extract URLs from metadata format
        return {
            local_path: metadata["remote_url"]
            for local_path, metadata in kernel_data.items()
        }

    # ----------------------------------------------
    # Download methods
    # ----------------------------------------------
    def kernels_that_need_to_be_downloaded(
        self,
    ) -> dict[str, str]:
        """Check which kernels need downloading using metadata-based staleness detection."""
        files_to_download = {}
        kernel_metadata = self.get_kernel_metadata()

        for local_path, remote_url in self.kernel_filepath_map.items():
            file_metadata = kernel_metadata.get(local_path, {})

            # Case 1: File doesn't exist locally
            if not os.path.exists(local_path):
                files_to_download[local_path] = remote_url
                continue

            # Case 2: Time-critical files - use time-based refresh
            if remote_url in self.timecritical:
                download_date = file_metadata.get("download_date")
                if self._is_download_older_than(download_date, hours=24):
                    files_to_download[local_path] = remote_url
                continue

            # Case 3: Regular files - check if remote file has changed
            #  if self._has_remote_file_changed(local_path, file_metadata):
            #  files_to_download[local_path] = remote_url

        return files_to_download

    def download_data(
        self,
    ) -> None:
        """Download remote spice-files to the local machine and update metadata."""
        files_to_download = self.kernels_that_need_to_be_downloaded()

        if not files_to_download:
            logger.debug(f"{self.name}: all kernels already downloaded")
            return

        # Get download summary
        summary = self._get_download_summary()
        file_count = summary["file_count"]
        total_size = summary["total_size"]

        logger.info(
            f"{self.name}: downloading {file_count} file(s) "
            f"({self._format_file_size(total_size)} total)"
        )

        # Get metadata for progress display
        kernel_metadata = self.get_kernel_metadata()

        for i, (local, remote) in enumerate(files_to_download.items(), start=1):
            filename = os.path.basename(local)

            # Get file metadata for display
            file_metadata = kernel_metadata.get(local, {})
            file_size = file_metadata.get("file_size")
            last_modified = file_metadata.get("last_modified", "unknown date")

            logger.info(
                f"  [{i}/{file_count}] {filename} [{self._format_file_size(file_size)}]"
            )
            if last_modified and last_modified != "unknown date":
                logger.debug(f"    last modified: {last_modified}")

            try:
                logger.info(f"    downloading {filename} ...")
                self._download_file(remote, local)

                # Update metadata after successful download
                self._update_kernel_metadata(local)

                # Show completion info
                actual_size = os.path.getsize(local) if os.path.exists(local) else None
                if actual_size:
                    logger.debug(
                        f"    downloaded: {self._format_file_size(actual_size)}"
                    )
                logger.info("    OK")

            except Exception as e:
                logger.error(f"    FAILED: {e}")
                raise ValueError(f"Failed to download {remote}") from e

        logger.info(
            f"{self.name}: download complete - {file_count} file(s) "
            f"({self._format_file_size(total_size)})"
        )

    def _download_file(self, remote: str, local: str) -> None:
        """Download a remote kernel using requests (not wget, which had unreliable certificates handling)."""
        os.makedirs(os.path.dirname(local), exist_ok=True)

        # maybe overkill, but download to a partial file so we don't end up
        # with something corrupted if the download fails midway
        partial_path = f"{local}.part"

        try:
            with requests.get(remote, stream=True, timeout=(10, 60)) as response:
                response.raise_for_status()
                with open(partial_path, "wb") as f:
                    for chunk in response.iter_content(chunk_size=1024 * 1024):
                        if chunk:
                            f.write(chunk)

            os.replace(partial_path, local)
        except Exception:
            try:
                if os.path.exists(partial_path):
                    os.remove(partial_path)
            except OSError:
                pass
            raise

    def _update_kernel_metadata(self, local_path: str) -> None:
        """Update metadata for a downloaded kernel file."""
        # Load the current kernel data
        with open(self.kernel_json) as f:
            kernel_data = json.load(f)

        # Update metadata for this file
        if local_path in kernel_data:
            metadata = kernel_data[local_path]
            metadata["download_date"] = datetime.now().isoformat()
            metadata["md5_hash"] = self._calculate_file_hash(local_path)

            # Update file size from actual downloaded file
            try:
                metadata["file_size"] = os.path.getsize(local_path)
            except OSError:
                metadata["file_size"] = None

        # Save updated metadata
        with open(self.kernel_json, "w") as f:
            json.dump(kernel_data, f, indent=2)

    def _listFD(self, url: str, wildcard: str = "") -> list[str]:
        """List all the files in a url.

        Allows a wildcard of the form stem*end
        Stolen from
        https://stackoverflow.com/questions/11023530/python-to-list-http-files-and-directories.
        """
        # Split wildcard (if it contains "*")
        if wildcard.count("*") == 0:
            wildcardStart = wildcard
            wildcardEnd = ""
        elif wildcard.count("*") == 1:
            wildcardStart = wildcard[: wildcard.find("*")]
            wildcardEnd = wildcard[wildcard.find("*") + 1 :]
        else:
            sys.exit(
                f"Cannot parse wildcards with >=2 asterisks in them ... [{wildcard!r}]"
            )

        # Get page ...
        page = requests.get(url, timeout=30).text

        # Parse page
        soup = BeautifulSoup(page, "html.parser")

        # Return matching filenames
        url = url if url[-1] == "/" else url + "/"
        return [
            url + href
            for node in soup.find_all("a")
            if (href := node.get("href")) is not None
            and isinstance(href, str)
            and href.startswith(wildcardStart)
            and href.endswith(wildcardEnd)
        ]

    # ----------------------------------------------
    # Load method(s)
    # ----------------------------------------------
    def _loaded_kernels(self) -> list[str]:
        """Return the kernels that are currently loaded."""
        return [sp.kdata(n, "ALL")[0] for n in range(sp.ktotal("ALL"))]

    def load(self, download_if_needed: bool = True) -> None:
        """Load the kernels into memory."""
        # Ensure we have everything we need locally
        # (this is a no-op if everything is already downloaded)
        self.download_data()

        # Try to load the local kernel files
        # ...
        # So, apparently I need to be careful not to load things repeatedly
        # (despite the docs claiming this won't happen)
        # ...
        # There must be a nicer way to do this than what I have below,
        # but the spicypy functionalities seem to be straight C-wrappers,
        # so perhaps the functionality really doesn't exist ...
        # https://spiceypy.readthedocs.io/en/v1.1.1/documentation.html
        #
        # TODO: For the GROUND kernels, there is a specific order in which they should be loaded
        #       (predicts first, reconstructions later). I am NOT currently enforcing this order.
        #       Enforcing this is complicated because of the wildcards ...
        #
        try:
            # Get loaded kernels
            already_loaded = {_: True for _ in self._loaded_kernels()}
            # Kernels *NOT* already loaded
            not_already_loaded = [
                local
                for local in self.kernel_filepath_map
                if local not in already_loaded
            ]
            # Load the kernels
            if not_already_loaded:
                sp.furnsh(not_already_loaded)

        # If the local files don't exist, then download & attempt to load again
        except Exception as e:
            raise ValueError("Failed to load kernels") from e

    # ----------------------------------------------
    # Metadata access methods
    # ----------------------------------------------
    def get_kernel_metadata(self) -> dict:
        """Return metadata for all kernels in this specifier."""
        try:
            with open(self.kernel_json) as f:
                return json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            return {}

    def get_kernel_info(self) -> dict:
        """Return information about this kernel specifier."""
        return {
            "obscodeMPC": self.obscodeMPC,
            "obscodeJPL": self.obscodeJPL,
            "name": self.name,
            "file_count": len(self.files) + len(self.wildcards),
            "timecritical_count": len(self.timecritical),
        }
