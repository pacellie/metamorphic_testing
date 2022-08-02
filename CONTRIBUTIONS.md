This file lists contributions by the individual team members.
Our team did a lot of trial & error, so this file is comparatively important.

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
- Implementation of Acoustic Event Classification (aec) example with the proposed metamorphic testing framework. See issues: #61, #64, merge request: !35 and the summary [WiKi Page](https://gitlab.lrz.de/pypracticum/team-mt-metamorphic-testing-framework/-/wikis/Metamorphic-Testing-For-Acoustic-Event-(Scene)-Classification-(idea-and-a-paper-summary))
- Refactoring audio visualizer to a callable class so that it can be used by both speech recognition and acoustic scene understanding examples with different sampling rate. See issue #126
- Refactoring audio examples to put speech recognition and acoustic scene classification into different folders so that tests can be executed separately from GUI web app. See issue #129 and merge request !45

Danny Benlin Oswan
===
- Gathered examples, see [wiki page](https://gitlab.lrz.de/pypracticum/team-mt-metamorphic-testing-framework/-/wikis/Examples-for-Metamorphic-Testing) (mainly [issue 13](https://gitlab.lrz.de/pypracticum/team-mt-metamorphic-testing-framework/-/issues/13), including chains and uneven relations.
- Investigated how Hypothesis is related to pytest and the pytest hooks, [issue 10](https://gitlab.lrz.de/pypracticum/team-mt-metamorphic-testing-framework/-/issues/13) or [first section in this wiki](https://gitlab.lrz.de/pypracticum/team-mt-metamorphic-testing-framework/-/wikis/Inspiration-from-hypothesis).
- Evaluate 3 old frameworks on chaining, [issue 41](https://gitlab.lrz.de/pypracticum/team-mt-metamorphic-testing-framework/-/issues/41), experimented on 3 branches named `experiment-from*-danny`.
- Code the examples for image MR (in examples/image_classifier and facial_keypoints) and shortest path algorithm, incl. the logging and docstrings in it (except the visualizer in classifier, that was Paul's).
- Added basics of [logging](https://gitlab.lrz.de/pypracticum/team-mt-metamorphic-testing-framework/-/issues/72), [exception](https://gitlab.lrz.de/pypracticum/team-mt-metamorphic-testing-framework/-/issues/65), and [docstring](https://gitlab.lrz.de/pypracticum/team-mt-metamorphic-testing-framework/-/issues/67).
- Prepared demo machine, including [wiki for audio setup](https://gitlab.lrz.de/pypracticum/team-mt-metamorphic-testing-framework/-/wikis/How-to-run-audio-examples-(Windows)), added into readme.
- Cleanup: logging, annotation, docstring, style for image MR and shortest path example.

Ting-Yu Lu
===
- Implement one of the initial framework architectures (#2, [branch](https://gitlab.lrz.de/pypracticum/team-mt-metamorphic-testing-framework/-/tree/framework-iris), [wiki](https://gitlab.lrz.de/pypracticum/team-mt-metamorphic-testing-framework/-/wikis/Ideas-on-how-code-using-our-framework-could-look#ting-yu-lu))
- Set up poetry ([#6](https://gitlab.lrz.de/pypracticum/team-mt-metamorphic-testing-framework/-/issues/6), [wiki](https://gitlab.lrz.de/pypracticum/team-mt-metamorphic-testing-framework/-/wikis/Poetry-command)) and linter CI pipeline ([#20](https://gitlab.lrz.de/pypracticum/team-mt-metamorphic-testing-framework/-/issues/20))
- Research paper "A New Method for Constructing Metamorphic Relations" and "Theoretical and Empirical Analyses of the Effectiveness of Metamorphic Relation Composition" ([#42](https://gitlab.lrz.de/pypracticum/team-mt-metamorphic-testing-framework/-/issues/42), [wiki](https://gitlab.lrz.de/pypracticum/team-mt-metamorphic-testing-framework/-/wikis/Papers-summaries))
- Pair programming with Martin Rau for the final framework architecture ideas ([branch](https://gitlab.lrz.de/pypracticum/team-mt-metamorphic-testing-framework/-/tree/framework-simon-iris))
- Implement additional framework features ([#46](https://gitlab.lrz.de/pypracticum/team-mt-metamorphic-testing-framework/-/issues/46), [#57](https://gitlab.lrz.de/pypracticum/team-mt-metamorphic-testing-framework/-/issues/57), [#69](https://gitlab.lrz.de/pypracticum/team-mt-metamorphic-testing-framework/-/issues/69), [#70](https://gitlab.lrz.de/pypracticum/team-mt-metamorphic-testing-framework/-/issues/70), [#71](https://gitlab.lrz.de/pypracticum/team-mt-metamorphic-testing-framework/-/issues/71), [#73](https://gitlab.lrz.de/pypracticum/team-mt-metamorphic-testing-framework/-/issues/73), [#77](https://gitlab.lrz.de/pypracticum/team-mt-metamorphic-testing-framework/-/issues/77), #87, [#115](https://gitlab.lrz.de/pypracticum/team-mt-metamorphic-testing-framework/-/issues/115))
- Research pytest-commander and pytest-html ([#91](https://gitlab.lrz.de/pypracticum/team-mt-metamorphic-testing-framework/-/issues/91), [branch](https://gitlab.lrz.de/pypracticum/team-mt-metamorphic-testing-framework/-/tree/91-pytest-commander-experiment), [wiki](https://gitlab.lrz.de/pypracticum/team-mt-metamorphic-testing-framework/-/wikis/Pytest-commander-&-Pytest-html))
- Write external documentation ([#101](https://gitlab.lrz.de/pypracticum/team-mt-metamorphic-testing-framework/-/issues/101))
- Write docstrings for one single file (#112, [branch](https://gitlab.lrz.de/pypracticum/team-mt-metamorphic-testing-framework/-/tree/112-helper-docstrings))
- Test part of the final framework (#74, [branch](https://gitlab.lrz.de/pypracticum/team-mt-metamorphic-testing-framework/-/tree/74-test-helper-and-suite))

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
- Wrote tests for the execution report (#74)
- Team lead

Martin Rau
===
- Research hypothesis and pytest testing frameworks, in particular dig through all the pytest plugins with focus on pytest-timeout and pytest-xdist ([wiki](https://gitlab.lrz.de/pypracticum/team-mt-metamorphic-testing-framework/-/wikis/Testing-Frameworks-Quicklinks), [pytest-timeout branch](https://gitlab.lrz.de/pypracticum/team-mt-metamorphic-testing-framework/-/tree/feature/pytest-timeout), [pytest-xdist branch](https://gitlab.lrz.de/pypracticum/team-mt-metamorphic-testing-framework/-/tree/feature/pytest-xdist)).
- Design and implement an initial framework architecture and sin/addition examples ([branch](https://gitlab.lrz.de/pypracticum/team-mt-metamorphic-testing-framework/-/tree/feature/architecture-martin), [wiki](https://gitlab.lrz.de/pypracticum/team-mt-metamorphic-testing-framework/-/wikis/Ideas-on-how-code-using-our-framework-could-look)).
- Re-design and re-implement the framework architecture ([branch](https://gitlab.lrz.de/pypracticum/team-mt-metamorphic-testing-framework/-/tree/feature/decorator-architecture)).
- Finalize framework design and implementation in pair-programming session with Ting-Yu Lu([branch](https://gitlab.lrz.de/pypracticum/team-mt-metamorphic-testing-framework/-/tree/framework-simon-iris)).
- Explore A,B,AB,BA approach of Simon. ([branch](https://gitlab.lrz.de/pypracticum/team-mt-metamorphic-testing-framework/-/blob/feature/a-b-ab-ba-example/tests/test_a_b_ab_ba.py))
- Improve Code quality: Docstrings ([branch](https://gitlab.lrz.de/pypracticum/team-mt-metamorphic-testing-framework/-/commit/bcc41c69f9b64f2eef23bd220708638688279d5b)), Typing ([branch1](https://gitlab.lrz.de/pypracticum/team-mt-metamorphic-testing-framework/-/tree/68-typing), [branch2](https://gitlab.lrz.de/pypracticum/team-mt-metamorphic-testing-framework/-/tree/68/typing-v2)).
- Improve failing test output ([branch](https://gitlab.lrz.de/pypracticum/team-mt-metamorphic-testing-framework/-/tree/88-89/improve-failing-test)), also in the console ([branch](https://gitlab.lrz.de/pypracticum/team-mt-metamorphic-testing-framework/-/tree/106/better-failed-tests-in-console)).
- Implement one-by-one test execution a few times since we broke it twice again ([branch](https://gitlab.lrz.de/pypracticum/team-mt-metamorphic-testing-framework/-/tree/102/one-by-one-test-execution-in-gui)).
- Implement tests for parts of the core framework ([branch](https://gitlab.lrz.de/pypracticum/team-mt-metamorphic-testing-framework/-/tree/74/framework-tests-decorator-metamorphic)).
