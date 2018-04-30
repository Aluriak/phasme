
i:
	python -m phasme infos data/test.gml --graph-properties --negative-results --round-float 3 -sn
c:
	python -m phasme convert data/bad.lp todel.gml --anonymize
	cat todel.gml
	rm todel.gml
g:
	python -m phasme generate out/todel powerlaw_cluster_graph n=5 m=2 p=0.01
graphics:
	- rm *.png
	python -m phasme infos data/realgraph.lp --graphics --graphics-params logxscale=1 logyscale=1 stacked_limits=[1,2,3]
tex:
	python -m phasme convert data/realgraph.lp todel.tex


t: test
test:
	python -m pytest phasme test --doctest-module -vv


.PHONY: t test all
