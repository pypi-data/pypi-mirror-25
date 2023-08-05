Sourdough
=========

Sourdough is a tool to install chef-client during instance boot.

FAQs
====

How are node names generated?
-----------------------------

In EC2
~~~~~~

If we're in EC2, we look for a Node tag/knob. If the Node tag/knob
exists, our node name will be
**AWS\_REGION-NODE\_TAG\_KNOB-INSTANCE\_ID**

If the node tag/knob doesn't exist, we look for the Hostname tag/knob
and set the node name to **AWS\_REGION-HOSTNAME\_TAGKNOB**.

If the Hostname tag/knob is missing we fail back to reading the output
of ``hostname``

Outside EC2
~~~~~~~~~~~

If we aren't in EC2, we look for a ``/etc/knobs/Hostname`` file and use
the contents of that - if there's no knob file we use the output of
``hostname`` so we have at least something sane-ish.
