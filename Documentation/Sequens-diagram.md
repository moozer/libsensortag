How the clients communicates with the sensortag
===============================================

![Sequence Diagram For Reading Temp Sensor Value](Sequence-diagram-of-sensortag-communication.png "Sequence Diagram")



As show above you can see that the client sends a connect message to the sensortag, which returns a message telling if the connection was successful or not.
Then you give a write command to an ID on the sensortag, then you write a read command to another ID.
The sensortag then sends you what value there is stored there.
Then you write a disconnect, and the connection between the client and sensortag ends.