# 5. Bug Reporting Guidelines


When you find a bug inPostgreSQLwe want to hear about it. Your bug reports play an important part in makingPostgreSQLmore reliable because even the utmost care cannot guarantee that every part ofPostgreSQLwill work on every platform under every circumstance.


The following suggestions are intended to assist you in forming bug reports that can be handled in an effective fashion. No one is required to follow them but doing so tends to be to everyone's advantage.


We cannot promise to fix every bug right away. If the bug is obvious, critical, or affects a lot of users, chances are good that someone will look into it. It could also happen that we tell you to update to a newer version to see if the bug happens there. Or we might decide that the bug cannot be fixed before some major rewrite we might be planning is done. Or perhaps it is simply too hard and there are more important things on the agenda. If you need help immediately, consider obtaining a commercial support contract.


Before you report a bug, please read and re-read the documentation to verify that you can really do whatever it is you are trying. If it is not clear from the documentation whether you can do something or not, please report that too; it is a bug in the documentation. If it turns out that a program does something different from what the documentation says, that is a bug. That might include, but is not limited to, the following circumstances:


Here“program”refers to any executable, not only the backend process.


Being slow or resource-hogging is not necessarily a bug. Read the documentation or ask on one of the mailing lists for help in tuning your applications. Failing to comply to theSQLstandard is not necessarily a bug either, unless compliance for the specific feature is explicitly claimed.


Before you continue, check on the TODO list and in the FAQ to see if your bug is already known. If you cannot decode the information on the TODO list, report your problem. The least we can do is make the TODO list clearer.


The most important thing to remember about bug reporting is to state all the facts and only facts. Do not speculate what you think went wrong, what“it seemed to do”, or which part of the program has a fault. If you are not familiar with the implementation you would probably guess wrong and not help us a bit. And even if you are, educated explanations are a great supplement to but no substitute for facts. If we are going to fix the bug we still have to see it happen for ourselves first. Reporting the bare facts is relatively straightforward (you can probably copy and paste them from the screen) but all too often important details are left out because someone thought it does not matter or the report would be understood anyway.


The following items should be contained in every bug report:


Do not be afraid if your bug report becomes rather lengthy. That is a fact of life. It is better to report everything the first time than us having to squeeze the facts out of you. On the other hand, if your input files are huge, it is fair to ask first whether somebody is interested in looking into it. Here is an[article](https://www.chiark.greenend.org.uk/~sgtatham/bugs.html)that outlines some more tips on reporting bugs.


Do not spend all your time to figure out which changes in the input make the problem go away. This will probably not help solving it. If it turns out that the bug cannot be fixed right away, you will still have time to find and share your work-around. Also, once again, do not waste your time guessing why the bug exists. We will find that out soon enough.


When writing a bug report, please avoid confusing terminology. The software package in total is called“PostgreSQL”, sometimes“Postgres”for short. If you are specifically talking about the backend process, mention that, do not just say“PostgreSQL crashes”. A crash of a single backend process is quite different from crash of the parent“postgres”process; please don't say“the server crashed”when you mean a single backend process went down, nor vice versa. Also, client programs such as the interactive frontend“psql”are completely separate from the backend. Please try to be specific about whether the problem is on the client or server side.


In general, send bug reports to the bug report mailing list at`<pgsql-bugs@lists.postgresql.org>`. You are requested to use a descriptive subject for your email message, perhaps parts of the error message.


Another method is to fill in the bug report web-form available at the project's[web site](https://www.postgresql.org/). Entering a bug report this way causes it to be mailed to the`<pgsql-bugs@lists.postgresql.org>`mailing list.


If your bug report has security implications and you'd prefer that it not become immediately visible in public archives, don't send it to`pgsql-bugs`. Security issues can be reported privately to`<security@postgresql.org>`.


Do not send bug reports to any of the user mailing lists, such as`<pgsql-sql@lists.postgresql.org>`or`<pgsql-general@lists.postgresql.org>`. These mailing lists are for answering user questions, and their subscribers normally do not wish to receive bug reports. More importantly, they are unlikely to fix them.


Also, please donotsend reports to the developers' mailing list`<pgsql-hackers@lists.postgresql.org>`. This list is for discussing the development ofPostgreSQL, and it would be nice if we could keep the bug reports separate. We might choose to take up a discussion about your bug report on`pgsql-hackers`, if the problem needs more review.


If you have a problem with the documentation, the best place to report it is the documentation mailing list`<pgsql-docs@lists.postgresql.org>`. Please be specific about what part of the documentation you are unhappy with.


If your bug is a portability problem on a non-supported platform, send mail to`<pgsql-hackers@lists.postgresql.org>`, so we (and you) can work on portingPostgreSQLto your platform.
