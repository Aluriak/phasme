
i:
	python -m phasme infos data/test.gml --graph-properties --negative-results --round-float 3 -sn
c:
	python -m phasme convert data/bad.lp todel.gml --anonymize
	cat todel.gml
	rm todel.gml
g:
	python -m phasme generate out/todel powerlaw_cluster_graph n=5 m=2 p=0.01
tex:
	python -m phasme convert data/realgraph.lp todel.tex
e:
	python -m phasme extract data/realgraph.lp todel.lp nodes a b 2


t: test
test:
	python -m pytest phasme test --doctest-module -vv


.PHONY: t test all
