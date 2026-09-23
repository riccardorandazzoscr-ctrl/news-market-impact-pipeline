"""R02: la data non identifica l'evento. Un AND e un verso vanno soddisfatti da un
solo evento (data × tema × geografia), mai dall'unione di fonti su paesi diversi."""
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

CARDS = {
    # Tankan e ISM lo stesso giorno: due eventi, due paesi.
    'news_01.md': ('macro_data', '', '| `2024-04-01` | neutral | japan_release, tankan, activity_growth | Tankan: fiducia delle grandi manifatturiere |'),
    'news_02.md': ('macro_data', '^GSPC', '| `2024-04-01` | pos | ism, activity_growth | ISM manifatturiero USA sopra 50 |'),
    # Stesso evento BoJ da due schede, ciascuna con metà delle etichette.
    'news_03.md': ('monetary_policy', '', '| `2016-01-29` | neg | rate_decision | La BoJ adotta tassi negativi |'),
    'news_04.md': ('monetary_policy', '', '| `2016-01-29` | neg | yen | Yen: la BoJ sorprende |'),
    # Evento Fed nella stessa data: non si fonde con la BoJ.
    'news_05.md': ('monetary_policy', '', '| `2016-01-29` | neg | hawkish | Fed: verbali restrittivi |'),
}


class EventTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        with tempfile.TemporaryDirectory() as tmp:
            day = Path(tmp) / 'daily' / '2026-09-23'
            day.mkdir(parents=True)
            kb = Path(tmp) / 'kb'
            kb.mkdir()
            for name, (theme, ref, row) in CARDS.items():
                (day / name).write_text(f'| `primary_theme` | {theme} |\n'
                                        f'| `direction_reference` | {ref} |\n\n{row}\n')
            lib = kb / '_episodes.yaml'
            with patch.object(analogues, 'DAILY_DIR', day.parent), \
                    patch.object(analogues, 'KB_DIR', kb), \
                    patch.object(analogues, 'LIB_PATH', lib), \
                    patch.object(analogues, 'REVIEW_PATH', kb / '_direction_reviews.yaml'), \
                    contextlib.redirect_stdout(io.StringIO()):
                analogues.cmd_build()
            cls.eps = yaml.safe_load(lib.read_text())['episodes']

    def find(self, theme, tokens, direction=None, reference=None, eps=None):
        out = io.StringIO()
        with patch.object(analogues, '_load', return_value=eps or self.eps), \
                contextlib.redirect_stdout(out), contextlib.redirect_stderr(io.StringIO()):
            analogues.cmd_find(theme, direction, None, tokens, 0, 0, True, reference)
        return set(filter(None, out.getvalue().strip().split(',')))

    def test_events_split_by_geography(self):
        ev = {e['theme']: [v['event_id'] for v in e['events']] for e in self.eps}
        self.assertEqual(ev['macro_data'], ['2024-04-01:macro_data:-',
                                            '2024-04-01:macro_data:japan_release'])
        self.assertEqual(ev['monetary_policy'], ['2016-01-29:monetary_policy:-',
                                                 '2016-01-29:monetary_policy:japan_release'])

    def test_tankan_is_not_an_american_ism(self):
        self.assertEqual(self.find('macro_data', ['japan_release', 'ism']), set())
        self.assertEqual(self.find('macro_data', ['japan_release', 'tankan']), {'2024-04-01'})

    def test_same_event_from_two_sources_still_matches(self):
        self.assertEqual(self.find('monetary_policy', ['rate_decision', 'yen']), {'2016-01-29'})
        self.assertEqual(self.find('monetary_policy', ['hawkish', 'yen']), set())

    def test_sign_must_come_from_a_selected_event(self):
        self.assertEqual(self.find('macro_data', ['ism'], 'pos', '^GSPC'), {'2024-04-01'})
        self.assertEqual(self.find('macro_data', ['tankan'], 'pos', '^GSPC'), set())

    def test_real_library_2024_04_01(self):
        real = analogues._load()
        self.assertNotIn('2024-04-01', self.find('macro_data', ['japan_release', 'ism'], eps=real))
        self.assertIn('2024-04-01', self.find('macro_data', ['japan_release', 'tankan'], eps=real))


if __name__ == '__main__':
    unittest.main()
