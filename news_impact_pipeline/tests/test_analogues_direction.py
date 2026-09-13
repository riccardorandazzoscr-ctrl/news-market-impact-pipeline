"""Direction must be scoped to an asset; legacy and conflicts fail closed."""
import contextlib
import io
from pathlib import Path
import sys
import unittest
import tempfile
import yaml
from unittest.mock import patch
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import analogues

class DirectionTests(unittest.TestCase):
    def run_find(self, episodes, direction='pos', reference=None, theme='commodity_energy'):
        out, err = io.StringIO(), io.StringIO()
        with patch.object(analogues, '_load', return_value=episodes), contextlib.redirect_stdout(out), contextlib.redirect_stderr(err):
            kwargs = {} if reference is None else {'direction_reference': reference}
            analogues.cmd_find(theme, direction, None, None, 12, 0, **kwargs)
        return set(filter(None, out.getvalue().strip().split(','))), err.getvalue()

    def episode(self, day, scoped=None):
        return {'date': day, 'theme': 'commodity_energy', 'direction': 'mixed',
                'directions': ['pos', 'neg'], 'directions_local': ['pos', 'neg'],
                'directions_declared': ['pos', 'neg'],
                'directions_by_reference': scoped or {}}

    def test_legacy_never_claims_strong_or_returns_ambiguous_dates(self):
        dates, note = self.run_find([self.episode('2015-07-14')])
        self.assertEqual(dates, set())
        self.assertIn('--direction-reference', note)
        self.assertNotIn('filtro forte', note)

    def test_reference_conflicts_and_small_pool(self):
        eps = [self.episode('2019-05-12', {'BZ=F': ['pos'], 'IYT': ['neg']}),
               self.episode('2015-07-14', {'BZ=F': ['neg']}),
               self.episode('2025-01-15', {'BZ=F': ['pos', 'neg']}),
               self.episode('2016-01-19')]
        self.assertEqual(self.run_find(eps, reference='BZ=F')[0], {'2019-05-12'})
        self.assertEqual(self.run_find(eps, direction='neg', reference='BZ=F')[0], {'2015-07-14'})
        self.assertEqual(self.run_find(eps, direction='neg', reference='IYT')[0], {'2019-05-12'})
        self.assertEqual(self.run_find(eps, reference='UNKNOWN')[0], set())

    def test_review_veto_excludes_an_existing_card_declaration(self):
        episode = self.episode('2025-01-15', {'BZ=F': ['neg']})
        episode['direction_review_excluded'] = {'BZ=F': 'eventi opposti nella stessa data'}
        dates, note = self.run_find([episode], direction='neg', reference='BZ=F')
        self.assertEqual(dates, set())
        self.assertIn('revisione', note)

    def test_build_applies_reviewed_sign_and_veto(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            daily, kb = root / 'daily', root / 'kb'
            day = daily / '2026-09-13'
            day.mkdir(parents=True)
            kb.mkdir()
            (day / 'news_01.md').write_text('''| 2018-05-08 | neg | sanctions | Ritiro dal JCPOA; offerta iraniana attesa in calo. |
| 2025-01-15 | neg | de_escalation | Cessate il fuoco. |
''')
            review = kb / '_direction_reviews.yaml'
            review.write_text('''reviews:
  - date: '2018-05-08'
    theme: commodity_energy
    reference: BZ=F
    direction: pos
    source: 2026-09-13/news_01.md
    reason: Sanzioni sull'offerta attesa.
  - date: '2025-01-15'
    theme: commodity_energy
    reference: BZ=F
    status: excluded
    source: 2026-09-13/news_01.md
    reason: Eventi opposti nella stessa data.
''')
            def harvest(_):
                return 'commodity_energy', 'bullish', [], ['2018-05-08', '2025-01-15'], (day / 'news_01.md').read_text()
            lib = kb / '_episodes.yaml'
            with patch.object(analogues, 'DAILY_DIR', daily), patch.object(analogues, 'KB_DIR', kb), patch.object(analogues, 'LIB_PATH', lib), patch.object(analogues, 'REVIEW_PATH', review), patch.object(analogues, 'harvest_card', side_effect=harvest), contextlib.redirect_stdout(io.StringIO()):
                analogues.cmd_build()
            eps = {e['date']: e for e in yaml.safe_load(lib.read_text())['episodes']}
            self.assertEqual(eps['2018-05-08']['directions_by_reference']['BZ=F'], ['pos'])
            self.assertIn('BZ=F', eps['2025-01-15']['direction_review_excluded'])
            self.assertIn('card:2026-09-13/news_01.md', eps['2018-05-08']['direction_sources']['BZ=F'])

    def test_reviewed_real_pools_do_not_reintroduce_doubtful_dates(self):
        episodes = analogues._load()
        for sign in ('pos', 'neg'):
            dates, _ = self.run_find(episodes, direction=sign, reference='BZ=F')
            self.assertFalse(dates & {'2016-01-19', '2020-01-08',
                                      '2025-01-15', '2025-06-22',
                                      '2026-02-27', '2026-03-12'})
        positive, _ = self.run_find(episodes, reference='BZ=F')
        negative, _ = self.run_find(episodes, direction='neg', reference='BZ=F')
        self.assertFalse(positive & negative)
        self.assertIn('2015-07-14', negative)
        self.assertNotIn('2015-07-14', positive)
        tariffs, _ = self.run_find(episodes, direction='neg', reference='^GSPC', theme='regulatory')
        self.assertIn('2018-03-22', tariffs)

    def test_build_preserves_reference_and_source_without_legacy_contamination(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            daily, kb = root / 'daily', root / 'kb'
            day = daily / '2026-09-13'
            day.mkdir(parents=True)
            kb.mkdir()
            for i in range(3):
                (day / f'news_{i}.md').touch()
            def harvest(path):
                ref, sign = [('BZ=F', 'pos'), ('IYT', 'neg'), ('', 'neg')][int(path.stem[-1])]
                text = f'| `direction_reference` | {ref} |\n| 2019-05-12 | {sign} | shipping_chokepoint | event |'
                return 'commodity_energy', 'bullish', ['shipping_chokepoint'], ['2019-05-12'], text
            lib = kb / '_episodes.yaml'
            with patch.object(analogues, 'DAILY_DIR', daily), patch.object(analogues, 'KB_DIR', kb), patch.object(analogues, 'LIB_PATH', lib), patch.object(analogues, 'REVIEW_PATH', kb / '_direction_reviews.yaml'), patch.object(analogues, 'harvest_card', side_effect=harvest), contextlib.redirect_stdout(io.StringIO()):
                analogues.cmd_build()
            episode = yaml.safe_load(lib.read_text())['episodes'][0]
            self.assertEqual(episode['directions_by_reference'], {'BZ=F': ['pos'], 'IYT': ['neg']})
            self.assertEqual(episode['direction_sources']['BZ=F'], ['card:2026-09-13/news_0.md'])
            self.assertEqual(episode['directions_declared'], ['neg', 'pos'])

if __name__ == '__main__':
    unittest.main()
