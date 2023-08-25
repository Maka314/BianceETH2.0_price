const socket = new WebSocket("wss://stream.binance.com:9443");

socket.addEventListener("open", function (e) {
  socket.send(`
  {
    "id": "5494febb-d167-46a2-996d-70533eb4d976",
    "method": "exchangeInfo",
    "params": {
      "symbols": ["BNBBTC"]
    }
  }`);
});

socket.addEventListener("message", function (e) {
  console.log(e.data);
});
