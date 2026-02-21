import os
import sys
import logging

logger = logging.getLogger(__name__)

# The shutil.disk_usage is available since Python 3.3,
# but in other versions, we need to use psutil.disk_usage to replace it.
# (For Synology's compatibility; there is no psutil in Python 3 in Synology)
SUPPORT_SHUTIL = sys.version_info >= (3, 3, 0)

def _resolve_path(path):
    """Resolve the path to an absolute, real path and verify it exists."""
    resolved = os.path.realpath(os.path.expanduser(path))
    if not os.path.exists(resolved):
        raise OSError("Path does not exist: %s (resolved to: %s)" % (path, resolved))
    return resolved

def disk_usage_(path):
    resolved_path = _resolve_path(path)

    if resolved_path != path:
        logger.debug("Resolved path '%s' to '%s'" % (path, resolved_path))

    du = None

    if SUPPORT_SHUTIL:
        import shutil
        du = shutil.disk_usage(resolved_path)
    else:
        import psutil
        du = psutil.disk_usage(resolved_path)

    # On macOS with APFS, statvfs may underreport free space because it
    # excludes "purgeable" space. Log a warning so users know to check.
    if sys.platform == 'darwin' and du.free == 0:
        logger.warning(
            "Reported free space is 0 for '%s'. "
            "If this is an APFS volume, macOS may not be reporting purgeable space. "
            "Verify with: diskutil info '%s'" % (resolved_path, resolved_path)
        )

    return {
        'total': du.total,
        'used': du.used,
        'free': du.free,
    }
