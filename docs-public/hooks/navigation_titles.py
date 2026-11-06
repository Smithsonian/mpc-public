"""Rename selected sections while keeping MkDocs' automatic navigation."""

SECTION_TITLES = {
    "mpc-ops-docs/index.md": "Operations",
    "mpc-ops-docs/apis/index.md": "APIs",
}


def on_nav(nav, **kwargs):
    for item in nav:
        if item.is_section:
            for child in item.children:
                if child.is_page and child.file.src_uri in SECTION_TITLES:
                    item.title = SECTION_TITLES[child.file.src_uri]
            on_nav(item.children)
    return nav
