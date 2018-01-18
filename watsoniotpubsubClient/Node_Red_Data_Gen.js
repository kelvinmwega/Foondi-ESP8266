var test1 = [0,1];

// Counter to select from array.
var counter1 = context.get('counter1')||0;
counter1 = counter1+1;
if(counter1 > 1) counter1 = 0;
context.set('counter1',counter1);

// Create MQTT message in JSON
msg.payload = test1[counter1];

return msg;
