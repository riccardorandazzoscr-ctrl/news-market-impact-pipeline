"""Regressioni della revisione: ingestione, benchmark, filtri e cutoff offline."""
import contextlib
import io
import sqlite3
import sys
import tempfile
import unittest
from datetime import date
from pathlib import Path
from unittest.mock import patch
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import forecast_tracking as ft
import analogues as a
from event_study import compute_returns

class PrecisioneTests(unittest.TestCase):
    def test_parser_legacy_combined_and_quarantine(self):
        with tempfile.TemporaryDirectory() as td:
            root=Path(td); day=root/'2026-09-18'; day.mkdir(); p=day/'news_01.md'
            p.write_text('''# Prova
#### `BZ=F`
| Stat | T+1 | T+3 |
|---|---|---|
| mediana | 1% | 2% |
| p25 | -1% | -2% |
| p75 | 3% | 4% |
| N | 12 | 12 |
#### `HO=F` e `CRACK_321`
| Stat | T+1 | T+3 |
|---|---|---|
| **HO=F** mediana | 3% | 4% |
| **HO=F** p25 / p75 | -2% / 5% | -3% / 6% |
| **CRACK_321** mediana | 5% | 6% |
| N | 10 | 10 |
''')
            with patch.object(ft,'DAILY_DIR',root):
                result=ft.parse_card(p)
                self.assertEqual(len(result),6)
                self.assertEqual(result[2]['hist_p25'],-2)
                p.write_text(p.read_text()+'\n#### `^GSPC`\n| Stat | T+1 | T+3 |\n|---|---|---|\n| mediana | 1% | NaN |\n')
                issues=[]; ft.parse_card(p,issues=issues)
                self.assertTrue(issues)

    def test_explicit_abstention_does_not_hide_invalid_table(self):
        with tempfile.TemporaryDirectory() as td:
            root=Path(td); day=root/'2026-09-18'; day.mkdir(); p=day/'news_01.md'
            p.write_text('# Prova\n**Motivo astensione**: nessun analogo compatibile\n')
            with patch.object(ft,'DAILY_DIR',root), contextlib.redirect_stdout(io.StringIO()):
                self.assertEqual(ft.cmd_audit('2026-09-18', require_declared=True),0)
                p.write_text(p.read_text()+'\n### `BZ=F` [previsione]\n| Stat | T+1 |\n|---|---|\n| mediana | NaN |\n')
                bad = []
                self.assertEqual(ft.cmd_audit('2026-09-18', require_declared=True, bad=bad),1)
                self.assertEqual(len(bad), 1)   # la scheda da escludere in 'register'

    def test_live_record_survives_later_malformed_card(self):
        with tempfile.TemporaryDirectory() as td:
            root=Path(td); day=root/'2026-09-18'; day.mkdir(); p=day/'news_01.md'
            p.write_text('# Prova\n### `BZ=F` [previsione]\n| Stat | T+1 |\n|---|---|\n| mediana | NaN |\n')
            row=dict(forecast_id='id', card_path='2026-09-18/news_01.md', registration='live', ingestion_status='ok')
            with patch.object(ft,'DAILY_DIR',root), patch.object(ft,'load_ledger',return_value=[row]), patch.object(ft,'write_ledger'), contextlib.redirect_stdout(io.StringIO()), contextlib.redirect_stderr(io.StringIO()):
                ft.cmd_backfill()
                self.assertEqual(row['ingestion_status'],'ok')

    def test_direction_conflict_keeps_index_but_excludes_directional_pool(self):
        import yaml
        with tempfile.TemporaryDirectory() as td:
            root=Path(td); daily=root/'daily'; kb=root/'kb'; kb.mkdir(); day=daily/'2026-09-18'; day.mkdir(parents=True)
            card=day/'news_01.md'
            card.write_text('| `direction_reference` | BZ=F |\n| 2020-01-01 | pos | oil_supply | event |')
            review=kb/'_direction_reviews.yaml'
            review.write_text(yaml.safe_dump(dict(reviews=[dict(date='2020-01-01',theme='commodity_energy',reference='BZ=F',direction='neg',source='2026-09-18/news_01.md',reason='Conflicting evidence')])))
            lib=kb/'_episodes.yaml'
            with patch.object(a,'DAILY_DIR',daily),patch.object(a,'KB_DIR',kb),patch.object(a,'LIB_PATH',lib),patch.object(a,'REVIEW_PATH',review),patch.object(a,'harvest_card',return_value=('commodity_energy','bullish',[],['2020-01-01'],card.read_text())),contextlib.redirect_stdout(io.StringIO()),contextlib.redirect_stderr(io.StringIO()):
                a.cmd_build()
                self.assertEqual(a._load()[0]['directions_by_reference']['BZ=F'],['neg','pos'])
                for sign in ('pos','neg'):
                    out=io.StringIO()
                    with contextlib.redirect_stdout(out):
                        a.cmd_find('commodity_energy',sign,None,None,1,30,direction_reference='BZ=F',strict=True)
                    self.assertEqual(out.getvalue().strip(),'')

    def test_live_registration_saves_method_and_immutable_forecast(self):
        with tempfile.TemporaryDirectory() as td:
            root=Path(td); day=root/date.today().isoformat(); day.mkdir(); card=day/'news_01.md'
            card.write_text('# Prova\n### `BZ=F` [previsione]\n| Stat | T+1 |\n|---|---|\n| mediana | 1% |\n| N | 12 |\n')
            with patch.object(ft,'DAILY_DIR',root),patch.object(ft,'LEDGER_PATH',root/'ledger.csv'),contextlib.redirect_stdout(io.StringIO()):
                self.assertEqual(ft.cmd_audit(day.name,require_declared=True),0)
                ft.cmd_backfill(day=day.name,live=True)
                original=ft.load_ledger()[0]
                self.assertEqual(original['registration'],'live')
                self.assertTrue((root/'_forecast_methods'/f"{original['method_version']}.json").exists())
                self.assertTrue(list((day/'_forecast_sources').glob('*.md')))
                card.write_text(card.read_text().replace('1%','2%'))
                ft.cmd_backfill(day=day.name,live=True)
                current=ft.load_ledger()[0]
                self.assertEqual(current['expected_median'],original['expected_median'])
                self.assertTrue(current['revised_at'])

    def test_strict_pool_does_not_widen(self):
        eps=[dict(date='2020-01-01',theme='macro_data',events=[dict(subthemes_local=['pmi'], evidence=[dict(subthemes_local=['pmi'])])],subthemes=['pmi']),
             dict(date='2020-02-01',theme='macro_data',events=[dict(subthemes_local=['cpi'], evidence=[dict(subthemes_local=['cpi'])])],subthemes=['pmi'])]
        out=io.StringIO()
        with patch.object(a,'_load',return_value=eps),contextlib.redirect_stdout(out),contextlib.redirect_stderr(io.StringIO()):
            a.cmd_find('macro_data',None,None,['pmi'],12,30,strict=True)
        self.assertEqual(out.getvalue().strip(),'2020-01-01')

    def test_strict_and_does_not_merge_sources(self):
        eps=[dict(date='2020-01-01',theme='macro_data',subthemes=[],
                  events=[dict(subthemes_local=['cpi','nfp'],evidence=[
                      dict(subthemes_local=['cpi']), dict(subthemes_local=['nfp'])])])]
        out=io.StringIO()
        with patch.object(a,'_load',return_value=eps),contextlib.redirect_stdout(out),contextlib.redirect_stderr(io.StringIO()):
            a.cmd_find('macro_data',None,None,['cpi','nfp'],1,30,match_all=True,strict=True)
        self.assertEqual(out.getvalue().strip(),'')

    def test_surprise_is_not_change_in_level(self):
        tax=a.load_taxonomy()
        for txt,expected in [('CPI scende al 3%, ma sopra il consenso del 2,9%.','inflation_upside'),('CPI sale al 3%, ma sotto il consenso del 3,2%.','inflation_downside')]:
            labels=a.labels_from_context(txt,'macro_data',set(),tax)
            self.assertEqual(labels & {'inflation_upside','inflation_downside'},{expected})
        self.assertFalse(a.labels_from_context('CPI scende al 3%.','macro_data',set(),tax)&{'inflation_upside','inflation_downside'})

    def test_as_of_excludes_future_outcomes(self):
        c=sqlite3.connect(':memory:');c.execute('CREATE TABLE prices(ticker,date,adj_close,close)')
        c.executemany('INSERT INTO prices VALUES(?,?,?,?)',[('X',f'2026-01-0{i}',100+i,100+i) for i in range(1,6)])
        got=compute_returns(c,'X',[date(2026,1,1)],[1,3],as_of=date(2026,1,3))
        self.assertEqual(set(got['per_event'][0]['returns']),{1})
        c.close()

    def test_historical_baseline_ignores_future(self):
        import pandas as pd
        prices=pd.Series(range(100,400),index=pd.date_range('2020-01-01',periods=300))
        cutoff=date(2020,8,1)
        first=ft.historical_baseline(prices,cutoff,5)
        prices.loc['2020-08-01':]=999999
        self.assertEqual(first,ft.historical_baseline(prices,cutoff,5))
        self.assertIsNotNone(first)

    def test_baseline_denominators(self):
        rows=[dict(expected_median='1',realized_return='1',hist_p25='-1',hist_p75='2'),dict(expected_median='-1',realized_return='1',hist_p25='',hist_p75=''),dict(expected_median='0.01',realized_return='-1',hist_p25='',hist_p75='')]
        s=ft.metric_summary(rows)
        self.assertEqual((s['n_hit'],s['hit'],s['up'],s['down']),(2,0.5,1.0,0.0))
        self.assertEqual(s['n_band'],1)

if __name__=='__main__':unittest.main()
