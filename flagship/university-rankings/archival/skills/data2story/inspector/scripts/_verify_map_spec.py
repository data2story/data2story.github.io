"""Shared spec: the per-kind required keys for a verify_map.json entry.

Single source of truth for BOTH the Stage-6 validator
(inspector/scripts/validate.py) and the Stage-7 viewer emitter
(inspector/scripts/generate_viewer.py). The dict was previously hand-copied into
each script with a "keep in LOCK-STEP" comment; importing it from here removes the
drift risk (a change to the required keys is made once, here).

It is a schema-lite mirror of verify_map.schema.json $defs. The five kinds are
complete (computation|media|generated|fact|credits); a decorative gradient/scrim
carries no data-* token and so has no verify_map entry (a credited generated
background uses kind:"generated").
"""

VERIFY_MAP_REQUIRED = {
    'computation': ('kind', 'title', 'claim', 'cell_id', 'code_file', 'code', 'run'),
    'media': ('kind', 'title', 'media_type', 'preview', 'source_url', 'license',
              'author', 'identity'),
    'generated': ('kind', 'title', 'media_type', 'preview', 'tool', 'model',
                  'prompt', 'purpose', 'disclosure', 'role'),
    'fact': ('kind', 'title', 'claim', 'category', 'sources'),
    'credits': ('kind', 'title', 'claim', 'category', 'sources'),
}
