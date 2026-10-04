<!-- Prospective draft: revised requirements and BLOG_BRIEF.md govern the eventual article. No implementation results or novelty claims are established. -->

# The fixture has to leave room for the wrench

Unpublished prospective draft. Implementation and results are pending.


One of the nice things about a small mechanical project is that it gives an abstract idea a very specific shape. In this case, that shape is a clamp for a cylindrical sensor. It is not a particularly glamorous object, which is part of the appeal.

I have enjoyed designing and printing parts for projects like bicycle components and a robotic pruning attachment. Those projects make the connection between a model on a screen and a useful physical object fairly direct. They also make it difficult to ignore the ordinary details: where the fastener goes, how the part is assembled, and whether there is room to get a tool into it.

FixtureForge is an attempt to bring those details into an experiment with AI-generated designs. I want to give an agent a small set of requirements and have it propose a sensor fixture. The fixture needs to hold a particular diameter, fit a mounting pattern, leave the connector accessible, and produce files that someone else can inspect.

The first version will be intentionally restrictive. It will generate one family of two-part clamps rather than attempt to design whatever mechanical object someone describes. I think that constraint makes the question more interesting: can the result satisfy a clear contract, including the parts of the contract that are easy to overlook in a pretty rendering?

I want the checking software to look at the exported geometry. Asking a program what diameter it intended to draw is not the same as measuring the hole it actually produced. The inspection should also include the space occupied by a screw head, a connector, and the tool needed to assemble everything.

For the agent, the simplest version of the job is to propose dimensions in a structured format. A conventional parametric model can turn those dimensions into solids. That keeps the experiment manageable and gives a failed check something specific to say. If I later let the agent write arbitrary CAD code, it should still have to pass the same geometric checks.

There is an obvious limit here: checking a CAD model does not tell me how a printed part will fit or how much load it can carry. I want the report to be clear about that. A later print-and-measure experiment would be a good excuse to get away from the computer, but I do not want to label the model's dimensions as measurements of a part that does not exist.

The result I am hoping for is a modest but useful loop: describe a fixture, generate it, discover what is wrong, and improve it. A clamp that leaves room for the wrench would be a fine place to start.
