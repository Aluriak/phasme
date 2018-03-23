
i:
	python -m grasp infos data/test.gml
c:
	python -m grasp clean data/bad2.lp -o todel


t: test
test:
	python -m pytest grasp test --doctest-module


.PHONY: t test all
