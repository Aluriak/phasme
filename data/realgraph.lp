% A graph with trees, a triangle and a cactus inside.
edge(a,(b;c)).
edge(b,(d;e)).
edge(c,(f;g)).
% The graph: triangle
edge(h,(a;i;j)).
edge(i,j).
% The graph: cactus
edge(k,(j;o;l)).
edge(m,(n;l)).
edge(n,o).
% The graph: showing up tree
edge(m,(q;r)).
