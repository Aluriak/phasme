
i:
	python -m grasp infos data/test.gml --graph-properties --negative-results --round-float 3
c:
	python -m grasp clean data/bad2.lp -o todel


t: test
test:
	python -m pytest grasp test --doctest-module -vv


.PHONY: t test all
