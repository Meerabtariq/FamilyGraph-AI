male(rehan).
male(salman).
male(mustafa).
male(ibtisam).
male(abdullah). 
female(ayesha).
female(mahnoor).
female(eman).
female(saneeaa).
female(hira).

/* Relationships */
parent(rehan, salman).
parent(rehan, mahnoor).
parent(ayesha, salman).
parent(ayesha, mahnoor).
parent(salman, mustafa).
parent(salman, ibtisam).
parent(mahnoor, eman).
parent(mahnoor, saneeaa).
parent(salman, hira). 
parent(hira, abdullah).

/* Rules */
father(X, Y) :- male(X), parent(X, Y).
mother(X, Y) :- female(X), parent(X, Y).
grandfather(X, Y) :- father(X, Z), parent(Z, Y).
grandmother(X, Y) :- mother(X, Z), parent(Z, Y).
uncle(X, Y) :- brother(X, Z), parent(Z, Y).
aunt(X, Y) :- sister(X, Z), parent(Z, Y).
brother(X, Y) :- male(X), sibling(X, Y).
sister(X, Y) :- female(X), sibling(X, Y).
sibling(X, Y) :- parent(Z, X), parent(Z, Y), X \= Y.