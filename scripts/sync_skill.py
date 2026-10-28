#!/usr/bin/env python3
"""Generate installed references from canonical source documents; verify drift."""
import argparse
import hashlib
import json
from pathlib import Path
import posixpath
import re
from urllib.parse import urlsplit
ROOT = Path(__file__).resolve().parents[1]
SKILL = ROOT / 'skills/build-with-torque'
MIRRORS = {'docs/AI_SETUP_PROMPT.md': 'references/AI_SETUP_PROMPT.md', 'docs/BUNDLE_AUTHORING.md': 'references/BUNDLE_AUTHORING.md', 'REGISTRY.md': 'references/REGISTRY.md'}
SOURCE_REPO = 'torque'
SOURCE_COMMIT = '5c2cadfdb698170374fa3c6c78291ac1842a99e6'

def generated():
    outputs = {}; records = []
    for source, dest in MIRRORS.items():
        path = ROOT / source; raw = path.read_bytes(); output = raw
        if path.suffix == ".md":
            def fix(match):
                ref = match[2]; uri = urlsplit(ref)
                if uri.scheme or uri.netloc or not uri.path: return match[0]
                key = posixpath.normpath(posixpath.join(posixpath.dirname(source), uri.path))
                if key in MIRRORS:
                    target = posixpath.relpath(MIRRORS[key], posixpath.dirname(dest))
                else:
                    target = "https://github.com/michaeljabbour/" + SOURCE_REPO + "/blob/" + SOURCE_COMMIT + "/" + key
                return "[" + match[1] + "](" + target + (("#" + uri.fragment) if uri.fragment else "") + ")"
            output = re.sub(r"(?<!!)\[([^\]]+)\]\(([^)\s]+)\)", fix, raw.decode()).encode()
        outputs[SKILL / dest] = output
        records.append({"source": source, "destination": dest, "source_sha256": hashlib.sha256(raw).hexdigest(), "output_sha256": hashlib.sha256(output).hexdigest()})
    outputs[SKILL / "reference-sources.json"] = (json.dumps(records, indent=2) + "\n").encode()
    return outputs

def main():
    parser=argparse.ArgumentParser(description=__doc__);parser.add_argument("--check", action="store_true");args=parser.parse_args()
    for path, content in generated().items():
        if args.check:
            if not path.is_file() or path.read_bytes()!=content:raise SystemExit("Reference drift: " + str(path.relative_to(ROOT)))
        else:path.parent.mkdir(parents=True,exist_ok=True);path.write_bytes(content)
    print("reference mirrors verified" if args.check else "reference mirrors generated")
if __name__=="__main__":main()
