# Back Story

As an SRE, I manage hundreds of repositories daily, often jumping between them to assist with actions, deployments, and more. This constant context switching requires a significant amount of energy and focus, especially when it comes to creating pull requests and awaiting developer reviews. Many developers, understandably, may not be fully familiar with GitHub Actions, which adds an extra layer of cognitive load for them as well. It quickly became clear that this process was unnecessarily resource-intensive.

By leveraging repository_dispatch, the SRE team can centralize action management in a single repository (the one housing the receiver actions). Developers, instead of modifying workflows across multiple repos, can trigger these actions via the GitHub API, targeting their desired receiver using event_type. However, the downside of this approach is that developers must navigate to a different repository to view action statuses—an inconvenient step that disrupts workflow.

After searching for a solution and seeing that others had encountered the same pain point, I decided to build it myself.
