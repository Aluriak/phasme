
i:
	python -m grasp infos data/test.gml --graph-properties --negative-results --round-float 3
c:
	python -m grasp convert data/bad.lp todel.gml --anonymize
	cat todel.gml
	rm todel.gml
g:
	python -m grasp generate out/todel powerlaw_cluster_graph n=5 m=2 p=0.01


t: test
test:
	python -m pytest grasp test --doctest-module -vv


.PHONY: t test all
