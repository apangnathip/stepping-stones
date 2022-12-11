# stepping-stones
Mathematical game based on Numberphile's [Stones on an Infinite Chessboard](https://www.youtube.com/watch?v=m4Uth-EaTZ8).
It is defined as the following:

- A chessboard of size *n\*n* is given.
- An arbitrary base configuration of stones whose value is one is chosen.
- A stone of one value higher can then be placed on cells where its total neighbouring sum is equivalent to the stone's value.
- Repeat stone placement until there is no further stones can be placed.

With these rules, what is the highest possible stone value you can achieve with the base configuration?

---

For example, a 5x5 chessboard with the following base configuration:

![steppingstonedemo](https://user-images.githubusercontent.com/92758882/206932182-940ce00c-9a53-4e88-bb81-b6ac60e13136.gif)
