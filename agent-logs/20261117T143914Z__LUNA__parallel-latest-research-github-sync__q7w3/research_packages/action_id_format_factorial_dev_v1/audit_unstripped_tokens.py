#!/usr/bin/env python3
"""Optional local-tokenizer check of raw output whitespace; no model/GPU call."""
import collections
import json
import re
import sys
from pathlib import Path


def main(journal, tokenizer_directory):
    from transformers import AutoTokenizer
    tokenizer = AutoTokenizer.from_pretrained(tokenizer_directory, local_files_only=True, trust_remote_code=False)
    events = [json.loads(line) for line in Path(journal).read_text().splitlines()]
    eos = set(next(event for event in events if event.get('event') == 'loading_complete')['eos_ids'])
    counts = collections.Counter(total=0, whitespace_changed=0, unstripped_bare_shape=0, unstripped_bracket_shape=0)
    for event in events:
        if event.get('event') != 'raw_result':
            continue
        tokens = event['output_token_ids']
        if not tokens or tokens[-1] not in eos or any(token in eos for token in tokens[:-1]):
            raise ValueError('unexpected or missing terminal EOS')
        raw = tokenizer.decode(tokens[:-1], skip_special_tokens=True, clean_up_tokenization_spaces=False)
        counts['total'] += 1
        counts['whitespace_changed'] += int(raw != raw.strip())
        counts['unstripped_bare_shape'] += int(bool(re.fullmatch(r'A[0-9]{3}', raw)))
        counts['unstripped_bracket_shape'] += int(bool(re.fullmatch(r'\[A[0-9]{3}\]', raw)))
    return dict(counts)


if __name__ == '__main__':
    if len(sys.argv) != 3:
        raise SystemExit('usage: audit_unstripped_tokens.py JOURNAL LOCAL_TOKENIZER_DIRECTORY')
    print(json.dumps(main(sys.argv[1], sys.argv[2]), ensure_ascii=False, indent=2, sort_keys=True))
