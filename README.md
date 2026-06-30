## Order book project

Program connects to Coinbase coin of your choice (.env) and plots liquidity data live in-browser. Will also write streamed data to a local sqlite db. Yellow is highest liquidity in graph.

Musings currrently commented in among the code. Bit rusty with python coming in, part of the motivation to do this project was reacquanting myself. Overall pretty happy with this. Would be even cooler to shift over to Rust or C++, but might be more than I have time for right now.

To run, cd into your Orderbook folder and then run 'python -m http.server 3000'. Run python main.py in a different terminal. Then open the link below. It will take a little bit of time to stretch the labels out properly, this is on my fix list.

http://localhost:3000/index.html

To do:
##### Another pass over frontend to improve look and update label
##### Fully implement logging
##### Enforce types (overlooked before - was rusty in Python)
##### Update syntax with _ for private methods (see above)
