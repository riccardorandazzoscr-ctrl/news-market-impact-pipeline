"""Esclusione di date di una scheda dalla libreria (`_card_exclusions.yaml`): la scheda
resta intatta, ma le date elencate non diventano episodi da quella fonte."""
import contextlib
import io
from pathlib import Path
import sys
import tempfile
import unittest
from unittest.mock import patch

import yaml

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import analogues


def build(exclusions):
    with tempfile.TemporaryDirectory() as tmp:
        day = Path(tmp) / 'daily' / '2026-08-24'
        day.mkdir(parents=True)
        kb = Path(tmp) / 'kb'
        kb.mkdir()
        rows = {'news_01.md': ['| `2019-10-01` | neg | fiscal_deadlock | Bilancio italiano |',
                               '| `2022-09-23` | neg | fiscal_deadlock | Mini-budget Kwarteng |'],
                'news_02.md': ['| `2019-10-01` | neg | fiscal_deadlock | Altra scheda, stessa data |']}
        for name, lines in rows.items():
            (day / name).write_text('| `primary_theme` | fiscal_policy |\n\n' + '\n'.join(lines) + '\n')
        excl = kb / '_card_exclusions.yaml'
        excl.write_text(yaml.safe_dump(exclusions))
        lib = kb / '_episodes.yaml'
        with patch.object(analogues, 'DAILY_DIR', day.parent), \
                patch.object(analogues, 'KB_DIR', kb), \
                patch.object(analogues, 'LIB_PATH', lib), \
                patch.object(analogues, 'REVIEW_PATH', kb / '_direction_reviews.yaml'), \
                patch.object(analogues, 'CARD_EXCLUSIONS_PATH', excl), \
                contextlib.redirect_stdout(io.StringIO()):
            analogues.cmd_build()
        eps = yaml.safe_load(lib.read_text())['episodes']
    return {e['date']: {s for v in e['events'] for s in v['sources']} for e in eps}


class CardExclusionTests(unittest.TestCase):
    def test_excluded_date_leaves_only_that_card(self):
        src = build({'exclusions': [{'source': '2026-08-24/news_01.md',
                                     'dates': [{'date': '2019-10-01', 'reason': 'evento sbagliato'}]}]})
        self.assertEqual(src['2019-10-01'], {'card:2026-08-24/news_02.md'})
        self.assertEqual(src['2022-09-23'], {'card:2026-08-24/news_01.md'})

    def test_exclusion_without_reason_is_refused(self):
        with self.assertRaises(ValueError):
            build({'exclusions': [{'source': '2026-08-24/news_01.md', 'dates': [{'date': '2019-10-01'}]}]})

    def test_real_library_has_no_excluded_pair(self):
        excl = yaml.safe_load(analogues.CARD_EXCLUSIONS_PATH.read_text(encoding='utf-8'))
        lib = {}
        for e in analogues._load():
            lib.setdefault(e['date'], set()).update(s for v in e['events'] for s in v['sources'])
        for row in excl['exclusions']:
            for d in row['dates']:
                self.assertNotIn(f"card:{row['source']}", lib.get(d['date'], set()), d['date'])


if __name__ == '__main__':
    unittest.main()
