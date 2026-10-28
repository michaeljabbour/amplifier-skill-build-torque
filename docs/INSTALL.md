# Install the method

Use `python3 scripts/capability.py doctor`, then `python3 scripts/capability.py install --dest <skills-parent>`. Keep the complete installed folder and license. Identical reinstall is idempotent; conflicts are refused unless you deliberately choose `--replace`, which retains a dated backup. Remove only that folder to uninstall. No native runtime, server, provider, or service is required to read and apply the method.

## Optional native work

The original Torque installers and package guide remain in the repository. They clone/install framework packages and can change a user installation; they are separate from the portable installer and were not run here. Use the actual host CLI/contracts and isolated data for application checks. The skill does not retire or merge the kernel, CLI, services, extensions, or domain bundles.
