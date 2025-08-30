import os
import re
import base64
from typing import Dict, Any, Tuple, Optional

try:
    import yaml  # type: ignore
except Exception:  # pragma: no cover
    yaml = None  # will raise if used without installation


_FRONTMATTER_RE = re.compile(r"^---\s*\n(.*?)\n---\s*(?:\n|$)", re.DOTALL)
_CODE_BLOCK_RE = re.compile(r"```(?:python|py)\s*\n(.*?)```", re.IGNORECASE | re.DOTALL)
_BLOCK_TEX_RE = re.compile(r"\$\$(.*?)\$\$", re.DOTALL)
_IMG_RE = re.compile(r"!\[(.*?)\]\((.*?)\)")


_DEF_MIME = {
    ".png": "image/png",
    ".jpg": "image/jpeg",
    ".jpeg": "image/jpeg",
    ".gif": "image/gif",
    ".svg": "image/svg+xml",
}


def _is_url(s: str) -> bool:
    return bool(re.match(r"^(https?:)?//", s))


def _to_data_uri(path: str) -> Optional[str]:
    ext = os.path.splitext(path)[1].lower()
    mime = _DEF_MIME.get(ext, "application/octet-stream")
    try:
        with open(path, "rb") as f:
            data = f.read()
        b64 = base64.b64encode(data).decode("ascii")
        return f"data:{mime};base64,{b64}"
    except Exception:
        return None


def parse_markdown(md_text: str, base_dir: Optional[str] = None) -> Tuple[Dict[str, Any], Dict[str, Any]]:
    """
    Parse a Markdown text with optional YAML frontmatter and extract fields
    for DB insertion. Returns (meta, payload) where:
      - meta: raw metadata/frontmatter
      - payload: dict that maps to ContentCreate fields
    """
    meta: Dict[str, Any] = {}
    body = md_text

    # Extract YAML frontmatter at top
    m = _FRONTMATTER_RE.match(md_text)
    if m:
        fm_text = m.group(1)
        body = md_text[m.end():]
        if yaml is None:
            raise RuntimeError("PyYAML is required to parse frontmatter. Please install pyyaml.")
        try:
            loaded = yaml.safe_load(fm_text) or {}
            if not isinstance(loaded, dict):
                loaded = {}
            meta = {k: loaded[k] for k in loaded}
        except Exception as e:
            raise RuntimeError(f"Failed to parse YAML frontmatter: {e}")

    # Extract python code blocks (concatenate multiple blocks)
    code_blocks = _CODE_BLOCK_RE.findall(body)
    python_code = "\n\n".join(cb.strip() for cb in code_blocks if cb and cb.strip())

    # Extract LaTeX block formulas $$...$$
    formulas: Dict[str, Any] = {}
    blocks = _BLOCK_TEX_RE.findall(body)
    for i, tex in enumerate(blocks, start=1):
        key = f"formula_{i}"
        formulas[key] = str(tex).strip()

    # Merge frontmatter formulas if present (prefer named keys)
    if isinstance(meta.get("formulas"), dict):
        # If values are strings or objects; frontend accepts both.
        for k, v in meta["formulas"].items():
            if k not in formulas:
                formulas[k] = v

    # Extract images -> charts_data
    charts_data: Dict[str, Any] = {}
    for alt, url in _IMG_RE.findall(body):
        name = alt.strip() or os.path.basename(url).split(".")[0]
        if _is_url(url):
            charts_data[name] = url
        else:
            # resolve relative path
            p = url
            if base_dir and not os.path.isabs(p):
                p = os.path.join(base_dir, p)
            data_uri = _to_data_uri(p)
            if data_uri:
                charts_data[name] = data_uri

    # Build payload for DB
    module = str(meta.get("module", "")).strip()
    subcategory = str(meta.get("subcategory", "")).strip()
    title = str(meta.get("title", "")).strip()
    tags = meta.get("tags") if isinstance(meta.get("tags"), list) else None

    payload: Dict[str, Any] = {
        "module": module,
        "subcategory": subcategory,
        "title": title,
        "content_body": body.strip(),
        "python_code": python_code,
        "formulas": formulas or None,
        "charts_data": charts_data or None,
        "tags": tags,
    }

    # Basic validation
    missing = [k for k in ("module", "subcategory", "title") if not payload.get(k)]
    if missing:
        raise ValueError(f"Missing required fields in frontmatter: {', '.join(missing)}")

    return meta, payload