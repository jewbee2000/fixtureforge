# Blog brief and release criteria

Working title: **The fixture has to leave room for the wrench**

Target length after implementation: 600–900 words. Audience: a technically curious reader who enjoys building things; not a job application reviewer addressed directly. Use first person, concrete engineering details, and mild humor when natural. Walter's bicycle-parts and couch-riser posts begin with a practical motivation and describe constraints plainly. Avoid a generic thought-leadership essay, copied phrases from other writers, inflated AI claims, or invented autobiographical stories.

The current draft is prospective. It is suitable as a starting point, not a finished retrospective. Convert future tense to past tense only when the referenced work exists. Preserve the honest distinction between Walter choosing/directing the project and an agent doing implementation work. The user has authorized first-person drafting, but personal beliefs or anecdotes beyond the supplied context remain suggestions for his review.

## Evidence to add after implementation

- One real screenshot or diagram of the project's result, with an explanatory caption.
- One specific failed candidate, what the independent check found, and the actual repair.
- One decision Walter or the agent made, its tradeoff, and whether it worked.
- The real command a reader can run, verified repository URL, and a link to the evidence report.
- What the project establishes and what remains untested. Any reported number must link to a recorded result.

Do not require a paid live-model campaign to write an honest post about building with Codex. Development evidence is meaningful in its own right. A replay demonstrates the evaluation mechanism, not model success. If live trials are added, include the denominator and failed attempts.

## Editorial handoff

Canonical editorial copy for this setup is the Jekyll file `_drafts/fixtureforge.md` in the accompanying website-drafts checkout. `docs/BLOG_DRAFT.md` is a convenience copy; after implementation, update the website draft and then sync this copy. Keep `published: false` until the actual project, links, and article are ready and publication is authorized. Set the article's publication date at that point, not in advance.

## Current draft


One of the nice things about a small mechanical project is that it gives an abstract idea a very specific shape. In this case, that shape is a clamp for a cylindrical sensor. It is not a particularly glamorous object, which is part of the appeal.

I have enjoyed designing and printing parts for projects like bicycle components and a robotic pruning attachment. Those projects make the connection between a model on a screen and a useful physical object fairly direct. They also make it difficult to ignore the ordinary details: where the fastener goes, how the part is assembled, and whether there is room to get a tool into it.

FixtureForge is an attempt to bring those details into an experiment with AI-generated designs. I want to give an agent a small set of requirements and have it propose a sensor fixture. The fixture needs to hold a particular diameter, fit a mounting pattern, leave the connector accessible, and produce files that someone else can inspect.

The first version will be intentionally restrictive. It will generate one family of two-part clamps rather than attempt to design whatever mechanical object someone describes. I think that constraint makes the question more interesting: can the result satisfy a clear contract, including the parts of the contract that are easy to overlook in a pretty rendering?

I want the checking software to look at the exported geometry. Asking a program what diameter it intended to draw is not the same as measuring the hole it actually produced. The inspection should also include the space occupied by a screw head, a connector, and the tool needed to assemble everything.

For the agent, the simplest version of the job is to propose dimensions in a structured format. A conventional parametric model can turn those dimensions into solids. That keeps the experiment manageable and gives a failed check something specific to say. If I later let the agent write arbitrary CAD code, it should still have to pass the same geometric checks.

There is an obvious limit here: checking a CAD model does not tell me how a printed part will fit or how much load it can carry. I want the report to be clear about that. A later print-and-measure experiment would be a good excuse to get away from the computer, but I do not want to label the model's dimensions as measurements of a part that does not exist.

The result I am hoping for is a modest but useful loop: describe a fixture, generate it, discover what is wrong, and improve it. A clamp that leaves room for the wrench would be a fine place to start.

## Usefulness audit of 2026-10-04

The current contribution is: A fixture service-access checker plus a parametric sensor-clamp example: verify that connectors, screws, and tools can actually reach their intended positions. Explain the existing tools, the narrow gap tested in M0, the non-default consumer example, one real failure, and any reason the result is best delivered as an integration. Do not claim a first-of-its-kind tool. Product AI features are optional. The current draft remains prospective; rewrite it after implementation from actual evidence and [REQUIREMENTS.md](REQUIREMENTS.md).
