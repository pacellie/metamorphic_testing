This file lists contributions by the individual team members.
Our team did a lot of trial & error, so this file is comparatively important.

Name
===
- ...
- ...

Tathagata Bandyopadhyay
===
- Research on machine learning based metamorphic testing examples. See [WiKi Page](https://gitlab.lrz.de/pypracticum/team-mt-metamorphic-testing-framework/-/wikis/Examples-for-Metamorphic-Testing#ml_examples_by_tathagata) (Scroll down to the bottom of the page)
- Research and ideation on Class based framework approach, although we decided to use some other approach finally. See [here](https://gitlab.lrz.de/pypracticum/team-mt-metamorphic-testing-framework/-/issues/40#note_1879716)
- Study on Audio augmentation Framework. See [Wiki Page](https://gitlab.lrz.de/pypracticum/team-mt-metamorphic-testing-framework/-/wikis/Audiomentations:-A-audio-augmentation-library)
- Comparison of our approach with MT_Keras. See [Wiki Page](https://gitlab.lrz.de/pypracticum/team-mt-metamorphic-testing-framework/-/wikis/MTKeras-Idea-(paper-summary))
- Ideation and implementation of an advanced deep learning based metamorphic example for **Speech Recognition**. See #49, #51, #54, #55, #62, #63
- Research on finding a proper metamorphic relation for speech Recognition. See #62 and [this WiKi page](https://gitlab.lrz.de/pypracticum/team-mt-metamorphic-testing-framework/-/wikis/Finding-a-suitable-metamorphic-relation-for-Speech-Recognition)
- Writing all docstrings. See #65
- Ideation on how to log and visualize non-text data (image and audio for us) (Discusion & Brainstorming)
- Implementation of audio logger and visualizer. See #116
- Flask based GUI web app for running the tests module wise. #118, #123, 37102629, !32
- Flask GUI response caching issue debuging and fixing. See issue #125 and [this wiki page](https://gitlab.lrz.de/pypracticum/team-mt-metamorphic-testing-framework/-/wikis/Issue-%23125-fix,-a-most-interesting-debugging-and-bug-fix)
- Implementation of Acoustic Event Classification (aec) example with the proposed metamorphic testing framework and corresponding refactoring of audio visualizer. See issues: #61, #64, #126, merge request: !35 and the summary [WiKi Page](https://gitlab.lrz.de/pypracticum/team-mt-metamorphic-testing-framework/-/wikis/Metamorphic-Testing-For-Acoustic-Event-(Scene)-Classification-(idea-and-a-paper-summary))


Danny Benlin Oswan
===
- Gathered examples, see wiki page (mainly issue 13), including chains and uneven relations.
- Investigated how Hypothesis is related to pytest (issue 10).
- Evaluate 3 old frameworks on chaining (issue 41).
- Code the examples for image MR (in examples/image_classifier), then fix it for pipeline.
- Added basics of logging, exception, and docstring (72, 65, 67).
- Merge image examples to main.
- Prepared image demos.

Ting-Yu Lu
===
- Framework architecture exploration ([#2](https://gitlab.lrz.de/pypracticum/team-mt-metamorphic-testing-framework/-/issues/2), [branch](https://gitlab.lrz.de/pypracticum/team-mt-metamorphic-testing-framework/-/tree/framework-iris), [wiki](https://gitlab.lrz.de/pypracticum/team-mt-metamorphic-testing-framework/-/issues/2))
- Setup poetry ([#6](https://gitlab.lrz.de/pypracticum/team-mt-metamorphic-testing-framework/-/issues/6), [wiki](https://gitlab.lrz.de/pypracticum/team-mt-metamorphic-testing-framework/-/wikis/Poetry-command)), linter CI pipeline ([#20](https://gitlab.lrz.de/pypracticum/team-mt-metamorphic-testing-framework/-/issues/20))
- Two papers research ([#42](https://gitlab.lrz.de/pypracticum/team-mt-metamorphic-testing-framework/-/issues/42), [wiki](https://gitlab.lrz.de/pypracticum/team-mt-metamorphic-testing-framework/-/wikis/Papers-summaries))
- Additional framework features implementation ([#46](https://gitlab.lrz.de/pypracticum/team-mt-metamorphic-testing-framework/-/issues/46), [#57](https://gitlab.lrz.de/pypracticum/team-mt-metamorphic-testing-framework/-/issues/57), [#69](https://gitlab.lrz.de/pypracticum/team-mt-metamorphic-testing-framework/-/issues/69), [#70](https://gitlab.lrz.de/pypracticum/team-mt-metamorphic-testing-framework/-/issues/70), [#71](https://gitlab.lrz.de/pypracticum/team-mt-metamorphic-testing-framework/-/issues/71), [#73](https://gitlab.lrz.de/pypracticum/team-mt-metamorphic-testing-framework/-/issues/73), [#77](https://gitlab.lrz.de/pypracticum/team-mt-metamorphic-testing-framework/-/issues/77), [#115](https://gitlab.lrz.de/pypracticum/team-mt-metamorphic-testing-framework/-/issues/115), [branch](https://gitlab.lrz.de/pypracticum/team-mt-metamorphic-testing-framework/-/tree/framework-simon-iris))
- Research pytest-commander and pytest-html ([#91](https://gitlab.lrz.de/pypracticum/team-mt-metamorphic-testing-framework/-/issues/91), [branch](https://gitlab.lrz.de/pypracticum/team-mt-metamorphic-testing-framework/-/tree/91-pytest-commander-experiment), [wiki](https://gitlab.lrz.de/pypracticum/team-mt-metamorphic-testing-framework/-/wikis/Pytest-commander-&-Pytest-html))
- External documentation ([#101](https://gitlab.lrz.de/pypracticum/team-mt-metamorphic-testing-framework/-/issues/101))

Paul Schwind
===
- Implemented one of the initial concepts (#2, documented [in the Wiki](https://gitlab.lrz.de/pypracticum/team-mt-metamorphic-testing-framework/-/wikis/Ideas-on-how-code-using-our-framework-could-look#paul-schwind)), also with a working implementation)
- Implemented sin example and housing price example using the concept framework (see above, also #47)
- Paper summary of "A Template-Based Approach to Describing Metamorphic Relations" ([Wiki page](https://gitlab.lrz.de/pypracticum/team-mt-metamorphic-testing-framework/-/wikis/Papers-summaries#a-template-based-approach-to-describing-metamorphic-relations))
- Research on hypothesis strategies ([Wiki page](https://gitlab.lrz.de/pypracticum/team-mt-metamorphic-testing-framework/-/wikis/Inspiration-from-hypothesis#how-test-case-generation-works))
- CI Setup Testing #20
- Research into transformation chaining (see comments in #24)
- Put house pricing into final framework and refactored code a bit (#79)
- Put a visualization of Metamorphic Testing into pytest-html reports of the tests (#100, #103)
- Improved how failed tests look in the GUI (#104)
- Implemented: show function source code in GUI on hover (#110)
