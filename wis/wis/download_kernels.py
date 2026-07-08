#!/usr/bin/env python3
"""Command-line tool to download WIS kernels.

Examples:
    # List available built-in kernels
    download-wis-kernels --list

    # Download specific built-in kernels
    download-wis-kernels DE430
    download-wis-kernels DE430 TESS

    # Download with custom kernels from a Python module
    download-wis-kernels --module mypackage.kernels DE430 MyCustomKernel

    # Mix built-in and custom
    download-wis-kernels --module my_kernels DE430 MyCustomKernel TESS
"""

import argparse
import importlib
import logging
import sys

from wis.kernel_instances_ground import DE430, DE440
from wis.kernel_instances_satellites import (
    GAIA,
    HST,
    JWST,
    KEPLER,
    TESS,
)
from wis.kernelspecifier import KernelSpecifier

logger = logging.getLogger(__name__)


def get_builtin_kernels() -> dict[str, KernelSpecifier]:
    """Return dictionary of built-in kernels."""
    return {
        "DE430": DE430,
        "DE440": DE440,
        "KEPLER": KEPLER,
        "TESS": TESS,
        "GAIA": GAIA,
        "HST": HST,
        "JWST": JWST,
    }


def load_custom_kernels(module_path: str) -> dict[str, KernelSpecifier]:
    """Load custom kernels from a Python module.

    The module should export KernelSpecifier instances as module-level variables.

    Args:
        module_path: Python module path (e.g., 'mypackage.kernels')

    Returns:
        Dictionary mapping kernel names to KernelSpecifier objects

    Example module (mypackage/kernels.py):
        from wis.kernelspecifier import KernelSpecifier

        MyCustomKernel = KernelSpecifier(
            obscodeMPC="C99",
            obscodeJPL="-999",
            name="MySatellite",
            files=["https://example.com/kernel.bsp"],
            wildcards={},
            timecritical=[]
        )
    """
    try:
        module = importlib.import_module(module_path)
    except ImportError as e:
        logger.error(f"Could not import module '{module_path}': {e}")
        sys.exit(1)

    custom_kernels = {}
    for name in dir(module):
        # Skip private attributes and imported modules
        if name.startswith("_"):
            continue

        obj = getattr(module, name)
        if isinstance(obj, KernelSpecifier):
            custom_kernels[name] = obj

    if not custom_kernels:
        logger.warning(f"No KernelSpecifier objects found in module '{module_path}'")

    return custom_kernels


def resolve_kernel_name(
    name: str, available_kernels: dict[str, KernelSpecifier]
) -> KernelSpecifier:
    """Resolve a kernel name to a KernelSpecifier object.

    Args:
        name: Kernel name (e.g., 'DE430', 'MyCustomKernel')
        available_kernels: Dictionary of available kernels

    Returns:
        KernelSpecifier object

    Raises:
        SystemExit: If kernel name is not found
    """
    if name not in available_kernels:
        available_names = list(available_kernels.keys())
        logger.error(f"Unknown kernel '{name}'. Available: {available_names}")
        sys.exit(1)

    return available_kernels[name]


def download(kernels: list[str], module: str | None = None) -> None:
    """Download specified kernels.

    Args:
        kernels: List of kernel names to download
        module: Optional Python module path containing custom kernels
    """
    # Start with built-in kernels
    available_kernels = get_builtin_kernels()

    # Load custom kernels if module specified
    if module:
        custom_kernels = load_custom_kernels(module)
        # Add custom kernels to available set
        available_kernels.update(custom_kernels)

    # Show header
    logger.info("WIS Kernel Download Tool")

    if not kernels:
        logger.info("\nUsage: download-wis-kernels [options] <kernel1> [kernel2] ...")
        logger.info("\nOptions:")
        logger.info("  --module, -m <module>  Load custom kernels from Python module")
        logger.info("  --list, -l             List available kernels and exit")
        logger.info("\nBuilt-in kernels:")
        for name in get_builtin_kernels():
            logger.info(f"  {name}")
        if module:
            custom_kernels = load_custom_kernels(module)
            if custom_kernels:
                logger.info("\nCustom kernels (from --module):")
                for name in custom_kernels:
                    logger.info(f"  {name}")
        logger.info("\nExamples:")
        logger.info("  download-wis-kernels DE430")
        logger.info("  download-wis-kernels DE430 TESS")
        logger.info(
            "  download-wis-kernels --module mypackage.kernels DE430 MyCustomKernel"
        )
        return

    # Show which kernels will be downloaded
    logger.info(f"\nDownloading {len(kernels)} kernel(s):")
    for name in kernels:
        if name in available_kernels:
            kernel = available_kernels[name]
            logger.info(f"  - {name} ({kernel.name})")
        else:
            logger.info(f"  - {name} (UNKNOWN - will error)")

    # Download each kernel
    downloaded = []
    failed = []

    for name in kernels:
        try:
            kernel = resolve_kernel_name(name, available_kernels)
            kernel.download_data()  # just download the data, don't load
            downloaded.append(name)
        except Exception as e:
            logger.error(f"Failed to download {name}: {e}")
            failed.append(name)

    # Summary
    logger.info("Download Summary")
    logger.info(f"Successfully downloaded: {len(downloaded)} kernel(s)")
    if downloaded:
        logger.info(f"  {', '.join(downloaded)}")
    if failed:
        logger.error(f"\nFailed: {len(failed)} kernel(s)")
        logger.error(f"  {', '.join(failed)}")

    if failed:
        sys.exit(1)


def main() -> None:
    """Entry point for CLI."""
    logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")

    parser = argparse.ArgumentParser(
        description="Download WIS (Where Is Satellite) SPICE kernels",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  download-wis-kernels --list
  download-wis-kernels DE430
  download-wis-kernels DE430 TESS
  download-wis-kernels --module mypackage.kernels DE430 MyCustomKernel
  download-wis-kernels -m my_kernels DE430 MyKernel1 MyKernel2 KEPLER
        """,
    )

    parser.add_argument(
        "kernels",
        nargs="*",
        help="Kernel names to download (e.g., DE430, TESS, MyCustomKernel)",
    )

    parser.add_argument(
        "--module",
        "-m",
        type=str,
        help="Python module path containing custom KernelSpecifier objects (e.g., 'mypackage.kernels')",
    )

    parser.add_argument(
        "--list",
        "-l",
        action="store_true",
        help="List available built-in kernels and exit",
    )

    args = parser.parse_args()

    # Handle --list flag
    if args.list:
        logger.info("Built-in WIS kernels:")
        for name, kernel in get_builtin_kernels().items():
            logger.info(f"  {name:<6} - {kernel.name}")
        logger.info("")
        if args.module:
            custom = load_custom_kernels(args.module)
            logger.info("Custom kernels from --module:")
            for name, kernel in custom.items():
                logger.info(f"  {name:<6} - {kernel.name}")
        return

    # Download kernels
    download(args.kernels, args.module)


if __name__ == "__main__":
    main()
