cxmate-py
=========

<img align="right" height="300" src="http://www.cytoscape.org/images/logo/cy3logoOrange.svg">

---

cxmate-py provides a Python SDK for interacting with [cxMate](https://github.com/cxmate/cxmate), an adapter that allows Cytoscape to talk to network services. This SDK enables quick and painless development of a cxMate service, follow the Getting Started guide to learn more about the process.

---

_cxMate is an official [Cytoscape](http://www.cytoscape.org) project written by the Cytoscape team._

Installation
------------

Install the cxMate SDK via pip.

```
pip install cxmate
```

Getting Started
---------------

Import the cxmate python mode:
```python
import cxmate
```

Create a subclass of the `cxMate.Service` class from the module:
```python
class MyEchoService(cxmate.Service):
```

Implement a single method in the class called process. It takes two arguments, a dictionary of parameters, and an element generator:
```python
class MyEchoService(cxmate.Service):

    def process(self, params, input_stream):
        """
        process is a required method, if it's not implemented, cxmate.service will throw an error
        this process implementation will echo the received network back to the sender

        :param input_stream: a python generator that returns CX elements
        :returns: a python generator that returns CX elements
        """
```

Whenever your service is called, cxMate will call your process method for you. you must extract networks from the element generator to create your input networks. cxMate comes with an adapter class to make conversion to popular network formats simple.
To send networks back to cxMate, you must return a network element generator. cxMate's adapter class can handle this also for various popular network formats:
```python

    def process(self, params, input_stream):
        network = cxmate.Adapter.to_networkx(input_stream)
        # Do stuff with network here
        return cxmate.Adapter.from_networkx(network)
```

Finally, setup your service to run when envoked. the cxmate.Service superclass implements a run method for you that takes an optional 'address:port' string.
```python
if __name__ == "__main__":
  myService = MyService()
  myService.run() #run starts the service listening for requests from cxMate
```

Working with streams
--------------------
cxMate translates a network request to a call to your `process(self, params, input_stream)` method. It expects this method to handle the request and return a new stream that cxMate can use to respond to the network request. While cxMate provides an `Adapter` class to read and write streams using popular Python network formats, there are cases where its neccesarry or benficial to understand and work the the streams directly.

A stream is a generator function (a function that yields values on demand). You'll need to understand Python generators to proceed with this tutorial. The generator returns NetworkElement objects. Each NetworkElement object contains a label field. The label determines which network the object belongs to, for example, a stream containing two networks may contain objects with labels 'network1' and 'network2'.

A NetworkElement object is a wrapper. It may contain any valid aspect type that has been assigned to a network in the `cxmate.json` file. To determine the type of the element in the wrapper, use the call `wrapper.WhichOneof('element')` (assuming that wrapper is a NetworkElement object). This call will return the type of the element as a string.

Once you've obtained the type of the wrapper, the concrete element can be obtained by calling it's respective property on the wrapper. The property name will match the string returned by `WhichOneof`.

```python
  for net_element in input_stream:
      print net_element.label
      net_element_type = net_element.WhichOneof('element')
      if net_element_type == 'node':
          node = net_element.node
      elif net_element_type == 'edge':
          edge = net_element.edge
```

When cxMate calls your `process(self, params, input_stream)` method, it expects a generator as a return value. This requests the construction of *new* NetworkElement objects. The NetworkElement object is defined in the `cxmate.cxmate_pb2` module. The example below creates an output_stream that contains a single network consisting of a single edge. It's important to note that to create the concrete type of the NetworkElement, a reference to the edge is taken from the new element. Trying to create a new edge seperately and assigning it to the edge property will not work.

```python
  def output_stream():
      my_net_element = NetworkElement()
      my_net_element.label = 'my_output_network'
      edge = my_net_element.edge
      edge.id = 1
      edge.target = 1
      edge.source = 2
      yield my_net_element
```

Using streams it's possible to implement online algorithms. Return a generator that has been curried with the input_stream. For each NetworkElement read from the input_stream, yield a new NetworkElement. Vary this pattern to perform any kind of batch processing.

Contributors
------------

We welcome all contributions via Github pull requests. We also encourage the filing of bugs and features requests via the Github [issue tracker](https://github.com/cxmate/cxmate-py/issues/new). For general questions please [send us an email](eric.david.sage@gmail.com).

License
-------

cxmate-py is MIT licensed and a product of the [Cytoscape Consortium](http://www.cytoscapeconsortium.org).

Please see the [License](https://github.com/cxmate/cxmate-py/blob/master/LICENSE) file for details.
