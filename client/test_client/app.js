// Encapsulate in an immediately invoked function for scope control
(function() {
  // Broker settings - using websockets
  var broker = "192.168.1.2";
  var port = 9001; // Ensure your broker supports websockets on this port
  // Generate a random client id to avoid conflicts
  var clientId = "ZigorClient";

  // Create the MQTT client instance. The fourth parameter is the client id.
  // The "/mqtt" parameter is the WebSocket path – change it if your broker requires a different path.
  var client = new Paho.Client(broker, port, "", clientId);

  // Called when the client loses its connection
  client.onConnectionLost = function(responseObject) {
    console.error("Connection lost:", responseObject.errorMessage);
  };

  // Called when a message arrives
  client.onMessageArrived = function(message) {
    console.log("Message arrived:", message.payloadString);
    try {
      var data = JSON.parse(message.payloadString);
      // Update the title if provided
      if (data.title) {
        document.getElementById("title").innerText = data.title;
      }
      // Update the body text if provided
      if (data.body) {
        document.getElementById("body").innerText = data.body;
      }
    } catch (e) {
      console.error("Failed to parse JSON message:", e);
    }
  };

  // Set options and callbacks for a successful connection
  var options = {
    onSuccess: function() {
      console.log("Connected to broker");
      // Subscribe to the topic after connecting successfully
      client.subscribe("zigor/screen");
    },
    onFailure: function(message) {
      console.error("Connection failed:", message.errorMessage);
    }
  };

  // Connect the client
  client.connect(options);

  // Function to publish a command message to the "zigor/input" topic.
  function publishCommand(command) {
    var mqttMessage = new Paho.Message(command);
    mqttMessage.destinationName = "zigor/input";
    client.send(mqttMessage);
  }

  // Add click event listeners for the buttons to publish the corresponding commands
  document.getElementById("prev").addEventListener("click", function() {
    publishCommand("PREV");
  });
  document.getElementById("enter").addEventListener("click", function() {
    publishCommand("ENTER");
  });
  document.getElementById("next").addEventListener("click", function() {
    publishCommand("NEXT");
  });

  // Add a wheel event listener to capture scroll wheel events
  document.addEventListener("wheel", function(event) {
    // Event.deltaY will be positive when scrolling down, negative when scrolling up
    if (event.deltaY > 0) {
      publishCommand("PREV");
    } else if (event.deltaY < 0) {
      publishCommand("NEXT");
    }
  }, { passive: true });

})();

