import py.test

from csirtg_smrt import Smrt
from csirtg_smrt.rule import Rule
from csirtg_smrt.constants import REMOTE_ADDR
from pprint import pprint

rule = 'test/malc0de/malc0de.yml'
rule = Rule(path=rule)
rule.fetcher = 'file'
s = Smrt(REMOTE_ADDR, 1234, client='dummy')


def test_malc0de_urls():
    rule.remote = 'test/malc0de/feed.txt'
    x = s.process(rule, feed='urls')
    x = list(x)

    assert len(x) > 0
    assert len(x[0].indicator) > 4

    indicators = set()
    for xx in x:
        indicators.add(xx.indicator)

    assert 'http://url.goosai.com/down/ufffdufffd?ufffdufffdufffd?ufffdufffdbreakprisonsearchv2.7u03afu06f0ufffdufffdufffdufffdufffdufffdat25_35027.exe' in indicators


def test_malc0de_malware():
    rule.remote = 'test/malc0de/feed.txt'
    x = s.process(rule, feed='malware')
    x = list(x)

    assert len(x) > 0
    assert len(x[0].indicator) > 4

    indicators = set()

    for xx in x:
        indicators.add(xx.indicator)

    assert '55dd72e153fbd0cf4cb86dc9a742ce74' in indicators
